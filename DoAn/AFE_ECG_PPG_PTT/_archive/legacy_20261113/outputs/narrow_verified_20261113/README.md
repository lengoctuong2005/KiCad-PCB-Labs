# PCB hiện hành 92 × 70 mm

Bản thu chiều ngang ngày 13/11/2026. Diện tích 6.440 mm²: giảm 8% từ 100 × 70 mm, giảm 19,5% từ 100 × 80 mm ban đầu. PCB gốc project đã cập nhật sang bản này; không dùng Gerber các revision trước cho bo hiện hành.

## Chức năng và bố trí

Một ECG, ba điện cực RA/LA/RL qua jack TRS J1; một MAX30102 PPG qua J3. Không thêm kênh, không đổi schematic, BOM hay firmware.

- J1 (14; 5,55) mm, hướng cắm −Y, miệng F.Fab cách mép trên 0,35 mm. J3 giữ tại (58; 16).
- ESP32 J2 dịch trái 8 mm tới (63; 16), vẫn giữ hai hàng socket cách nhau 25,4 mm. Khoảng giữa hai hàng dành cho DevKit, không phải diện tích trống.
- H2/H4 dịch tới (54; 6)/(54; 65). H1/H3 giữ nguyên.
- Hai keepout anten cùng dịch về x=60…92, y=0…12 mm, giữ đầy đủ cấm track/via/pad/fill/footprint trên F.Cu/B.Cu.
- Footprint cụm analog giữ nguyên. Fanout ECG_OUT/LOD_N/ALERT/+3V3 và GND được sửa để không chập sau thu khoảng cách. C8 có via GND tại (59,275; 46,1), cách pad GND 0,6 mm; chất lượng nhiễu/return cần đo bench.

## Bằng chứng

KiCad 10.0.8 sau refill, mọi severity và all-track-errors: DRC 0, unconnected 0, schematic parity 0, ignored_checks rỗng. Review độc lập chạy lại đạt cùng kết quả. ERC 0, giữ hai kiểm không áp dụng ghi trong report. Năm kiểm CAD PASS: analog, feedback, pad-net parity, geometry và drill. Có 86 lỗ/slot khớp file drill trong 0,0011 mm; số lượng via không đổi 34.

Đã xuất Gerber, drill, BOM, placement mm, PDF schematic/layout, bản lắp 1:1 và ảnh top/bottom. Render độc lập gerbv 2.10.0 có diagnostics X2 không hỗ trợ, nhận diện lớp đáy rỗng và mask dạng region không aperture; giữ nguyên diagnostics tại `gerbv_logs.json`. Không coi viewer exit 0 là phê duyệt CAM của xưởng.

## Revision và giới hạn

Nguồn 100 × 70 mm được giữ trong `../narrow_20261113/baseline/`. Ứng viên lỗi trực tiếp trong `../narrow_20261113/` không được dùng; nguồn đã sửa và kiểm tại `../narrow_20261113/gap_candidate/` khớp PCB gốc hiện hành.

Chưa xác nhận lắp DevKit/socket/module PPG, plug/jack/vỏ và khoảng thao tác vít bằng mẫu thực. Chưa kiểm RF, analog, timing hoặc chạy firmware trên phần cứng trong lần sửa này. Không gắn lên người; dùng pin hoặc DRC sạch không chứng minh an toàn. Chưa phê duyệt chế tạo/lắp ráp và chưa push GitHub.
