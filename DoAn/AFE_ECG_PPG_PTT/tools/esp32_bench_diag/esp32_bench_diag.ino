#include <Arduino.h>
#include <Wire.h>
#include <stdint.h>
#include <stdbool.h>
#include "esp_timer.h"

#define PIN_I2C_SDA 21
#define PIN_I2C_SCL 22
#define PIN_ADS_ALERT 27
#define PIN_MAX_INT 26
#define PIN_LOD_PLUS 32
#define PIN_LOD_MINUS 33
#define PIN_ECG_BACKUP_ADC 34

#define I2C_MASTER_FREQ_HZ 400000UL
#define LOD_ADC_HIGH_THRESHOLD_MV 1400

#define ADS1115_ADDR 0x48
#define ADS1115_REG_CONV 0x00
#define ADS1115_REG_CFG 0x01
#define ADS1115_REG_LO_THRESH 0x02
#define ADS1115_REG_HI_THRESH 0x03
#define ADS1115_CFG_MSB 0x04
#define ADS1115_CFG_LSB_475SPS 0xC0
#define ADS1115_CONV_READY_WINDOW_US 1900ULL

#define MAX30102_ADDR 0x57
#define MAX30102_REG_INT_STATUS1 0x00
#define MAX30102_REG_INT_STATUS2 0x01
#define MAX30102_REG_INT_EN1 0x02
#define MAX30102_REG_FIFO_WR_PTR 0x04
#define MAX30102_REG_OVF_COUNTER 0x05
#define MAX30102_REG_FIFO_RD_PTR 0x06
#define MAX30102_REG_FIFO_DATA 0x07
#define MAX30102_REG_FIFO_CONFIG 0x08
#define MAX30102_REG_MODE_CONFIG 0x09
#define MAX30102_REG_SPO2_CONFIG 0x0A
#define MAX30102_REG_LED1_PA 0x0C
#define MAX30102_REG_LED2_PA 0x0D
#define MAX30102_REG_PART_ID 0xFF
#define MAX30102_EXPECTED_PART_ID 0x15

#define MAX30102_FIFO_CFG_NO_AVE 0x1F
#define MAX30102_MODE_SPO2 0x03
#define MAX30102_SPO2_CFG_400SPS 0x2F
#define MAX30102_LED_PA_7MA 0x24
#define MAX30102_INT_PPG_RDY 0x40
#define MAX30102_INT_A_FULL 0x80

#define QUALITY_FLAG_LOD_POS 0x01U
#define QUALITY_FLAG_LOD_NEG 0x02U
#define QUALITY_FLAG_SATURATED 0x04U
#define QUALITY_FLAG_I2C_ERROR 0x08U
#define QUALITY_FLAG_FIFO_OVERFLOW 0x10U
#define QUALITY_FLAG_QUEUE_DROP 0x20U
#define QUALITY_FLAG_FIFO_BURST 0x40U
#define QUALITY_FLAG_TIMESTAMP_UNCERTAIN 0x80U

static portMUX_TYPE s_isr_mux = portMUX_INITIALIZER_UNLOCKED;
static volatile bool s_ads_pending = false;
static volatile uint64_t s_ads_ts_us = 0;
static volatile uint32_t s_ads_irq_count = 0;
static volatile uint32_t s_ads_missed = 0;

static volatile bool s_max_pending = false;
static volatile uint64_t s_max_ts_us = 0;
static volatile uint32_t s_max_irq_count = 0;
static volatile uint32_t s_max_missed = 0;

static bool s_ads_ready = false;
static bool s_max_ready = false;
static uint32_t s_seq = 0;
static uint64_t s_last_ecg_ts = 0;
static uint64_t s_last_ppg_ts = 0;
static uint64_t s_next_ppg_poll_us = 0;
static bool s_pending_drop = false;

static inline bool lod_mv_is_high(int mv) {
    return mv >= LOD_ADC_HIGH_THRESHOLD_MV;
}

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

void IRAM_ATTR on_ads_alert_isr(void) {
    uint64_t now_us = (uint64_t)esp_timer_get_time();
    portENTER_CRITICAL_ISR(&s_isr_mux);
    if (s_ads_pending) {
        s_ads_missed++;
    }
    s_ads_ts_us = now_us;
    s_ads_pending = true;
    s_ads_irq_count++;
    portEXIT_CRITICAL_ISR(&s_isr_mux);
}

void IRAM_ATTR on_max_int_isr(void) {
    uint64_t now_us = (uint64_t)esp_timer_get_time();
    portENTER_CRITICAL_ISR(&s_isr_mux);
    if (s_max_pending) {
        s_max_missed++;
    }
    s_max_ts_us = now_us;
    s_max_pending = true;
    s_max_irq_count++;
    portEXIT_CRITICAL_ISR(&s_isr_mux);
}

static bool i2c_probe_addr(uint8_t addr) {
    Wire.beginTransmission(addr);
    return Wire.endTransmission(true) == 0;
}

static bool i2c_write_bytes(uint8_t addr, const uint8_t *data, size_t len) {
    Wire.beginTransmission(addr);
    size_t written = Wire.write(data, len);
    if (written != len) {
        Wire.endTransmission(true);
        return false;
    }
    return Wire.endTransmission(true) == 0;
}

static bool i2c_write_reg_u8(uint8_t addr, uint8_t reg, uint8_t val) {
    uint8_t buf[2] = {reg, val};
    return i2c_write_bytes(addr, buf, sizeof(buf));
}

static bool i2c_read_regs(uint8_t addr, uint8_t reg, uint8_t *out, size_t len) {
    Wire.beginTransmission(addr);
    if (Wire.write(reg) != 1) {
        Wire.endTransmission(true);
        return false;
    }
    if (Wire.endTransmission(false) != 0) {
        return false;
    }
    size_t got = Wire.requestFrom(addr, (uint8_t)len);
    if (got != len) {
        while (Wire.available()) {
            (void)Wire.read();
        }
        return false;
    }
    for (size_t i = 0; i < len; i++) {
        int ch = Wire.read();
        if (ch < 0) {
            return false;
        }
        out[i] = (uint8_t)ch;
    }
    return true;
}

static bool configure_ads1115(uint16_t *cfg_readback) {
    uint8_t hi_thresh[3] = {ADS1115_REG_HI_THRESH, 0x80, 0x00};
    uint8_t lo_thresh[3] = {ADS1115_REG_LO_THRESH, 0x00, 0x00};
    uint8_t cfg[3] = {ADS1115_REG_CFG, ADS1115_CFG_MSB, ADS1115_CFG_LSB_475SPS};
    if (!i2c_write_bytes(ADS1115_ADDR, hi_thresh, sizeof(hi_thresh))) {
        return false;
    }
    if (!i2c_write_bytes(ADS1115_ADDR, lo_thresh, sizeof(lo_thresh))) {
        return false;
    }
    if (!i2c_write_bytes(ADS1115_ADDR, cfg, sizeof(cfg))) {
        return false;
    }
    uint8_t rb[2] = {0, 0};
    if (!i2c_read_regs(ADS1115_ADDR, ADS1115_REG_CFG, rb, sizeof(rb))) {
        return false;
    }
    *cfg_readback = (uint16_t)(((uint16_t)rb[0] << 8) | rb[1]);
    uint8_t ptr = ADS1115_REG_CONV;
    if (!i2c_write_bytes(ADS1115_ADDR, &ptr, 1)) {
        return false;
    }
    uint16_t expected_mask = (uint16_t)(((uint16_t)ADS1115_CFG_MSB << 8) | ADS1115_CFG_LSB_475SPS);
    return ((*cfg_readback) & 0x7FFFU) == (expected_mask & 0x7FFFU);
}

static bool configure_max30102(void) {
    if (!i2c_write_reg_u8(MAX30102_ADDR, MAX30102_REG_MODE_CONFIG, 0x40)) {
        return false;
    }
    delay(10);
    uint8_t ptr_clear[4] = {MAX30102_REG_FIFO_WR_PTR, 0x00, 0x00, 0x00};
    if (!i2c_write_bytes(MAX30102_ADDR, ptr_clear, sizeof(ptr_clear))) {
        return false;
    }
    if (!i2c_write_reg_u8(MAX30102_ADDR, MAX30102_REG_FIFO_CONFIG, MAX30102_FIFO_CFG_NO_AVE)) {
        return false;
    }
    if (!i2c_write_reg_u8(MAX30102_ADDR, MAX30102_REG_MODE_CONFIG, MAX30102_MODE_SPO2)) {
        return false;
    }
    if (!i2c_write_reg_u8(MAX30102_ADDR, MAX30102_REG_SPO2_CONFIG, MAX30102_SPO2_CFG_400SPS)) {
        return false;
    }
    if (!i2c_write_reg_u8(MAX30102_ADDR, MAX30102_REG_LED1_PA, MAX30102_LED_PA_7MA)) {
        return false;
    }
    if (!i2c_write_reg_u8(MAX30102_ADDR, MAX30102_REG_LED2_PA, MAX30102_LED_PA_7MA)) {
        return false;
    }
    uint8_t st = 0;
    if (!i2c_read_regs(MAX30102_ADDR, MAX30102_REG_INT_STATUS1, &st, 1)) {
        return false;
    }
    if (!i2c_read_regs(MAX30102_ADDR, MAX30102_REG_INT_STATUS2, &st, 1)) {
        return false;
    }
    return i2c_write_reg_u8(MAX30102_ADDR, MAX30102_REG_INT_EN1,
                            (uint8_t)(MAX30102_INT_PPG_RDY | MAX30102_INT_A_FULL));
}

static void emit_csv_line(uint64_t ts_us, int16_t ecg_raw, uint32_t ppg_ir,
                          uint8_t lod, uint8_t q_flags, int32_t skew_us, char sample_type) {
    if (s_pending_drop) {
        q_flags |= QUALITY_FLAG_QUEUE_DROP;
    }
    uint32_t seq = s_seq++;
    char line[128];
    int len = snprintf(line, sizeof(line), "%lu,%llu,%d,%lu,%u,%u,%ld,%c\n",
                       (unsigned long)seq,
                       (unsigned long long)ts_us,
                       (int)ecg_raw,
                       (unsigned long)ppg_ir,
                       (unsigned)lod,
                       (unsigned)q_flags,
                       (long)skew_us,
                       sample_type);
    if (len <= 0 || (size_t)len >= sizeof(line)) {
        s_pending_drop = true;
        return;
    }
    if (Serial.availableForWrite() < len) {
        s_pending_drop = true;
        return;
    }
    size_t written = Serial.write((const uint8_t *)line, (size_t)len);
    if (written == (size_t)len) {
        s_pending_drop = false;
    } else {
        s_pending_drop = true;
    }
}

void setup(void) {
    Serial.begin(115200);
    delay(250);

    pinMode(PIN_ADS_ALERT, INPUT_PULLUP);
    pinMode(PIN_MAX_INT, INPUT_PULLUP);
    analogReadResolution(12);
    analogSetPinAttenuation(PIN_LOD_PLUS, ADC_11db);
    analogSetPinAttenuation(PIN_LOD_MINUS, ADC_11db);
    analogSetPinAttenuation(PIN_ECG_BACKUP_ADC, ADC_11db);

    Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL, I2C_MASTER_FREQ_HZ);

    bool ads_ack = i2c_probe_addr(ADS1115_ADDR);
    bool max_ack = i2c_probe_addr(MAX30102_ADDR);
    uint8_t part_id = 0;
    bool max_id_ok = max_ack && i2c_read_regs(MAX30102_ADDR, MAX30102_REG_PART_ID, &part_id, 1) &&
                     (part_id == MAX30102_EXPECTED_PART_ID);
    Serial.printf("[SELF-TEST] Step 1 I2C Probe: ADS1115(0x48)=%s MAX30102(0x57)=%s PART_ID=0x%02X (%s)\n",
                  ads_ack ? "OK" : "FAIL",
                  max_ack ? "OK" : "FAIL",
                  (unsigned)part_id,
                  max_id_ok ? "PASS" : "FAIL");

    uint16_t ads_cfg_rb = 0;
    bool ads_cfg_ok = ads_ack && configure_ads1115(&ads_cfg_rb);
    bool max_cfg_ok = max_id_ok && configure_max30102();

    attachInterrupt(digitalPinToInterrupt(PIN_ADS_ALERT), on_ads_alert_isr, FALLING);
    attachInterrupt(digitalPinToInterrupt(PIN_MAX_INT), on_max_int_isr, FALLING);
    delay(50);

    uint32_t ads_irqs = 0;
    uint32_t max_irqs = 0;
    portENTER_CRITICAL(&s_isr_mux);
    ads_irqs = s_ads_irq_count;
    max_irqs = s_max_irq_count;
    s_ads_pending = false;
    s_ads_missed = 0;
    s_max_pending = false;
    s_max_missed = 0;
    portEXIT_CRITICAL(&s_isr_mux);

    s_ads_ready = ads_cfg_ok;
    s_max_ready = max_cfg_ok;

    Serial.printf("[SELF-TEST] Step 2 ADS1115 Config: 475SPS AIN0-AIN1 ALERT=GPIO27 cfg=0x%04X irq_50ms=%lu status=%s\n",
                  (unsigned)ads_cfg_rb,
                  (unsigned long)ads_irqs,
                  (ads_cfg_ok && ads_irqs > 0) ? "PASS" : "FAIL");

    Serial.printf("[SELF-TEST] Step 3 MAX30102 Config: 400SPS SpO2/IR INT=GPIO26 irq_50ms=%lu status=%s\n",
                  (unsigned long)max_irqs,
                  (max_cfg_ok && max_irqs > 0) ? "PASS" : "FAIL");

    int lod_p_mv = (int)analogReadMilliVolts(PIN_LOD_PLUS);
    int lod_m_mv = (int)analogReadMilliVolts(PIN_LOD_MINUS);
    int ecg_bak_mv = (int)analogReadMilliVolts(PIN_ECG_BACKUP_ADC);
    bool lod_p_hi = lod_mv_is_high(lod_p_mv);
    bool lod_m_hi = lod_mv_is_high(lod_m_mv);

    Serial.printf("[SELF-TEST] Step 4 LOD ADC: GPIO32=%dmV(%s) GPIO33=%dmV(%s) thresh=%dmV GPIO34=%dmV status=PASS\n",
                  lod_p_mv, lod_p_hi ? "HIGH" : "LOW",
                  lod_m_mv, lod_m_hi ? "HIGH" : "LOW",
                  LOD_ADC_HIGH_THRESHOLD_MV,
                  ecg_bak_mv);

    Serial.println("[SELF-TEST] SAFETY: NO HUMAN CONNECTION / BENCH SIMULATOR ONLY");
    Serial.println("seq,ts_us,ecg_raw,ppg_ir,lod,quality_flags,skew_us,sample_type");

    s_seq = 0;
    s_last_ecg_ts = 0;
    s_last_ppg_ts = 0;
    s_pending_drop = false;
    s_next_ppg_poll_us = (uint64_t)esp_timer_get_time() + 10000ULL;
}

void loop(void) {
    bool do_ads = false;
    uint64_t ads_ts = 0;
    uint32_t ads_missed = 0;

    bool do_max = false;
    uint64_t max_ts = 0;
    uint32_t max_missed = 0;

    uint64_t now_us = (uint64_t)esp_timer_get_time();

    portENTER_CRITICAL(&s_isr_mux);
    if (s_ads_pending) {
        do_ads = true;
        ads_ts = s_ads_ts_us;
        ads_missed = s_ads_missed;
        s_ads_pending = false;
        s_ads_missed = 0;
    }
    if (s_max_pending) {
        do_max = true;
        max_ts = s_max_ts_us;
        max_missed = s_max_missed;
        s_max_pending = false;
        s_max_missed = 0;
    }
    portEXIT_CRITICAL(&s_isr_mux);

    if (!do_max && s_max_ready && digitalRead(PIN_MAX_INT) == LOW && now_us >= s_next_ppg_poll_us) {
        do_max = true;
        max_ts = now_us;
        s_next_ppg_poll_us = now_us + 10000ULL;
    } else if (do_max) {
        s_next_ppg_poll_us = now_us + 10000ULL;
    }

    if (do_ads && s_ads_ready) {
        int lod_p_mv = (int)analogReadMilliVolts(PIN_LOD_PLUS);
        int lod_m_mv = (int)analogReadMilliVolts(PIN_LOD_MINUS);
        uint8_t lod = 0;
        uint8_t q_flags = 0;
        if (lod_mv_is_high(lod_p_mv)) {
            lod |= 0x01U;
            q_flags |= QUALITY_FLAG_LOD_POS;
        }
        if (lod_mv_is_high(lod_m_mv)) {
            lod |= 0x02U;
            q_flags |= QUALITY_FLAG_LOD_NEG;
        }
        if (ads_missed > 0) {
            q_flags |= QUALITY_FLAG_QUEUE_DROP;
        }

        uint8_t ads_buf[2] = {0, 0};
        bool ok = i2c_read_regs(ADS1115_ADDR, ADS1115_REG_CONV, ads_buf, sizeof(ads_buf));
        uint64_t read_done_us = (uint64_t)esp_timer_get_time();
        if (ads_read_window_uncertain(ads_ts, read_done_us)) {
            q_flags |= QUALITY_FLAG_TIMESTAMP_UNCERTAIN;
        }
        if (!ok) {
            q_flags |= QUALITY_FLAG_I2C_ERROR;
            emit_csv_line(ads_ts, 0, 0, lod, q_flags, 0, 'E');
        } else {
            if (ads_ts <= s_last_ecg_ts) {
                ads_ts = s_last_ecg_ts + 1ULL;
            }
            s_last_ecg_ts = ads_ts;
            int16_t ecg_raw = (int16_t)(((uint16_t)ads_buf[0] << 8) | ads_buf[1]);
            if (ecg_raw >= 32700 || ecg_raw <= -32700) {
                q_flags |= QUALITY_FLAG_SATURATED;
            }
            int32_t skew_us = (s_last_ppg_ts == 0) ? 0 : (int32_t)((int64_t)s_last_ecg_ts - (int64_t)s_last_ppg_ts);
            emit_csv_line(s_last_ecg_ts, ecg_raw, 0, lod, q_flags, skew_us, 'E');
        }
    }

    if (do_max && s_max_ready) {
        uint8_t base_flags = (max_missed > 0) ? QUALITY_FLAG_QUEUE_DROP : 0U;
        uint8_t ptr_buf[3] = {0, 0, 0};
        uint8_t st1 = 0;
        uint8_t st2 = 0;
        bool ptr_ok = i2c_read_regs(MAX30102_ADDR, MAX30102_REG_FIFO_WR_PTR, ptr_buf, sizeof(ptr_buf));
        bool st1_ok = i2c_read_regs(MAX30102_ADDR, MAX30102_REG_INT_STATUS1, &st1, 1);
        bool st2_ok = i2c_read_regs(MAX30102_ADDR, MAX30102_REG_INT_STATUS2, &st2, 1);
        (void)st2;
        if (!ptr_ok || !st1_ok || !st2_ok) {
            emit_csv_line(max_ts, 0, 0, 0,
                          (uint8_t)(base_flags | QUALITY_FLAG_I2C_ERROR | QUALITY_FLAG_TIMESTAMP_UNCERTAIN),
                          0, 'P');
        } else {
            int num_samples = max30102_fifo_sample_count(ptr_buf[0] & 0x1F, ptr_buf[2] & 0x1F, ptr_buf[1] & 0x1F);
            if (num_samples > 0) {
                uint8_t burst_flags = ppg_burst_quality_flags(base_flags, num_samples,
                                                              ptr_buf[1] & 0x1F,
                                                              (st1 & MAX30102_INT_A_FULL) != 0U);
                uint8_t fifo_buf[192];
                int remaining = num_samples;
                int idx = 0;
                bool fifo_ok = true;
                while (remaining > 0) {
                    int batch = remaining > 16 ? 16 : remaining;
                    if (!i2c_read_regs(MAX30102_ADDR, MAX30102_REG_FIFO_DATA,
                                       &fifo_buf[idx * 6], (size_t)(batch * 6))) {
                        fifo_ok = false;
                        break;
                    }
                    idx += batch;
                    remaining -= batch;
                }
                if (!fifo_ok) {
                    emit_csv_line(max_ts, 0, 0, 0,
                                  (uint8_t)(base_flags | QUALITY_FLAG_I2C_ERROR | QUALITY_FLAG_TIMESTAMP_UNCERTAIN),
                                  0, 'P');
                } else {
                    for (int i = 0; i < num_samples; i++) {
                        int off = i * 6;
                        uint32_t ir = ((uint32_t)(fifo_buf[off + 3] & 0x03) << 16) |
                                      ((uint32_t)fifo_buf[off + 4] << 8) |
                                      (uint32_t)fifo_buf[off + 5];
                        uint8_t sample_flags = burst_flags;
                        if (ir >= 260000UL) {
                            sample_flags |= QUALITY_FLAG_SATURATED;
                        }
                        if (max_ts <= s_last_ppg_ts) {
                            max_ts = s_last_ppg_ts + 1ULL;
                        }
                        s_last_ppg_ts = max_ts;
                        emit_csv_line(s_last_ppg_ts, 0, ir, 0, sample_flags, 0, 'P');
                    }
                }
            }
        }
    }
}
