ESP32: SDA21 SCL22 I2C 400kHz. ADS1115 0x48 cont diff AIN0-AIN1 475SPS (DR=110b, 0xC0) ALERT27 ISR. MAX30102 0x57 SpO2 IR 400SPS (SPO2_SR=011b, 0x2F) 18-bit FIFO no decimation (SMP_AVE=000b, 0x1F) INT26 ISR. FIFO timing is not sample-accurate: the interrupt can remain latched while further samples arrive. Do not reconstruct precise timestamps by backdating from the queued IRQ. Non-blocking FreeRTOS queues with drop counters. UDP stream over Wi-Fi STA Core 1 priority 5. CSV packet mới: seq,ts_us,ecg,ppg_ir,lod,quality_flags,mcu_skew_us,sample_type. sample_type E là ECG, P là một mẫu IR PPG; trường kênh còn lại bằng 0. Host vẫn đọc được packet 7 trường cũ. Timestamp PPG là thời điểm sự kiện IRQ hoặc poll, không phải thời điểm mẫu đã hiệu chuẩn; bit7 đánh dấu TIMESTAMP_UNCERTAIN cho PPG, bit6 chỉ đánh dấu FIFO_BURST khi đọc hơn một mẫu. Không dùng skew hoặc timestamp này để nghiệm thu PAT. Host simulation test in tests/test_ptt_firmware_logic.c. Note: Timestamps are based on MCU internal esp_timer. Hardware synchronization and end-to-end timing precision require physical oscilloscope and logic analyzer measurement on real hardware.

Cập nhật 13/11/2026: mọi mẫu IR đọc được từ FIFO được enqueue riêng; lỗi I²C phát packet lỗi, queue-drop chỉ được xác nhận sau enqueue thành công. GPIO MAX INT thấp được kiểm lại định kỳ để phục hồi khi mất cạnh ngắt. ADS đo thời điểm hoàn thành đọc I²C rồi đánh dấu chưa chắc chắn khi vượt cửa sổ bảo thủ 1900 µs; không bảo đảm nhận đúng mọi conversion khi task bị trễ.

Build ESP-IDF v5.5 cho target `esp32` đã PASS ngày 13/11/2026, gồm compile và link ứng dụng/bootloader/partition table. Đã sửa định dạng số nguyên bằng PRIu32/PRId32 để đúng Xtensa ABI. Ứng dụng 776160 byte, còn 26% app partition. Log build và lần build kiểm lại nằm trong `outputs/final_verification_20261113/firmware/logs/`. Bộ ảnh nạp kèm offsets nằm tại `outputs/final_verification_20261113/firmware/flash/`. Chưa nạp lên ESP32 hoặc thử bo thật; build PASS không chứng minh timing cảm biến hay an toàn.

Toolchain tạm: ESP-IDF tại `/tmp/opencode/esp_extract/esp-idf`, `IDF_TOOLS_PATH=/tmp/opencode/esp_tools`; có thể mất sau khi dọn `/tmp`. Các lệnh dưới đây kiểm helper C, enqueue thực trong host harness, parser và DSP mô phỏng.

```bash
make -B -C DoAn/AFE_ECG_PPG_PTT/firmware/esp32_ptt_streamer test
```

```bash
python3 DoAn/AFE_ECG_PPG_PTT/firmware/esp32_ptt_streamer/tests/check_acquisition_regression.py
```

```bash
python3 DoAn/AFE_ECG_PPG_PTT/software/test_protocol_regression.py
```

Bản biên dịch là `esp32_ptt_streamer/main/main.c`; bản `esp32_ptt_streamer/main.c` được giữ byte-identical để tránh nhầm nguồn. Không gắn điện cực lên người dựa vào host test hoặc CAD sạch.
