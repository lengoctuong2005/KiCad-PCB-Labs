# PCB 92 × 70 mm, sửa return GND cục bộ

Đây là bộ xuất hiện hành, chưa được xưởng duyệt CAM hoặc lắp ráp. ZIP `GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip` chỉ chứa đúng 11 file Gerber/drill cấp gốc. PDF/BOM/placement và `.gbrjob` nằm ngoài ZIP này.

## Thay đổi

Giữ nguyên schematic, net/value, footprint, vị trí linh kiện, outline 92 × 70 mm, nguồn analog 2,8 V và project rules. Một ECG ba điện cực qua J1; một PPG qua dây từ J3. Không thay firmware hoặc mở PAT live.

- Bốn via GND 0,6/0,3 mm, tented trên cả hai lớp, nằm ngoài pad: U1 tại (39,6;34,32), C4 tại (40,85;32), C11 tại (44,6;32,175), C10 tại (14,7;64) mm.
- U1.16 tới via có nhánh F.Cu 0,653 mm; C4.2 có nhánh 1,075 mm. Via C4 cách mép đồng pad khoảng 0,325 mm. C11/C10 nối via qua GND track có sẵn. Các via nối plane GND B.Cu đã refill; mặt trên không có GND zone tại đây.
- Nhánh J2.1→J3.1 dài 5 mm tăng rộng từ 0,2 lên 0,5 mm. Không xóa đường GND, không đi lại các trace analog khác.

## Kết quả

KiCad 10.0.8 DRC sau refill/save, mọi severity, all-track-errors và parity: 0 violation, 0 unconnected, 0 parity, ignored_checks rỗng. Review độc lập chạy lại đạt. ERC 0 với hai loại không áp dụng được ghi rõ: global label chỉ xuất hiện một lần và SPICE model.

Bảy kiểm CAD/package PASS. 46 footprint, 151 node; 90 lỗ/slot khớp Excellon trong 0,0011 mm, gồm 38 via 0,3 mm, 48 lỗ/slot tool 1 mm và 4 lỗ M3 3,2 mm. ZIP kiểm CRC, đúng member và byte khớp thư mục Gerber. DRC không chứng minh chức năng analog, không thay electrical test bo trần hoặc phê duyệt CAM xưởng.

Top/bottom/mask/paste được render độc lập bằng gerbv 2.10.0. Viewer không hiểu metadata X2 và có cảnh báo nhận diện lớp rỗng/mask chỉ dùng region; diagnostics giữ nguyên trong `gerbv_logs.json`. Không chỉnh Gerber để che warning. `Assembly_1to1.pdf` cần in 100%, không fit page, và so mẫu module/jack/socket thật.

## Chưa đóng các cổng

- MPN và effective capacitance C10: tối thiểu 1 µF, ESR 0–2 Ω theo MCP1700; voltage rating hoặc dung lượng danh định chưa đủ.
- Mức logic LOD ở rail 2,8 V: chưa có worst-case VOH bảo đảm theo điều kiện thực. Không tự đổi U3 3 V hoặc thêm pull-up.
- Module MAX30102, pinout, nguồn, level-shift, pull-up/INT, dây/strain relief; module ESP32/socket/vỏ và đỡ cơ khí.
- CAM/SMT, stencil, solder-mask registration/tenting, lắp thực, nhiễu/đáp ứng analog, RF, timing và an toàn tiếp xúc cơ thể.

Chỉ bench với tín hiệu giả lập. Dùng pin không chứng minh an toàn cho người. Firmware không đổi trong vòng sửa này; build ESP-IDF v5.5 trước đây là bằng chứng lịch sử trước tách cấu hình public, không phải build mới hay chạy phần cứng. Chưa commit/push bản sửa này.

## Truy xuất

`baseline/` giữ nguồn trước sửa; `candidate/` giữ ứng viên và report thử, không dùng report trial thay `drc.json` hiện hành. Các gói cũ nằm trong `../../_archive/legacy_20261113/`, mapping/hash tại INDEX.json. `manifest.json` ghi hash nguồn và output mới; không sửa hash lịch sử để nhận là revision hiện hành.
