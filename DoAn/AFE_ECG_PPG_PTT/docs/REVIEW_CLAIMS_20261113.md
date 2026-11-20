# Đối chiếu nhận xét trước chế tạo

Phạm vi: PCB 92 × 70 mm, một ECG ba điện cực và một PPG. Phân biệt bằng chứng CAD với giả thuyết nhiễu và điều kiện chọn linh kiện. Chưa đánh giá an toàn tiếp xúc cơ thể.

| Nhận xét | Kết quả đối chiếu | Xử lý |
|---|---|---|
| Thiếu return GND gần U1/C4/C11 | Via GND gần nhất cách U1.16 12,790 mm, C4.2 11,724 mm, C11.2 7,898 mm trước sửa | Thử return cục bộ ngoài pad, kiểm DRC và plane; không nhận hết nhiễu nếu chưa đo |
| Dòng LED buộc chạy nối tiếp qua GND U1 | Chưa chứng minh: J3.7 xuyên lỗ và GND zone tạo nhánh song song | Không suy dòng hồi chỉ từ chuỗi track F.Cu |
| Carrier phải dẫn dòng Wi-Fi 300–500 mA | Không đúng cho mọi cấu hình; DevKit có regulator riêng khi cấp USB, J2.1 cấp carrier | Xác định hướng cấp và tải thực trước tính sụt áp; không cấp nhiều nguồn cùng lúc |
| Mọi track 0,2 mm là không đạt | Trước sửa các rail đúng rộng 0,2 mm; chiều dài tổng nhánh không phải đường tải duy nhất | Cải thiện nhánh cấp J3 khi không phá clearance; kiểm sụt áp/nhiễu bench |
| C10 danh định 1 µF đủ | Chưa đủ bảo đảm điện dung hiệu dụng | MCP1700 cần tối thiểu 1 µF, ESR 0–2 Ω; chốt MPN theo bias/tolerance/nhiệt độ |
| AD8232 VOH_min = 0,8×VS | Chưa có căn cứ trong bảng AD8232 đã tra; 0,8×VDD xuất hiện ở VOH ESP32 | Không đổi rail 3 V hoặc gắn pull-up tùy tiện; worst-case LOD vẫn cần xác nhận |
| Phải chia AGND/DGND và nối 0 Ω | Không phải quy tắc bắt buộc cho bo này | Giữ GND chung, cải thiện đường hồi và phân vùng dòng |
| Track dưới exposed pad chắc chắn gây cầu hàn | Chưa đủ căn cứ; phải xét mask/paste/land pattern và quy trình lắp | Không khoan via hở trong pad; xem mask/paste với xưởng |
| J3 cắm được mọi breakout MAX30102 | Sai; chưa chốt module/pinout, J3/J2 chỉ cách tâm 5 mm | Dùng PPG rời qua dây, kiểm nguồn, pull-up, INT, pinout và chống kéo |
| ZIP bị cắt/hỏng vì có build/binary | CRC các ZIP đã kiểm không thấy hỏng; trình xem bị cắt không chứng minh ZIP hỏng | Tạo gói nhẹ allowlist, Gerber-only phẳng; không kèm build/private/agent data |
| Kích thước report chứng minh ERC/DRC lỗi hiện hành | Không hợp lệ; report lịch sử có thể thuộc PCB khác | Gắn kết quả vào đúng hash/revision, cách ly artifact cũ |
| Nội suy burst PPG 2.500 µs đủ mở PAT | Không chứng minh timing IRQ/FIFO/I²C và sai số đồng hồ | Giữ TIMESTAMP_UNCERTAIN và khóa PAT live đến hiệu chuẩn |
| Firmware công khai đã build mới | Chưa; build ESP-IDF v5.5 trước đây là trước tách cấu hình mạng public | Bản public cần cấu hình local và build lại; không nhận build cũ là bằng chứng mới |
| Dùng pin là đủ để đo người | Sai | Chỉ thử bench bằng tín hiệu giả lập; cần đánh giá an toàn phù hợp |

## Cổng còn mở

C10 và passive MPN, module ESP32/MAX30102 đúng mẫu, plug/vỏ/đỡ cơ khí, CAM/stencil/assembly, đo rail/transient/nhiễu/đáp ứng analog, timing và an toàn cơ thể chưa được xác nhận chỉ bằng CAD. Không tự tạo BOM/CPL PCBA đã duyệt hoặc tuyên bố sản phẩm đạt.

## Nguồn

- [AD8232 Rev. D, bảng logic và layout](https://www.analog.com/media/en/technical-documentation/data-sheets/AD8232.pdf)
- [MCP1700 DS20001826E, §5.2](https://ww1.microchip.com/downloads/en/DeviceDoc/MCP1700-Low-Quiescent-Current-LDO-20001826E.pdf)
- [ESP32 datasheet, DC characteristics](https://documentation.espressif.com/esp32_datasheet_en.pdf)
- [DevKitC V4 schematic, nguồn và header](https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_sch.pdf)
