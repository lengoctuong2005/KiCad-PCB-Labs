# Phần mềm thu nhận và phân tích ECG + PPG PAT

Bộ công cụ Python kiểm tra chất lượng gói telemetry từ firmware ESP32 và tính Pulse Arrival Time trên dữ liệu mô phỏng hoặc dữ liệu CSV đã hiệu chuẩn đồng bộ thời gian hai kênh. Dự án là mẫu thử nghiệm bench, không phải thiết bị y tế và không có cách ly an toàn điện IEC 60601-1.

## 1. Giới hạn đo lường và khóa PAT thời gian thực

PAT đo từ đỉnh R của ECG đến chân sóng xung PPG bao gồm Pre-Ejection Period của tim, không phải Pulse Transit Time thuần túy trên thành mạch.

Firmware `esp32_ptt_streamer` đọc ADC ADS1115 cho kênh ECG và đọc FIFO của MAX30102 cho kênh IR PPG, gắn nhãn thời gian theo `esp_timer_get_time()` tại thời điểm ngắt hoặc polling I2C. Do MAX30102 trả mẫu theo burst FIFO và chưa có hiệu chuẩn trễ nội suy đồng hồ quang học, firmware luôn bật bit 7 `TIMESTAMP_UNCERTAIN` trên mọi gói `P` và bật cờ này trên gói `E` khi thời gian đọc I2C vượt `1900 us`.

Vì thiếu nhãn thời gian phần cứng đã hiệu chuẩn cho từng mẫu PPG, chế độ `--udp` và `--file` trong `ptt_live_analyzer.py` bị khóa tính PAT: đầu ra JSON luôn đặt `"pat": null` và ghi thông báo `PAT disabled: firmware PPG sample timing, FIFO and I2C validity are unverified.` ra `stderr`. Chỉ hai nguồn sau chạy phân tích PAT:

- `--simulate`: sinh dữ liệu tổng hợp 500 Hz trong 12 giây với mảng thời gian ECG và PPG độc lập để kiểm thử thuật toán.
- `--timed-csv`: nạp tệp CSV có cột `ppg_timestamp_us` độc lập đã được kiểm chứng từ phép đo ngoài.

Nội suy tuyến tính lên lưới `1000 Hz` khi xử lý không tạo ra độ chính xác thời gian `1 ms` nếu thiếu chuẩn hóa thời gian đầu vào. Không áp dụng bù trễ mặc định `5.6 ms`; chỉ truyền `--ecg-relative-delay-ms` khi có số liệu đo thực nghiệm trễ tương đối giữa kênh ECG và PPG trên phần cứng thật.

## 2. Cấu hình lọc tương tự trên schematic hiện hành

Tầng lọc và khuếch đại ECG dùng AD8232 với các giá trị linh kiện thực tế trong `AFE_ECG_PPG_PTT.kicad_sch` và `docs/CALC.json`:

- LPF Sallen-Key bậc 2: `R11 = R12 = 1 MΩ`, `C5 = 1.5 nF` nối `SK_N1` với `AD_OUT`, `C6 = 10 nF` nối `OPAMP_P` với `REFOUT`.
- Khuếch đại tầng op-amp: `R13 = 100 kΩ`, `R14 = 1 MΩ`, hệ số khuếch đại danh định bằng `11`.
- Tần số cắt và hệ số phẩm chất lý tưởng của Sallen-Key: `f0 ≈ 41.09 Hz` và `Q ≈ 0.775`. Đây là trị số tính toán lý thuyết của khối LPF, chưa phải đáp ứng tần số đo thực tế toàn mạch.
- HPF theo AD8232 Figure 66: `C1 = C2 = 0.33 µF`, `R6 = R8 = 10 MΩ`, `R18 = 1.4 MΩ`.
- Điện trở nối tiếp đầu vào điện cực: `R1 = R2 = R3 = 360 kΩ` chỉ bảo vệ mạch khi thử bench, không thay thế cách ly y tế.

## 3. Giao thức gói tin UDP và CSV

Firmware xuất từng mẫu đơn lẻ dưới dạng chuỗi ASCII CSV 8 trường kết thúc bằng `\n`:

```text
seq,timestamp_us,ecg_raw,ppg_ir,lead_off,quality_flags,mcu_skew_us,sample_type
```

Quy ước từng trường trong `parse_packet()`:

| Trường | Kiểu và miền hợp lệ | Ý nghĩa |
| :--- | :--- | :--- |
| `seq` | Số nguyên không dấu 32 bit, `0..4294967295` | Bộ đếm thứ tự gói tăng liên tục |
| `timestamp_us` | Số nguyên không dấu 64 bit | Thời gian MCU tính bằng micro giây từ `esp_timer_get_time()` |
| `ecg_raw` | Số nguyên có dấu 16 bit, `-32768..32767` | Giá trị ADC ADS1115; bằng `0` trên gói `P` |
| `ppg_ir` | Số nguyên 18 bit, `0..262143` | Giá trị kênh IR từ FIFO MAX30102; bằng `0` trên gói `E` |
| `lead_off` | `0..3` | Bit 0 là `LOD+`, bit 1 là `LOD-` |
| `quality_flags` | `0..255` cho 8 trường, `0..127` cho 7 trường cũ | Mặt nạ bit cảnh báo chất lượng dữ liệu |
| `mcu_skew_us` | Số nguyên có dấu 32 bit | Độ lệch `last_ecg_ts - last_ppg_ts` trên gói `E`; bằng `0` trên gói `P` |
| `sample_type` | `E` hoặc `P` | `E` là mẫu ECG, `P` là một mẫu từ FIFO PPG |

Định dạng 7 trường cũ bỏ qua `sample_type` và mặc định hiểu là `'E'` vẫn được `parse_packet()` hỗ trợ để đọc log cũ. Mỗi mẫu lấy ra từ FIFO MAX30102 được gửi bằng một gói `P` riêng biệt, không nhân bản giá trị ECG cũ.

Ý nghĩa các bit trong `quality_flags` và kiểm tra lỗi ở `quality_error()`:

- Bit 0 với giá trị `1`: tuột điện cực dương `LOD+`.
- Bit 1 với giá trị `2`: tuột điện cực âm `LOD-`.
- Bit 2 với giá trị `4`: bão hòa tín hiệu; `quality_error()` cũng báo `saturation_or_contact` khi `|ecg_raw| >= 32700` hoặc gói có PPG nằm ngoài khoảng `101..261999`.
- Bit 3 với giá trị `8`: lỗi giao tiếp I2C, ánh xạ thành `i2c_error`.
- Bit 4 với giá trị `16`: tràn FIFO MAX30102, ánh xạ thành `fifo_overflow`.
- Bit 5 với giá trị `32`: rớt phần tử hàng đợi ngắt hoặc hàng đợi UDP trong firmware, ánh xạ thành `queue_drop`.
- Bit 6 với giá trị `64`: đọc nhiều hơn một mẫu trong một lần lấy FIFO MAX30102, ánh xạ thành `fifo_burst`.
- Bit 7 với giá trị `128`: `TIMESTAMP_UNCERTAIN`, ánh xạ thành `timestamp_uncertain`.
- Nếu không dính các bit trên nhưng `|sync_skew_us| > 2000`, gói bị đánh dấu `mcu_skew_large`.

## 4. Thuật toán xử lý trong `ptt_live_analyzer.py`

1. Chia đoạn hợp lệ tại `segments_for_analysis()`: yêu cầu `ppg_timestamp_us` khác `None`, suy ra `in_fs` từ trung vị chu kỳ giữa các gói liên tiếp, loại gói lỗi chất lượng và tách đoạn mới mỗi khi mất gói hoặc jitter lệch quá `35%` chu kỳ danh định. Đoạn dưới 4 giây bị bỏ qua.
2. Tái lấy mẫu và lọc số trong `analyze()`: nội suy tuyến tính ECG và PPG về lưới thời gian chung ở `target_fs`, mặc định `1000.0 Hz`, hợp lệ từ `200` đến `5000 Hz`. Lọc pha bằng `sosfiltfilt` với bộ lọc Butterworth bậc 2 dải thông `5 - 15 Hz` cho ECG và `0.5 - 8 Hz` cho PPG.
3. Phát hiện đỉnh R tại `detect_r_peaks()`: bình phương đạo hàm bậc 1 của ECG đã lọc, làm mượt bằng trung bình trượt cửa sổ `150 ms`, lấy ngưỡng `median + 0.25 * (P99.5 - median)` với khoảng cách tối thiểu `300 ms` giữa các đỉnh, rồi dò cực đại biên độ tuyệt đối trong bán kính `100 ms`.
4. Tìm chân sóng PPG tại `tangent_foot()`: tìm đỉnh tâm thu PPG trong cửa sổ từ `r_index + 80 ms` đến trước `min(r_index + 500 ms, r_next)`, xác định đáy tâm trương nhỏ nhất trong `300 ms` trước đỉnh đó, sau đó lấy giao điểm giữa tiếp tuyến tại điểm có độ dốc dương lớn nhất với mức đáy tâm trương.
5. Kiểm tra cửa sổ sinh lý: loại bỏ nhát đập ở `0.5 s` đầu và cuối đoạn, loại chân sóng không tăng đơn điệu theo nhịp, và chỉ nhận nhịp có `120 ms <= pat_raw_ms <= 450 ms`.

## 5. Cài đặt và lệnh sử dụng

Cài đặt thư viện Python từ thư mục gốc repository:

```bash
pip install -r DoAn/AFE_ECG_PPG_PTT/software/requirements.txt
```

Các tùy chọn dòng lệnh của `DoAn/AFE_ECG_PPG_PTT/software/ptt_live_analyzer.py`:

- Nguồn dữ liệu bắt buộc chọn một: `--simulate`, `--timed-csv PATH`, `--udp [PORT]`, hoặc `--file PATH`.
- `--bind IP`: địa chỉ IP bind khi nhận UDP, mặc định `0.0.0.0`.
- `--duration SECONDS`: thời gian thu gói UDP tính bằng giây, mặc định `10.0`.
- `--target-fs HZ`: tần số lưới nội suy dùng cho `analyze()`, mặc định `1000.0`.
- `--ecg-relative-delay-ms MS`: độ trễ hiệu chuẩn ECG trừ PPG cộng thêm vào `pat_raw_ms` để ra `pat_corrected_ms`.
- `--live`: hiển thị đồ thị sóng ECG và PPG thời gian thực qua `matplotlib` khi chạy `--udp`; PAT vẫn bị tắt.

Ví dụ chạy từ thư mục gốc repository:

```bash
python3 DoAn/AFE_ECG_PPG_PTT/software/ptt_live_analyzer.py --simulate
```

```bash
python3 DoAn/AFE_ECG_PPG_PTT/software/ptt_live_analyzer.py --timed-csv validated_samples.csv --target-fs 1000 --ecg-relative-delay-ms 4.2
```

```bash
python3 DoAn/AFE_ECG_PPG_PTT/software/ptt_live_analyzer.py --udp 5005 --bind 0.0.0.0 --duration 30 --live
```

```bash
python3 DoAn/AFE_ECG_PPG_PTT/software/ptt_live_analyzer.py --file recorded_telemetry.csv
```

Chạy kiểm thử tự động cho bộ phân tích giao thức và pipeline DSP:

```bash
python3 DoAn/AFE_ECG_PPG_PTT/software/test_protocol_regression.py
python3 tests/test_dsp_ptt_pipeline.py
```
