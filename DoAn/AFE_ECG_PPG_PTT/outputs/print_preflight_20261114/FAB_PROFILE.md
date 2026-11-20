# Profile kiểm PCB trần, cập nhật ngày 18/11/2026

Profile tham chiếu: [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities). Đây là đối chiếu bảng năng lực công khai, không phải báo giá, xác nhận đơn hàng hoặc phê duyệt CAM. Nếu chọn xưởng khác phải đối chiếu lại.

## Cấu hình đề xuất cho prototype

PCB trần 2 lớp FR-4, 92 x 70 mm, dày danh định 1,6 mm, copper thành phẩm 1 oz, soldermask xanh, silkscreen trắng, outline routed không V-score. Đề xuất ENIG để thuận lợi mặt phẳng hàn IC LFCSP/VSSOP pitch 0,5 mm; chưa có báo giá nên không cam kết ngân sách. Không đặt PCBA tự động theo BOM/CPL hiện tại. Stencil mặt trên là lựa chọn lắp cần thỏa thuận độ dày và khẩu độ mở với người hàn hoặc xưởng.

## Đối chiếu

| Mục | Bảng năng lực tham chiếu | Thiết kế sau kiểm ngày 18/11/2026 |
|---|---|---|
| 1 oz track/space | 0,10/0,10 mm cho 1 đến 2 lớp | Track >= 0,20 mm tại chân IC, trunk `+3V3`/`+VS_A` 0,40 mm, nhánh `J2.1-J3.1` 0,50 mm; clearance 0,20 mm, vùng phủ `B.Cu` 0,25 mm |
| Drill | Bảng hỗ trợ nhỏ hơn 0,30 mm, tùy chi phí/quy trình | Via 0,60/0,30 mm, 38 via |
| PTH annular ring 1 oz hai lớp | Đề xuất 0,25 mm, tối thiểu tuyệt đối 0,18 mm | Pad THT đạt từ 0,35 mm; vành via 0,15 mm theo mục via riêng |
| Plated slot | Rộng >= 0,5 mm, dài >= 2 x rộng | Jack có 3 slot danh định 2 x 1 mm, ở ranh tỷ lệ 2:1; yêu cầu CAM xác nhận slot/PTH |
| Copper tới routed edge | >= 0,20 mm | Rule dự án 0,50 mm |
| Mask expansion | Cho phép 1:1; khoảng tới trace lân cận >= 0,09 mm | Expansion 0; cần xem trực tiếp lớp mask trong preview CAM |
| Mask bridge xanh 1 oz | 0,10 mm | Rule web 0,10 mm |
| Legend height/line/pad distance | 1,0 mm / 0,15 mm / 0,15 mm | Text >= 1,0/0,15 mm, graphic >= 0,15 mm; kiểm profile tạm `min_silk_clearance` 0,15 mm đạt 0 lỗi |
| Thermal spoke vùng phủ đồng | Đảm bảo dẫn nhiệt và hàn đủ cầu | Vùng phủ `GND` trên `B.Cu` dùng khoảng hở 0,25 mm, cầu nhiệt 0,40 mm, 0 lỗi `starved_thermal` |
| Board size/thickness | Hỗ trợ 92 x 70 mm, 1,6 mm trong dải công khai | Cấu hình này không đòi panel HDI hay microvia |

Không chọn plugged/filled via chỉ vì CAD tented; tenting, plugging và filled-capped khác nhau. Yêu cầu xưởng giữ mask theo Gerber, review via gần pad và vùng pin 1/EP.

## Xác nhận với xưởng trước thanh toán

- Preview nhận đúng 92 x 70 mm, 2 lớp và outline kín.
- Có 90 feature khoan/slot: 38 via 0,3 mm, 48 lỗ/slot tool 1 mm gồm 3 slot J1, 4 lỗ M3 3,2 mm có mạ. File NPTH rỗng có chủ ý.
- Giữ ba slot J1 đúng hướng, đúng đơn vị và origin; không chuyển lỗ M3 thành NPTH khi chưa chấp thuận.
- Review mask/EP/paste/legend và tenting; không thay net, không xóa đồng hoặc khoan theo đề xuất CAM mà chưa kiểm lại.
- Bare-board electrical test theo netlist và phạm vi xưởng xác nhận.

Giá, thời gian giao hàng, số lượng, lớp phủ cuối cùng và khả năng lắp phải xem tại đơn hàng thực. Gói chỉ để gửi review chế tạo prototype, không chứng minh an toàn tiếp xúc cơ thể hay mạch hoạt động.
