#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_timer.h"
#include "esp_netif.h"
#include "driver/gpio.h"
#include "driver/i2c.h"
#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include "lwip/netdb.h"
#include "esp32_ptt_streamer.h"

static const char *TAG = "PTT_FIRMWARE";
static QueueHandle_t s_isr_evt_queue = NULL;
static QueueHandle_t s_telemetry_queue = NULL;
static EventGroupHandle_t s_wifi_event_group = NULL;
static const int WIFI_CONNECTED_BIT = BIT0;

static volatile uint32_t s_isr_drop_count = 0;
static volatile uint32_t s_telemetry_drop_count = 0;
static uint32_t s_packet_sequence = 0;
static uint32_t s_reported_isr_drops = 0;
static uint32_t s_reported_telemetry_drops = 0;

static void IRAM_ATTR ads1115_isr_handler(void *arg) {
    (void)arg;
    uint64_t now_us = (uint64_t)esp_timer_get_time();
    isr_event_t evt = {
        .type = EVENT_ADS1115_READY,
        .timestamp_us = now_us
    };
    BaseType_t high_task_woken = pdFALSE;
    if (xQueueSendFromISR(s_isr_evt_queue, &evt, &high_task_woken) != pdTRUE) {
        s_isr_drop_count++;
    }
    if (high_task_woken) {
        portYIELD_FROM_ISR();
    }
}

static void IRAM_ATTR max30102_isr_handler(void *arg) {
    (void)arg;
    uint64_t now_us = (uint64_t)esp_timer_get_time();
    isr_event_t evt = {
        .type = EVENT_MAX30102_READY,
        .timestamp_us = now_us
    };
    BaseType_t high_task_woken = pdFALSE;
    if (xQueueSendFromISR(s_isr_evt_queue, &evt, &high_task_woken) != pdTRUE) {
        s_isr_drop_count++;
    }
    if (high_task_woken) {
        portYIELD_FROM_ISR();
    }
}

static esp_err_t i2c_master_init(void) {
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = PIN_I2C_SDA,
        .scl_io_num = PIN_I2C_SCL,
        .sda_pullup_en = GPIO_PULLUP_DISABLE,
        .scl_pullup_en = GPIO_PULLUP_DISABLE,
        .master.clk_speed = I2C_MASTER_FREQ_HZ,
    };
    esp_err_t err = i2c_param_config(I2C_MASTER_PORT, &conf);
    if (err != ESP_OK) {
        return err;
    }
    return i2c_driver_install(I2C_MASTER_PORT, conf.mode, 0, 0, 0);
}

static esp_err_t ads1115_init(void) {
    uint8_t hi_thresh[3] = {0x03, 0x80, 0x00};
    uint8_t lo_thresh[3] = {0x02, 0x00, 0x00};
    uint8_t cfg[3] = {0x01, ADS1115_CFG_MSB, ADS1115_CFG_LSB_475SPS};

    esp_err_t err;
    err = i2c_master_write_to_device(I2C_MASTER_PORT, ADS1115_ADDR, hi_thresh, 3, pdMS_TO_TICKS(10));
    if (err != ESP_OK) {
        return err;
    }
    err = i2c_master_write_to_device(I2C_MASTER_PORT, ADS1115_ADDR, lo_thresh, 3, pdMS_TO_TICKS(10));
    if (err != ESP_OK) {
        return err;
    }
    return i2c_master_write_to_device(I2C_MASTER_PORT, ADS1115_ADDR, cfg, 3, pdMS_TO_TICKS(10));
}

static esp_err_t max30102_init(void) {
    uint8_t reset_cmd[2] = {MAX30102_REG_MODE_CONFIG, 0x40};
    esp_err_t err = i2c_master_write_to_device(I2C_MASTER_PORT, MAX30102_ADDR, reset_cmd, 2, pdMS_TO_TICKS(10));
    if (err != ESP_OK) {
        return err;
    }
    vTaskDelay(pdMS_TO_TICKS(10));

    uint8_t reg_fifo_ptrs[4] = {MAX30102_REG_FIFO_WR_PTR, 0x00, 0x00, 0x00};
    err = i2c_master_write_to_device(I2C_MASTER_PORT, MAX30102_ADDR, reg_fifo_ptrs, 4, pdMS_TO_TICKS(10));
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "MAX30102 FIFO pointer clear failed: %s", esp_err_to_name(err));
        return err;
    }

    uint8_t reg_fifo[2] = {MAX30102_REG_FIFO_CONFIG, MAX30102_FIFO_CFG_NO_AVE};
    uint8_t reg_mode[2] = {MAX30102_REG_MODE_CONFIG, MAX30102_MODE_SPO2};
    uint8_t reg_spo2[2] = {MAX30102_REG_SPO2_CONFIG, MAX30102_SPO2_CFG_400SPS};
    uint8_t reg_led_red[2] = {MAX30102_REG_LED1_PA, MAX30102_LED_PA_7MA};
    uint8_t reg_led_ir[2] = {MAX30102_REG_LED2_PA, MAX30102_LED_PA_7MA};
    uint8_t reg_int_en[2] = {MAX30102_REG_INT_EN1, MAX30102_INT_PPG_RDY | MAX30102_INT_A_FULL};
    const uint8_t (*writes[])[2] = {&reg_fifo, &reg_mode, &reg_spo2, &reg_led_red, &reg_led_ir};
    for (size_t i = 0; i < sizeof(writes) / sizeof(writes[0]); ++i) {
        err = i2c_master_write_to_device(I2C_MASTER_PORT, MAX30102_ADDR, *writes[i], 2, pdMS_TO_TICKS(10));
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "MAX30102 config write %u failed: %s", (unsigned)i, esp_err_to_name(err));
            return err;
        }
    }

    uint8_t status_regs[2] = {MAX30102_REG_INT_STATUS1, MAX30102_REG_INT_STATUS2};
    uint8_t status_val = 0;
    for (int i = 0; i < 2; ++i) {
        err = i2c_master_write_read_device(I2C_MASTER_PORT, MAX30102_ADDR, &status_regs[i], 1, &status_val, 1, pdMS_TO_TICKS(10));
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "MAX30102 status clear failed: %s", esp_err_to_name(err));
            return err;
        }
    }

    return i2c_master_write_to_device(I2C_MASTER_PORT, MAX30102_ADDR, reg_int_en, 2, pdMS_TO_TICKS(10));
}

static void wifi_event_handler(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data) {
    (void)arg;
    (void)event_data;
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        xEventGroupClearBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
        esp_wifi_connect();
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

static void wifi_init_sta(void) {
    s_wifi_event_group = xEventGroupCreate();
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_event_handler, NULL, NULL));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = CONFIG_WIFI_SSID,
            .password = CONFIG_WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
}

static void enqueue_telemetry(uint64_t timestamp_us, int16_t ecg_raw, uint32_t ppg_ir,
                              uint8_t lead_off, uint8_t quality_flags, int32_t skew_us,
                              char sample_type) {
    uint32_t isr_drops = s_isr_drop_count;
    uint32_t telemetry_drops = s_telemetry_drop_count;
    if (isr_drops != s_reported_isr_drops || telemetry_drops != s_reported_telemetry_drops) {
        quality_flags |= QUALITY_FLAG_QUEUE_DROP;
    }
    telemetry_packet_t pkt = {
        .seq = s_packet_sequence++,
        .timestamp_us = timestamp_us,
        .ecg_raw = ecg_raw,
        .ppg_ir = ppg_ir,
        .lead_off = lead_off,
        .quality_flags = quality_flags,
        .mcu_skew_us = skew_us,
        .sample_type = sample_type,
    };
    if (xQueueSend(s_telemetry_queue, &pkt, 0) != pdTRUE) {
        s_telemetry_drop_count++;
    } else {
        s_reported_isr_drops = isr_drops;
        s_reported_telemetry_drops = telemetry_drops;
    }
}

static void sensor_acquisition_task(void *pvParameters) {
    (void)pvParameters;
    isr_event_t evt;
    uint8_t ads_reg = 0x00;
    uint8_t ads_buf[2];

    uint8_t ptr_reg = MAX30102_REG_FIFO_WR_PTR;
    uint8_t ptr_buf[3];
    uint8_t fifo_reg = MAX30102_REG_FIFO_DATA;
    uint8_t fifo_buf[192];
    uint8_t max_status_regs[2] = {MAX30102_REG_INT_STATUS1, MAX30102_REG_INT_STATUS2};
    uint8_t max_status[2];

    int16_t latest_ecg = 0;
    uint64_t last_ecg_ts = 0;
    uint64_t last_ppg_ts = 0;
    uint64_t next_ppg_poll_us = 0;

    while (1) {
        uint64_t now_us = (uint64_t)esp_timer_get_time();
        BaseType_t have_event;
        if (!gpio_get_level(PIN_MAX_INT) && now_us >= next_ppg_poll_us) {
            evt.type = EVENT_MAX30102_READY;
            evt.timestamp_us = now_us;
            next_ppg_poll_us = now_us + 10000ULL;
            have_event = pdTRUE;
        } else {
            have_event = xQueueReceive(s_isr_evt_queue, &evt, pdMS_TO_TICKS(10));
        }
        if (have_event == pdTRUE) {
            if (evt.type == EVENT_ADS1115_READY) {
                uint8_t lod = 0;
                if (gpio_get_level(PIN_LOD_PLUS)) {
                    lod |= 0x01;
                }
                if (gpio_get_level(PIN_LOD_MINUS)) {
                    lod |= 0x02;
                }

                uint8_t q_flags = 0;
                if (lod & 0x01) {
                    q_flags |= QUALITY_FLAG_LOD_POS;
                }
                if (lod & 0x02) {
                    q_flags |= QUALITY_FLAG_LOD_NEG;
                }

                esp_err_t ads_err = i2c_master_write_read_device(I2C_MASTER_PORT, ADS1115_ADDR, &ads_reg, 1, ads_buf, 2, pdMS_TO_TICKS(5));
                uint64_t read_done_us = (uint64_t)esp_timer_get_time();
                if (ads_read_window_uncertain(evt.timestamp_us, read_done_us)) {
                    q_flags |= QUALITY_FLAG_TIMESTAMP_UNCERTAIN;
                }
                if (ads_err != ESP_OK) {
                    q_flags |= QUALITY_FLAG_I2C_ERROR;
                    enqueue_telemetry(evt.timestamp_us, 0, 0, lod, q_flags, 0, SAMPLE_TYPE_ECG);
                    continue;
                }
                last_ecg_ts = evt.timestamp_us;
                latest_ecg = (int16_t)((ads_buf[0] << 8) | ads_buf[1]);
                if (latest_ecg >= 32700 || latest_ecg <= -32700) {
                    q_flags |= QUALITY_FLAG_SATURATED;
                }

                int32_t skew_val = (last_ppg_ts == 0) ? 0 : (int32_t)((int64_t)last_ecg_ts - (int64_t)last_ppg_ts);
                enqueue_telemetry(last_ecg_ts, latest_ecg, 0, lod, q_flags, skew_val, SAMPLE_TYPE_ECG);
            } else if (evt.type == EVENT_MAX30102_READY) {
                uint8_t base_flags = 0;

                esp_err_t ptr_err = i2c_master_write_read_device(I2C_MASTER_PORT, MAX30102_ADDR, &ptr_reg, 1, ptr_buf, 3, pdMS_TO_TICKS(5));
                esp_err_t st1_err = i2c_master_write_read_device(I2C_MASTER_PORT, MAX30102_ADDR, &max_status_regs[0], 1, &max_status[0], 1, pdMS_TO_TICKS(5));
                esp_err_t st2_err = i2c_master_write_read_device(I2C_MASTER_PORT, MAX30102_ADDR, &max_status_regs[1], 1, &max_status[1], 1, pdMS_TO_TICKS(5));
                if (ptr_err != ESP_OK || st1_err != ESP_OK || st2_err != ESP_OK) {
                    enqueue_telemetry(evt.timestamp_us, 0, 0, 0,
                                      (uint8_t)(base_flags | QUALITY_FLAG_I2C_ERROR | QUALITY_FLAG_TIMESTAMP_UNCERTAIN),
                                      0, SAMPLE_TYPE_PPG);
                    continue;
                }

                int num_samples = max30102_fifo_sample_count(ptr_buf[0] & 0x1F, ptr_buf[2] & 0x1F, ptr_buf[1] & 0x1F);
                if (num_samples <= 0) {
                    continue;
                }

                int bytes_to_read = num_samples * 6;
                esp_err_t fifo_err = i2c_master_write_read_device(I2C_MASTER_PORT, MAX30102_ADDR, &fifo_reg, 1, fifo_buf, bytes_to_read, pdMS_TO_TICKS(10));
                if (fifo_err != ESP_OK) {
                    enqueue_telemetry(evt.timestamp_us, 0, 0, 0,
                                      (uint8_t)(base_flags | QUALITY_FLAG_I2C_ERROR | QUALITY_FLAG_TIMESTAMP_UNCERTAIN),
                                      0, SAMPLE_TYPE_PPG);
                    continue;
                }
                last_ppg_ts = evt.timestamp_us;

                uint8_t burst_flags = ppg_burst_quality_flags(base_flags, num_samples,
                                                              ptr_buf[1] & 0x1F,
                                                              (max_status[0] & MAX30102_INT_A_FULL) != 0U);
                for (int i = 0; i < num_samples; i++) {
                    int offset = i * 6;
                    uint32_t ir = ((uint32_t)(fifo_buf[offset + 3] & 0x03) << 16) |
                                  ((uint32_t)fifo_buf[offset + 4] << 8) |
                                  (uint32_t)fifo_buf[offset + 5];
                    uint8_t sample_flags = burst_flags;
                    if (ir >= 260000U) {
                        sample_flags |= QUALITY_FLAG_SATURATED;
                    }
                    enqueue_telemetry(evt.timestamp_us, 0, ir, 0, sample_flags, 0, SAMPLE_TYPE_PPG);
                }
            }
        }
    }
}

static void udp_transmission_task(void *pvParameters) {
    (void)pvParameters;
    xEventGroupWaitBits(s_wifi_event_group, WIFI_CONNECTED_BIT, pdFALSE, pdTRUE, portMAX_DELAY);

    struct sockaddr_in dest_addr;
    dest_addr.sin_addr.s_addr = inet_addr(CONFIG_TARGET_IP);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(CONFIG_UDP_PORT);

    int sock;
    while ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP)) < 0) {
        ESP_LOGE(TAG, "UDP socket creation failed");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }

    struct timeval timeout = {
        .tv_sec = 0,
        .tv_usec = 50000,
    };
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));

    telemetry_packet_t pkt;
    char payload_str[160];

    while (1) {
        if (xQueueReceive(s_telemetry_queue, &pkt, portMAX_DELAY) == pdTRUE) {
            int len = snprintf(payload_str, sizeof(payload_str), "%u,%llu,%d,%u,%u,%u,%d,%c\n",
                               pkt.seq,
                               (unsigned long long)pkt.timestamp_us,
                               pkt.ecg_raw,
                               pkt.ppg_ir,
                               pkt.lead_off,
                               pkt.quality_flags,
                               pkt.mcu_skew_us,
                               pkt.sample_type);
            if (len <= 0 || (size_t)len >= sizeof(payload_str)) {
                ESP_LOGE(TAG, "Telemetry formatting failed");
                continue;
            }
            if (sendto(sock, payload_str, (size_t)len, 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)) != len) {
                ESP_LOGW(TAG, "UDP telemetry send failed");
                vTaskDelay(pdMS_TO_TICKS(10));
            }
        }
    }

    if (sock >= 0) {
        close(sock);
    }
    vTaskDelete(NULL);
}

void app_main(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    gpio_config_t lod_conf = {
        .pin_bit_mask = (1ULL << PIN_LOD_PLUS) | (1ULL << PIN_LOD_MINUS),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    ESP_ERROR_CHECK(gpio_config(&lod_conf));

    ESP_ERROR_CHECK(i2c_master_init());
    ESP_ERROR_CHECK(ads1115_init());
    ESP_ERROR_CHECK(max30102_init());

    s_isr_evt_queue = xQueueCreate(QUEUE_SIZE_ISR, sizeof(isr_event_t));
    s_telemetry_queue = xQueueCreate(QUEUE_SIZE_TELEMETRY, sizeof(telemetry_packet_t));
    ESP_ERROR_CHECK(s_isr_evt_queue && s_telemetry_queue ? ESP_OK : ESP_ERR_NO_MEM);

    gpio_config_t isr_pins_conf = {
        .pin_bit_mask = (1ULL << PIN_ADS_ALERT) | (1ULL << PIN_MAX_INT),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .intr_type = GPIO_INTR_NEGEDGE
    };
    ESP_ERROR_CHECK(gpio_config(&isr_pins_conf));

    ESP_ERROR_CHECK(gpio_install_isr_service(0));
    ESP_ERROR_CHECK(gpio_isr_handler_add(PIN_ADS_ALERT, ads1115_isr_handler, NULL));
    ESP_ERROR_CHECK(gpio_isr_handler_add(PIN_MAX_INT, max30102_isr_handler, NULL));

    wifi_init_sta();

    xTaskCreatePinnedToCore(sensor_acquisition_task, "sensor_task", 4096, NULL, 12, NULL, 0);
    xTaskCreatePinnedToCore(udp_transmission_task, "udp_task", 4096, NULL, 5, NULL, 1);
}
