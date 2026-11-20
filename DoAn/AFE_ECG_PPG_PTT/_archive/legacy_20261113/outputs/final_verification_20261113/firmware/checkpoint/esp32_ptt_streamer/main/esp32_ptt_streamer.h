#ifndef ESP32_PTT_STREAMER_H
#define ESP32_PTT_STREAMER_H

#include <stdint.h>
#include <stdbool.h>

#define PIN_I2C_SDA 21
#define PIN_I2C_SCL 22
#define PIN_ADS_ALERT 27
#define PIN_MAX_INT 26
#define PIN_LOD_PLUS 32
#define PIN_LOD_MINUS 33
#define PIN_ECG_BACKUP_ADC 34

#define I2C_MASTER_PORT 0
#define I2C_MASTER_FREQ_HZ 400000

#define ADS1115_ADDR 0x48
#define ADS1115_CFG_MSB 0x04
#define ADS1115_CFG_LSB_475SPS 0xC0
#define ADS1115_CFG_LSB_860SPS 0xE0
#define ADS1115_CONV_READY_WINDOW_US 1900ULL

#define MAX30102_ADDR 0x57
#define MAX30102_REG_FIFO_WR_PTR 0x04
#define MAX30102_REG_OVF_COUNTER 0x05
#define MAX30102_REG_FIFO_RD_PTR 0x06
#define MAX30102_REG_FIFO_DATA 0x07
#define MAX30102_REG_FIFO_CONFIG 0x08
#define MAX30102_REG_MODE_CONFIG 0x09
#define MAX30102_REG_SPO2_CONFIG 0x0A
#define MAX30102_REG_LED1_PA 0x0C
#define MAX30102_REG_LED2_PA 0x0D
#define MAX30102_REG_INT_EN1 0x02
#define MAX30102_REG_INT_STATUS1 0x00
#define MAX30102_REG_INT_STATUS2 0x01

#define MAX30102_FIFO_CFG_NO_AVE 0x1F
#define MAX30102_MODE_SPO2 0x03
#define MAX30102_SPO2_CFG_400SPS 0x2F
#define MAX30102_LED_PA_7MA 0x24
#define MAX30102_INT_PPG_RDY 0x40
#define MAX30102_INT_A_FULL 0x80

#define PPG_SAMPLE_PERIOD_US 2500ULL
#define ECG_SAMPLE_PERIOD_US 2105ULL

#define CONFIG_WIFI_SSID "AFE_PTT_NET"
#define CONFIG_WIFI_PASS "12345678"
#define CONFIG_TARGET_IP "192.168.4.2"
#define CONFIG_UDP_PORT 5005

#define QUEUE_SIZE_ISR 128
#define QUEUE_SIZE_TELEMETRY 256

#define QUALITY_FLAG_LOD_POS       (1U << 0)
#define QUALITY_FLAG_LOD_NEG       (1U << 1)
#define QUALITY_FLAG_SATURATED     (1U << 2)
#define QUALITY_FLAG_I2C_ERROR     (1U << 3)
#define QUALITY_FLAG_FIFO_OVERFLOW (1U << 4)
#define QUALITY_FLAG_QUEUE_DROP    (1U << 5)
#define QUALITY_FLAG_FIFO_BURST    (1U << 6)
#define QUALITY_FLAG_TIMESTAMP_UNCERTAIN (1U << 7)

#define SAMPLE_TYPE_ECG 'E'
#define SAMPLE_TYPE_PPG 'P'

static inline bool ads_read_window_uncertain(uint64_t evt_ts_us, uint64_t read_done_us) {
    return read_done_us > evt_ts_us && (read_done_us - evt_ts_us) > ADS1115_CONV_READY_WINDOW_US;
}

static inline int max30102_fifo_sample_count(uint8_t wr_ptr, uint8_t rd_ptr, uint8_t ovf_cnt) {
    int n = (int)wr_ptr - (int)rd_ptr;
    if (n < 0) {
        n += 32;
    }
    if (n == 0 && ovf_cnt > 0) {
        n = 32;
    }
    if (n > 32) {
        n = 32;
    }
    return n < 0 ? 0 : n;
}

static inline uint8_t ppg_burst_quality_flags(uint8_t base_flags, int num_samples,
                                              uint8_t ovf_cnt, bool fifo_a_full) {
    uint8_t flags = (uint8_t)(base_flags | QUALITY_FLAG_TIMESTAMP_UNCERTAIN);
    if (num_samples > 1) {
        flags |= QUALITY_FLAG_FIFO_BURST;
    }
    if (ovf_cnt > 0 || fifo_a_full) {
        flags |= QUALITY_FLAG_FIFO_OVERFLOW;
    }
    return flags;
}

typedef enum {
    EVENT_ADS1115_READY = 1,
    EVENT_MAX30102_READY = 2
} isr_event_type_t;

typedef struct {
    isr_event_type_t type;
    uint64_t timestamp_us;
} isr_event_t;

typedef struct __attribute__((packed)) {
    uint32_t seq;
    uint64_t timestamp_us;
    int16_t ecg_raw;
    uint32_t ppg_ir;
    uint8_t lead_off;
    uint8_t quality_flags;
    int32_t mcu_skew_us;
    char sample_type;
} telemetry_packet_t;

#endif
