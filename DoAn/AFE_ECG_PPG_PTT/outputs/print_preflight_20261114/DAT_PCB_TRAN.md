# Hướng dẫn gửi xưởng PCB trần

## 1. Chọn đúng dữ liệu

Upload duy nhất `GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip` trong thư mục này để xưởng xem CAM. Không upload nguyên project, candidate, baseline, archive, firmware/build hoặc ZIP cũ. Đây là yêu cầu PCB trần prototype, chưa đặt PCBA.

## 2. Thông số đề xuất

| Ô đặt hàng | Giá trị dự kiến |
|---|---|
| Dimensions | 92 × 70 mm |
| Layers / material | 2 / FR-4 |
| Thickness | 1,6 mm danh định |
| Copper | 1 oz |
| Mask / legend | Green / white |
| Finish | ENIG đề xuất cho pad phẳng; giá theo quote |
| Outline | Single routed board, không V-score |
| Vias | Through-hole 0,6/0,3 mm, tented theo mask; không via-in-pad fill/cap |
| Assembly | Không PCBA trong đơn này |
| Quantity | Chọn số mẫu theo nhu cầu và báo giá; chưa chốt |

Nếu đổi finish, copper weight, mask color hoặc xưởng, đối chiếu lại capabilities, mask/legend và quy trình hàn. Không suy cùng giá/giới hạn cho cấu hình khác.

## 3. Ghi chú có thể gửi CAM

> Two-layer FR-4 prototype, nominal outline 92.00 × 70.00 mm. Please verify three plated 2.00 × 1.00 mm oval slots at audio jack J1 and keep their orientation. Four 3.20 mm mounting holes are plated and connected to GND, not NPTH. Via drill is 0.30 mm, diameter 0.60 mm; tenting is specified by solder-mask data, no via-in-pad filled/capped process requested. Please review the LFCSP exposed-pad mask and fine-pitch mask dams, legend, and slot tolerances. Do not modify copper, connectivity, drill geometry, or mask openings without requesting approval. Please confirm bare-board electrical-test coverage before manufacture.

## 4. Trước thanh toán

- [ ] Preview nhận 92 × 70 mm, hai lớp, outline kín; top/bottom không bị mirror ngoài ý muốn.
- [ ] Slot J1 giữ đúng hướng; 90 feature khoan/slot và origin đúng, file NPTH rỗng được hiểu đúng.
- [ ] M3 vẫn có mạ; via tented không bị hiểu thành yêu cầu plugged/filled.
- [ ] Mask, chữ 1,0 mm/nét 0,15 mm và pad EP được xưởng chấp nhận, mọi thay đổi CAM được review.
- [ ] Đã in Assembly_1to1.pdf actual size 100% và so linh kiện thực; nếu chưa có mẫu, ghi rõ rủi ro fit trước khi quyết định đặt prototype.
- [ ] Quote xác nhận quantity, vật liệu, thickness, copper, finish, electrical test, phí stencil/vận chuyển/thuế và thời gian.

Không tự tích các ô chưa làm. File Gerber sạch cho phép gửi review/báo giá, không tự chứng minh phần cứng chạy. Chưa dùng trên người; không xem dùng pin là phê duyệt an toàn.

Nguồn profile tham chiếu: https://jlcpcb.com/capabilities/pcb-capabilities, tra ngày 14/11/2026.
