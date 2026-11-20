# PCB thu gọn 100 × 70 mm, 13/11/2026

## Bản hiện hành

PCB tại gốc project đã cập nhật từ ứng viên đã kiểm. Diện tích giảm từ 8.000 xuống 7.000 mm², tức 12,5%. Schematic và project rules không đổi. Bản nguồn trước sửa được giữ trong `baseline/`; `candidate/` chứa nguồn ứng viên. Không dùng các Gerber 100 × 80 mm của gói trước cho PCB hiện hành.

- J1: (14; 5,55) mm, góc 0°, hướng cắm ra phía −Y. Mặt miệng F.Fab ở y=0,35 mm, sát cạnh trên. Reference J1 nằm trên bo tại (20; 8) mm.
- H3: (5; 65), H4: (62; 65) mm. H1/H2 giữ nguyên. Bốn lỗ M3 vẫn có pad GND.
- U1/U2/U3, linh kiện analog và J2/J3 giữ nguyên vị trí. Sửa routing chỉ trên LA_IN, RA_IN, RL_E và GND.
- Hai vùng cấm anten x=68…100, y=0…12 mm trên F.Cu/B.Cu giữ nguyên; B.Cu GND zone thu về y=69 mm và refill.

## Kết quả kiểm

- KiCad 10.0.8: DRC 0, unrouted 0, schematic parity 0; mọi severity, ignored_checks rỗng.
- ERC 0; hai kiểm không áp dụng vẫn được ghi rõ trong `erc.rpt`: SPICE và global label xuất hiện một lần.
- Netlist: 46 footprint, 151 node, đúng value/footprint/symbol path/pad-net.
- Geometry: outline 100 × 70 mm, vị trí/hướng jack, lỗ gá, keepout cả hai lớp và chữ cảnh báo PASS.
- Drill: 86 lỗ/slot khớp PCB trong 0,0011 mm, gồm 34 via 0,3 mm, 48 lỗ/slot dùng tool 1 mm và 4 lỗ M3 3,2 mm.
- Gerber/drill top, bottom, mask và paste render bằng gerbv 2.10.0. Viewer không hiểu thuộc tính metadata X2 TF/TA/TO/TD; còn cảnh báo nhận diện RS-274D trên lớp silk/paste đáy rỗng và mask chỉ dùng region không khai báo aperture. Đã xem hình mask có đủ vùng mở pad; chưa xác nhận toàn bộ ngữ nghĩa mask bằng CAM của xưởng. Giữ nguyên dữ liệu gốc và toàn bộ diagnostics tại `gerbv_logs.json`. Không coi exit code 0 là chứng nhận CAM của xưởng.
- `Assembly_1to1.pdf` là bản vẽ 1:1; in ở 100%, không fit page, rồi đối chiếu mẫu module/jack thực.

## Nội dung

`gerbers/` là dữ liệu copper, mask, silk, paste, outline và drill mới. `BOM.csv`, `placement_mm.csv`, `Schematic.pdf`, `PCB_Layout.pdf`, `Assembly_1to1.pdf`, `PCB_Top.png`, `PCB_Bottom.png` và `CAM_*.png` thuộc bản thu gọn. `manifest.json` ghi hash và giới hạn; ZIP chỉ chứa dữ liệu chế tạo và hướng dẫn, không phải lệnh đặt gia công.

## Chưa xác minh

Chưa thử jack/plug/vỏ, mẫu ESP32/MAX30102, MPN passive, CAM/assembly với xưởng, đáp ứng analog, RF hoặc timing thực tế. Chưa nạp firmware hoặc chạy hardware trong lần sửa layout này. Thu gọn diện tích không bảo đảm giảm giá nếu chưa báo giá. Không dùng trên người; DRC sạch hoặc dùng pin không thay thế đánh giá an toàn. Chưa phát hành sản phẩm và chưa push bản sửa này lên GitHub.
