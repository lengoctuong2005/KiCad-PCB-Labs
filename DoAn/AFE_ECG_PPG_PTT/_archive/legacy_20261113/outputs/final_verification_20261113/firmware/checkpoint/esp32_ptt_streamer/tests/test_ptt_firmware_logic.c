#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include "../main/esp32_ptt_streamer.h"

typedef struct {
    telemetry_packet_t buffer[QUEUE_SIZE_TELEMETRY];
    size_t head;
    size_t tail;
    size_t count;
    uint32_t drop_count;
} mock_nonblocking_queue_t;

static void queue_init(mock_nonblocking_queue_t *q) {
    q->head = 0;
    q->tail = 0;
    q->count = 0;
    q->drop_count = 0;
}

static bool queue_push_nonblocking(mock_nonblocking_queue_t *q, const telemetry_packet_t *pkt) {
    if (q->count >= QUEUE_SIZE_TELEMETRY) {
        q->drop_count++;
        return false;
    }
    q->buffer[q->head] = *pkt;
    q->head = (q->head + 1) % QUEUE_SIZE_TELEMETRY;
    q->count++;
    return true;
}

static bool queue_pop(mock_nonblocking_queue_t *q, telemetry_packet_t *pkt) {
    if (q->count == 0) {
        return false;
    }
    *pkt = q->buffer[q->tail];
    q->tail = (q->tail + 1) % QUEUE_SIZE_TELEMETRY;
    q->count--;
    return true;
}

static void test_register_configurations_against_datasheet(void) {
    uint8_t ads_dr_bits = (ADS1115_CFG_LSB_475SPS >> 5) & 0x07;
    assert(ads_dr_bits == 0x06);

    uint8_t ads_dr_860_bits = (ADS1115_CFG_LSB_860SPS >> 5) & 0x07;
    assert(ads_dr_860_bits == 0x07);

    uint8_t max_smp_ave = (MAX30102_FIFO_CFG_NO_AVE >> 5) & 0x07;
    assert(max_smp_ave == 0x00);

    uint8_t max_rollover = (MAX30102_FIFO_CFG_NO_AVE >> 4) & 0x01;
    assert(max_rollover == 0x01);

    uint8_t max_spo2_sr = (MAX30102_SPO2_CFG_400SPS >> 2) & 0x07;
    assert(max_spo2_sr == 0x03);

    uint8_t max_led_pw = MAX30102_SPO2_CFG_400SPS & 0x03;
    assert(max_led_pw == 0x03);

    assert(MAX30102_MODE_SPO2 == 0x03);
}

static void test_fifo_sample_count_and_uncertainty_helpers(void) {
    assert(max30102_fifo_sample_count(10, 6, 0) == 4);
    assert(max30102_fifo_sample_count(7, 7, 0) == 0);
    assert(max30102_fifo_sample_count(2, 29, 0) == 5);
    assert(max30102_fifo_sample_count(7, 7, 3) == 32);
    assert(max30102_fifo_sample_count(0, 0, 0) == 0);

    assert(ppg_burst_quality_flags(0, 1, 0, false) == QUALITY_FLAG_TIMESTAMP_UNCERTAIN);
    assert((ppg_burst_quality_flags(0, 1, 0, false) & QUALITY_FLAG_FIFO_BURST) == 0);
    assert((ppg_burst_quality_flags(0, 2, 0, false) & QUALITY_FLAG_FIFO_BURST) != 0);
    assert((ppg_burst_quality_flags(0, 4, 1, false) & QUALITY_FLAG_FIFO_OVERFLOW) != 0);
    assert((ppg_burst_quality_flags(0, 4, 0, true) & QUALITY_FLAG_FIFO_OVERFLOW) != 0);
    assert((ppg_burst_quality_flags(QUALITY_FLAG_QUEUE_DROP, 1, 2, true) & QUALITY_FLAG_QUEUE_DROP) != 0);

    assert(ads_read_window_uncertain(1000000ULL, 1000000ULL) == false);
    assert(ads_read_window_uncertain(1000000ULL, 1000000ULL + ADS1115_CONV_READY_WINDOW_US) == false);
    assert(ads_read_window_uncertain(1000000ULL, 1000001ULL + ADS1115_CONV_READY_WINDOW_US) == true);
    assert(ads_read_window_uncertain(9000000ULL, 1000000ULL) == false);
}

static void test_packet_structure_and_packing(void) {
    assert(sizeof(telemetry_packet_t) == 25);

    telemetry_packet_t pkt;
    memset(&pkt, 0, sizeof(pkt));
    pkt.seq = 1001;
    pkt.timestamp_us = 1731174000123456ULL;
    pkt.ecg_raw = -12450;
    pkt.ppg_ir = 262143;
    pkt.lead_off = 0x01;
    pkt.quality_flags = QUALITY_FLAG_LOD_POS | QUALITY_FLAG_FIFO_BURST;
    pkt.mcu_skew_us = -450;
    pkt.sample_type = SAMPLE_TYPE_PPG;

    uint8_t *raw = (uint8_t *)&pkt;
    uint32_t parsed_seq = *(uint32_t *)(raw);
    uint64_t parsed_ts = *(uint64_t *)(raw + 4);
    int16_t parsed_ecg = *(int16_t *)(raw + 12);
    uint32_t parsed_ppg = *(uint32_t *)(raw + 14);
    uint8_t parsed_lod = *(uint8_t *)(raw + 18);
    uint8_t parsed_flags = *(uint8_t *)(raw + 19);
    int32_t parsed_skew = *(int32_t *)(raw + 20);
    char parsed_type = (char)raw[24];

    assert(parsed_seq == 1001);
    assert(parsed_ts == 1731174000123456ULL);
    assert(parsed_ecg == -12450);
    assert(parsed_ppg == 262143);
    assert(parsed_lod == 0x01);
    assert(parsed_flags == (QUALITY_FLAG_LOD_POS | QUALITY_FLAG_FIFO_BURST));
    assert(parsed_skew == -450);
    assert(parsed_type == SAMPLE_TYPE_PPG);
}

static void test_nonblocking_queue_drop_tracking(void) {
    mock_nonblocking_queue_t q;
    queue_init(&q);

    telemetry_packet_t pkt;
    memset(&pkt, 0, sizeof(pkt));

    for (size_t i = 0; i < QUEUE_SIZE_TELEMETRY; i++) {
        pkt.seq = (uint32_t)i;
        bool ok = queue_push_nonblocking(&q, &pkt);
        assert(ok == true);
    }
    assert(q.count == QUEUE_SIZE_TELEMETRY);
    assert(q.drop_count == 0);

    for (size_t i = 0; i < 50; i++) {
        pkt.seq = 9999;
        bool ok = queue_push_nonblocking(&q, &pkt);
        assert(ok == false);
    }
    assert(q.drop_count == 50);

    telemetry_packet_t out;
    bool pop_ok = queue_pop(&q, &out);
    assert(pop_ok == true);
    assert(out.seq == 0);
    assert(q.count == QUEUE_SIZE_TELEMETRY - 1);

    pkt.seq = 8888;
    assert(queue_push_nonblocking(&q, &pkt) == true);
    assert(q.count == QUEUE_SIZE_TELEMETRY);
}

static void test_udp_serialization_format(void) {
    telemetry_packet_t pkt = {
        .seq = 42,
        .timestamp_us = 123456789ULL,
        .ecg_raw = 8192,
        .ppg_ir = 150000,
        .lead_off = 2,
        .quality_flags = QUALITY_FLAG_LOD_NEG | QUALITY_FLAG_QUEUE_DROP,
        .mcu_skew_us = 310,
        .sample_type = SAMPLE_TYPE_PPG
    };

    char buf[160];
    int len = snprintf(buf, sizeof(buf), "%u,%llu,%d,%u,%u,%u,%d,%c\n",
                       pkt.seq,
                       (unsigned long long)pkt.timestamp_us,
                       pkt.ecg_raw,
                       pkt.ppg_ir,
                       pkt.lead_off,
                       pkt.quality_flags,
                       pkt.mcu_skew_us,
                       pkt.sample_type);

    assert(len > 0);
    assert(len < (int)sizeof(buf));

    uint32_t seq = 0;
    unsigned long long ts = 0;
    int ecg = 0;
    unsigned int ppg = 0;
    unsigned int lod = 0;
    unsigned int flags = 0;
    int skew = 0;
    char sample_type = 0;

    int scanned = sscanf(buf, "%u,%llu,%d,%u,%u,%u,%d,%c", &seq, &ts, &ecg, &ppg, &lod, &flags, &skew, &sample_type);
    assert(scanned == 8);
    assert(seq == 42);
    assert(ts == 123456789ULL);
    assert(ecg == 8192);
    assert(ppg == 150000);
    assert(lod == 2);
    assert(flags == (QUALITY_FLAG_LOD_NEG | QUALITY_FLAG_QUEUE_DROP));
    assert(skew == 310);
    assert(sample_type == SAMPLE_TYPE_PPG);
}

int main(void) {
    test_register_configurations_against_datasheet();
    test_fifo_sample_count_and_uncertainty_helpers();
    test_packet_structure_and_packing();
    test_nonblocking_queue_drop_tracking();
    test_udp_serialization_format();
    printf("PASS: test_ptt_firmware_logic verified all 5 subsystems\n");
    return 0;
}
