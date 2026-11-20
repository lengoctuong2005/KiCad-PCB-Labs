import re
import subprocess
import tempfile
from pathlib import Path

project = Path(__file__).resolve().parents[1]
source = (project / 'main/main.c').read_text()
start = source.index('static void enqueue_telemetry(')
stop = source.index('\nstatic void sensor_acquisition_task', start)
enqueue = source[start:stop]
read = source.index('esp_err_t ads_err = i2c_master_write_read_device', stop)
finished = source.index('uint64_t read_done_us =', read)
check = source.index('ads_read_window_uncertain(', finished)
assert read < finished < check
assert 'next_ppg_poll_us = now_us + 10000ULL' in source
assert 'if (have_event == pdTRUE)' in source
assert re.search(r'for \(int i = 0; i < num_samples; i\+\+\).*?enqueue_telemetry\(.*?SAMPLE_TYPE_PPG', source, re.S)
assert 'last_telemetry_drops' not in source
assert (project / 'main.c').read_text() == source
harness = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include "esp32_ptt_streamer.h"
#define pdTRUE 1
static volatile uint32_t s_isr_drop_count;
static volatile uint32_t s_telemetry_drop_count;
static uint32_t s_packet_sequence;
static uint32_t s_reported_isr_drops;
static uint32_t s_reported_telemetry_drops;
static int s_telemetry_queue;
static bool accept_packet;
static telemetry_packet_t delivered;
static int xQueueSend(int queue, const telemetry_packet_t *packet, int wait) {
    (void)queue;
    (void)wait;
    if (!accept_packet) return 0;
    delivered = *packet;
    return pdTRUE;
}
'''
harness += enqueue
harness += r'''
int main(void) {
    s_isr_drop_count = 3;
    enqueue_telemetry(10, 1, 0, 0, 0, 0, SAMPLE_TYPE_ECG);
    assert(s_reported_isr_drops == 0);
    assert(s_telemetry_drop_count == 1);
    accept_packet = true;
    enqueue_telemetry(20, 0, 120000, 0, 0, 0, SAMPLE_TYPE_PPG);
    assert(delivered.quality_flags & QUALITY_FLAG_QUEUE_DROP);
    assert(delivered.seq == 1);
    assert(s_reported_isr_drops == 3);
    assert(s_reported_telemetry_drops == 1);
    enqueue_telemetry(30, 1, 0, 0, 0, 0, SAMPLE_TYPE_ECG);
    assert(!(delivered.quality_flags & QUALITY_FLAG_QUEUE_DROP));
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='afe-enqueue-') as directory:
    test = Path(directory) / 'test.c'
    binary = Path(directory) / 'test'
    test.write_text(harness)
    subprocess.run(['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-pedantic', '-I', str(project / 'main'), str(test), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
print('PASS: actual enqueue keeps drop flags until accepted; ADS read completion ordering, PPG emission and duplicate source verified')
