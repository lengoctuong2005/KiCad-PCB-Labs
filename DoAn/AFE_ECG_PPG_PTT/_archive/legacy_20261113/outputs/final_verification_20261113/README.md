# AFE ECG + PPG PAT: bản kiểm cuối trên máy, 13/11/2026

## Kết quả đã xác minh

- Nguồn chính: `../../AFE_ECG_PPG_PTT.kicad_sch`, `.kicad_pcb`, `.kicad_pro` và thư viện trong `../../libs/`.
- KiCad 10.0.8: ERC 0, DRC 0, unrouted 0, schematic parity 0. DRC `ignored_checks` rỗng. ERC giữ hai loại không áp dụng: SPICE và global label xuất hiện một lần. Không có exclusion che lỗi.
- Đã siết min clearance 0.2 mm, min silk clearance 0.1 mm, solder-mask web 0.1 mm; bật lại missing-courtyard và các check PCB trước đây bỏ qua. Di chuyển chữ U1 để không chen R13/R14.
- Gerber thực trong `gerbers/` được render bằng gerbv 2.10.0: copper hai mặt, mask, silk, paste, outline và drill. Xem ảnh cùng lệnh/log trong `gerber/`. Viewer không hiểu metadata X2 TF/TA/TO/TD, không ghi nhận lỗi hình học khác; không bỏ thuộc tính khỏi gói gốc để làm im log.
- `tests/check_fabrication_drills.py`: 86 lỗ/slot khớp vị trí, đường kính, hướng slot và loại mạ với PCB trong dung sai 0.0011 mm. Test âm dịch một lỗ 0.5 mm bị từ chối.
- BOM 46 reference, placement 35 reference, đơn vị mm. H1–H4 và TP1–TP7 là phần không đặt máy. PosY theo quy ước KiCad, không tự đổi dấu khi giao nhà lắp.
- Build ESP-IDF v5.5, target `esp32`: compile/link PASS, ứng dụng 776160 byte, 26% app partition còn trống. Lần build độc lập PASS: `firmware/logs/07_independent_build.log`. Đã sửa format số nguyên đúng Xtensa ABI bằng PRIu32/PRId32.
- Test C build mới, enqueue khi queue đầy, protocol cũ/mới và DSP mô phỏng PASS. Build không thay thế chạy trên silicon.

## File dùng đúng mục đích

- `gerbers/`, `BOM.csv`, `placement_mm.csv`, `Schematic.pdf`, `PCB_Layout.pdf`, `PCB_Top.png`: dữ liệu CAD mới nhất.
- `firmware/flash/`: ảnh nạp ESP32 và `flasher_args.json` sinh từ build thật. Offsets: bootloader 0x1000, partition 0x8000, app 0x10000. Không dùng app.bin đơn lẻ để thay bootloader/partition chưa xác nhận.
- Firmware dùng cấu hình mạng mẫu, phải cấu hình đúng môi trường rồi build lại trước khi dùng. Không công bố firmware nhị phân có cấu hình mạng riêng. Toolchain tạm trong `/tmp/opencode` có thể bị dọn sau phiên.
- Thư mục `../repair_20261112/` là snapshot cũ để truy vết, không phải bộ xuất mới nhất sau sửa silkscreen/rules/firmware.

## Hợp đồng module và giới hạn còn lại

J2 được thiết kế theo Espressif ESP32-DevKitC V4, 38 chân, WROOM-32E, hai hàng cách 25.4 mm. J3 pin 1–7 là VIN 3.3 V, SCL, SDA, INT, RD không dùng, IRD không dùng, GND. R16/R17 kéo bus về 3.3 V; module phải có nguồn/level-shift/INT phù hợp. Không bảo đảm mọi breakout MAX30102 hoặc board ESP32 clone tương thích. Không cắm module chưa xác nhận pinout vào header chỉ theo hình ảnh bán hàng.

AD8232 LOD 2.8 V sang ESP32 có margin danh định nhưng VOH min trường hợp xấu chưa được bảo đảm bằng dữ liệu hiện có. ADS1115 là delta-sigma, không dùng mô hình SAR để kết luận lỗi settling. C9 là tụ đầu vào LDO +3V3; C10 là tụ đầu ra +VS_A. C10 cần MPN với điện dung hiệu dụng tối thiểu 1 µF và ESR 0–2 Ω theo MCP1700 ở điều kiện sử dụng.

Chưa có mẫu module/cáp thực, in 1:1 đặt thử, MPN đầy đủ của passive, phê duyệt rotation/stencil/xưởng hoặc báo giá. Do đó chưa ký duyệt lắp ráp tự động hay hứa cắm vào chạy. Có thể dùng hồ sơ để review và chuẩn bị prototype; chỉ phát hành đặt bo khi phần cơ khí/interface và yêu cầu nhà gia công đã xác nhận.

Chưa nạp lên ESP32, cấp nguồn bo, đo đáp ứng analog, CMRR, timing, FIFO/IRQ hoặc hiệu năng truyền. PAT live vẫn khóa vì timestamp PPG chưa hiệu chuẩn. Thử đầu tiên bằng nguồn tín hiệu giả lập phù hợp, không dùng người làm tải thử. LDO không cách ly; pin và DRC sạch không chứng minh an toàn tiếp xúc cơ thể.

## Nguồn kỹ thuật

- AD8232 Rev. D: https://www.analog.com/media/en/technical-documentation/data-sheets/AD8232.pdf
- ADS1115: https://www.ti.com/lit/ds/symlink/ads1115.pdf
- MCP1700 DS20001826E: https://ww1.microchip.com/downloads/en/DeviceDoc/MCP1700-Low-Quiescent-Current-LDO-20001826E.pdf
- DevKitC V4: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- ESP32 datasheet: https://documentation.espressif.com/esp32_datasheet_en.pdf
