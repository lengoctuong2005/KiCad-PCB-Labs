# Hướng dẫn đặt PCB, mua linh kiện, hàn lắp và nghiệm thu bench

Tài liệu hướng dẫn quy trình khép kín cho phiên bản bo mạch 92 x 70 mm cập nhật ngày 18/11/2026. Mọi bước thử nghiệm chỉ dùng nguồn tín hiệu giả lập trên bàn thí nghiệm. Hệ thống không có cách ly an toàn điện IEC 60601-1 và tuyệt đối `NO HUMAN CONNECTION`.

## 1. Đặt gia công PCB trần

1. Nạp duy nhất tệp `outputs/print_preflight_20261114/GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip` gồm đúng 11 tệp phẳng cấp gốc lên cổng báo giá xưởng. Không upload nguyên thư mục project hoặc các tệp cũ trong `_archive`.
2. Nhập thông số theo `outputs/print_preflight_20261114/DAT_PCB_TRAN.md` và `FAB_PROFILE.md`: kích thước 92 x 70 mm, 2 lớp FR-4 dày 1,6 mm, đồng 1 oz, soldermask xanh lá, silkscreen trắng, lớp phủ ENIG đề xuất cho chân pitch 0,5 mm, cắt viền routed đơn bo không V-score, via 0,60/0,30 mm tented theo mask không chọn filled hoặc plugged.
3. Mở xem bốn ảnh kiểm tra CAM trích xuất từ ZIP tại `outputs/print_preflight_20261114/`:
   - `CAM_top.png`: kiểm tra đồng `F.Cu`, nhãn `F.Silkscreen` và lỗ khoan `PTH`.
   - `CAM_bottom.png`: kiểm tra vùng phủ `GND` lớp `B.Cu` khoảng hở 0,25 mm, cầu nhiệt 0,40 mm và khe cách ly anten x = 60 đến 92 mm, y = 0 đến 12 mm.
   - `CAM_mask.png`: xác nhận 38/38 via được phủ kín soldermask trên cả hai mặt.
   - `CAM_paste.png`: xác nhận 4 cửa sổ kem hàn phân đoạn `1,05 x 1,05 mm` chiếm 65,2% diện tích exposed pad 2,6 x 2,6 mm của `U1`.
4. Kiểm tra trên bản preview CAM của xưởng đủ 90 feature khoan mạ gồm 3 slot oval `G85` 2,00 x 1,00 mm tại `J1` và 4 lỗ M3 3,2 mm nối GND; tệp `NPTH.drl` rỗng 0 lỗ là chủ ý. Nên đặt kèm stencil mặt trên nếu hàn khò `U1`.
5. In `outputs/print_preflight_20261114/Assembly_1to1.pdf` ở tỷ lệ 100% thực tế để ướm thử ESP32-DevKitC V4, hai thanh socket và jack 3,5 mm trước khi chốt đơn.

## 2. Mua linh kiện từ LCSC và kiểm tra module ngoài

Sử dụng trực tiếp `outputs/print_preflight_20261114/BOM_Orderable_LCSC.csv` gồm 20 dòng linh kiện LCSC cho 35 vị trí mua được. Các mục `H1..H4` và `TP1..TP7` mang nhãn `DNP` / `PCB_INTEGRATED` không cần mua.

- **Kiểm tra tồn kho khi thanh toán:** Các mã `U2` `C37593`, `C6/C7` `C82282`, `R16/R17` `C23162`, `R18` `C38070` trả về `stock=None` trên endpoint snapshot tra cứu dù có đơn giá hợp lệ; cần kiểm tra số lượng tồn kho trực tiếp trên trang LCSC trước khi đặt.
- **Jack 3,5 mm `J1`:** Sử dụng `SJ1-3533N` mã `C4992360` có tồn kho snapshot thấp 3 chiếc. Xác nhận khớp cơ khí 3 chân slot với footprint `SJ1-3533NG` trước khi đặt hàng.
- **Socket ESP32 `J2`:** Đặt số lượng `2` thanh socket cái `22850120ANG1SYA01` mã `C429947` loại 1x20P pitch 2,54 mm cho mỗi bo mạch, sau đó cắt bớt 1 chân mỗi thanh thành 1x19P.
- **Tụ ổn áp `C10`:** Chọn `TCC0603X7R105K500CT` mã `C5360793` thông số 1 uF 50 V X7R 0603 để giảm suy hao điện dung do DC bias tại rail 2,8 V và giữ ESR trong dải 0 đến 2 Ω theo yêu cầu của MCP1700-2802E.
- **Hai module mua rời ngoài `BOM_Orderable_LCSC.csv`:**
  1. **ESP32-DevKitC V4 38 chân:** Dùng bản có khoảng cách hai hàng chân 25,4 mm, kiểm tra thứ tự chân khớp bảng net của `J2` trước khi cắm.
  2. **Module MAX30102:** Phân biệt rõ mạch xanh MH-ET LIVE với các bo mạch đen phổ thông trên thị trường trước khi đấu dây ra `J3`. Kiểm tra thứ tự 7 chân thực tế phải nối đúng theo chân 1 đến chân 7 của `J3`: `+3V3`, `SCL`, `SDA`, `INT_MAX`, bỏ trống `RD`, bỏ trống `IRD`, `GND`. Kiểm tra đồng hồ và sơ đồ mạch của module để chắc chắn bus I2C và đường `INT` tương thích mức 3,3 V và không đấu kéo lên 1,8 V hoặc làm giảm quá thấp tổng trở kéo lên song song với `R16/R17` 4,7 kΩ trên bo chính.

## 3. Hàn lắp 5 giai đoạn và vệ sinh mạch

Mở `outputs/print_preflight_20261114/Interactive_Soldering_Guide.html` bằng trình duyệt bất kỳ ở chế độ offline để xem bản đồ pad 92 x 70 mm, vị trí chấm đỏ Pin 1 của `U1`, `U2`, `U3`, `J1`, `J2`, `J3` và bộ lọc từng bước:

1. **Giai đoạn 1 - Hàn IC SMD:** Quét kem hàn qua stencil phân đoạn 65,2% lên pad và EP của `U1` AD8232 LFCSP-20, khò theo hồ sơ nhiệt kem hàn bằng thermocouple. Tiếp tục hàn `U2` ADS1115 TSSOP-10 pitch 0,5 mm và `U3` MCP1700 SOT-23, soi kính lúp kiểm tra cầu hàn.
2. **Giai đoạn 2 - Hàn thụ động tương tự 0603:** Hàn `R1..R3`, các điện trở trở kháng cao `R4..R6`, `R8..R10`, `R18`, điện trở lọc/khuếch đại `R11..R15` và tụ `C1..C7`, `C11`.
3. **Giai đoạn 3 - Hàn thụ động nguồn và I2C 0603:** Hàn `C8`, `C9`, `C10`, cặp kéo lên I2C `R16`, `R17` và kéo lên ngắt `R19`.
4. **Giai đoạn 4 - Rửa IPA 99% và đo nguội chống chập:** Dùng cồn IPA 99% cùng bàn chải ESD cọ sạch hoàn toàn nhựa thông quanh các nút trở kháng cao 10 MΩ gồm `R4..R6`, `R8..R10`, `R18`, `C1`, `C2` và chân `U1`. Để khô hoàn toàn rồi đo nguội bằng đồng hồ vạn năng khi chưa cắm ESP32 hoặc MAX30102: `TP6` tới `TP7` > 10 kΩ, `TP5` tới `TP7` > 10 kΩ, `TP7` thông 0 Ω tới bốn lỗ `H1..H4`.
5. **Giai đoạn 5 - Hàn đầu nối xuyên lỗ và kiểm tra nguồn trên pad `TP1..TP7`:** Cắt hai thanh `J2` về 1x19P, hàn `J1`, `J2` và `J3` 1x7P. Cấp nguồn bench giới hạn dòng trước khi cắm IC ngoài và đo kiểm tra trên bảng `TP1..TP7`: `TP6` đạt ~3,30 V, `TP5` đạt ~2,80 V, `TP2` REFOUT đạt ~1,40 V, `TP1` ECG_OUT tĩnh gần 1,40 V, `TP3` và `TP4` gần 2,80 V khi hở điện cực.

## 4. Nạp firmware ESP32 và chẩn đoán qua Serial

Rút hoàn toàn cáp điện cực `J1` và bảo đảm không có điện cực nối người trước khi cắm cáp USB vào ESP32.

- **Nạp firmware Wi-Fi UDP chính:**
  - Chạy `bash DoAn/AFE_ECG_PPG_PTT/tools/flash_esp32.sh --prebuilt` để tự dò cổng `/dev/ttyUSB*` hoặc `/dev/ttyACM*` và nạp ba tệp nhị phân sẵn tại `firmware/esp32_ptt_streamer/build/` ở baud 460800.
  - Nếu cần chỉnh SSID, mật khẩu hoặc IP đích qua `idf.py menuconfig` từ `main/Kconfig.projbuild`, chạy `bash DoAn/AFE_ECG_PPG_PTT/tools/flash_esp32.sh --idf`.
- **Chẩn đoán nhanh trên bàn không cần Wi-Fi:**
  - Nạp sketch `DoAn/AFE_ECG_PPG_PTT/tools/esp32_bench_diag/esp32_bench_diag.ino` bằng Arduino IDE và mở Serial Monitor ở tốc độ 115200 baud.
  - Sketch thực hiện 4 bước tự kiểm tra lúc khởi động: dò `0x48` ADS1115 và `0x57` MAX30102 kiểm tra `PART_ID == 0x15`, cấu hình ADS1115 475 SPS kèm ngắt `GPIO27`, cấu hình MAX30102 400 SPS SpO2/IR kèm ngắt `GPIO26`, đọc điện áp `GPIO32` và `GPIO33` qua `analogReadMilliVolts()` so với ngưỡng `LOD_ADC_HIGH_THRESHOLD_MV = 1400 mV` nhằm khép kín biên độ logic từ rail 2,8 V sang ESP32 3,3 V.
  - Sau khi in các dòng `[SELF-TEST]`, sketch phát liên tục gói CSV 8 trường `E`/`P` tương thích trực tiếp với `software/ptt_live_analyzer.py --file`.

## 5. Nghiệm thu bench 7 bước và xác minh phần mềm

1. Chạy kiểm tra sẵn sàng trước khi đo:
   ```bash
   python3 DoAn/AFE_ECG_PPG_PTT/tools/bench_bringup_verify.py --preflight
   ```
   Tất cả 10 cổng kiểm tra từ nguồn KiCad, ZIP, khoan `PTH`/`NPTH`, tenting via và stencil `U1`, `BOM.csv`, firmware binaries, công cụ nạp/chẩn đoán, hướng dẫn hàn/lắp 1:1, DRC và mô phỏng DSP đều phải báo PASS.
2. Thực hiện 7 bước đo bench bằng máy phát tín hiệu ECG giả lập và mô hình quang học giả lập: kiểm nguồn 3,3 V / 2,8 V, kiểm I2C 400 kHz, kiểm `REFOUT` và băng thông lọc HPF/LPF lý tưởng `41,09 Hz`, kiểm hở điện cực `LOD_P`/`LOD_N` qua ngưỡng 1400 mV, kiểm sóng ECG trên Patient Simulator, kiểm sóng PPG trên Optical Phantom và kiểm định trễ đồng bộ.
3. Lưu log Serial CSV từ `esp32_bench_diag.ino` hoặc thu trực tiếp UDP cổng 5005 từ firmware chính để kiểm tra thông số truyền thông bằng `bench_bringup_verify.py`:
   ```bash
   python3 DoAn/AFE_ECG_PPG_PTT/tools/bench_bringup_verify.py --csv-check captured_bench.csv
   python3 DoAn/AFE_ECG_PPG_PTT/tools/bench_bringup_verify.py --udp-check --port 5005 --duration 10
   ```
4. Chạy `software/ptt_live_analyzer.py --file captured_bench.csv` hoặc `--udp 5005` để kiểm toán chất lượng gói tin. Mọi luồng thu trực tiếp từ firmware vẫn khóa tính PAT với `"pat": null` do cờ `TIMESTAMP_UNCERTAIN` cho tới khi bổ sung phép đo hiệu chuẩn thời gian giữa hai cảm biến.
