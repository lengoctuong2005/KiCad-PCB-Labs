# Bàn giao agent sửa đồ án AFE ECG + PPG

Ngày đối chiếu: 09/11/2026. Phạm vi: thiết kế nguyên lý, PCB, firmware và xử lý PAT cho đồ án thử nghiệm. Không phải thiết bị y tế, không có xác nhận an toàn khi gắn lên người.

## Kết luận và cảnh báo bắt buộc

**CHẶN GIA CÔNG VÀ ĐO TRÊN NGƯỜI.** Báo cáo và câu trả lời trước đây khẳng định thiết kế đã hoàn thành, DRC sạch, an toàn, đạt IEC, có sai số đồng bộ xác định và sẵn sàng sản xuất là không có cơ sở hoặc mâu thuẫn kết quả kiểm tra. Không sử dụng ZIP Gerber, BOM, CPL, báo cáo HTML/PDF hiện có làm hồ sơ sản xuất hoặc bằng chứng nghiệm thu. Không xóa chúng vì có thể cần truy vết.

KiCad CLI 10.0.8 kiểm tra bản hiện hành: **301 vi phạm DRC, 0 pad chưa kết nối, 170 mục kiểm tra parity footprint/schematic**. DRC có chập nguồn và giao cắt; 0 pad chưa nối không chứng minh mạch đúng. ERC báo 0 lỗi, 0 cảnh báo nhưng bỏ qua bốn loại kiểm tra. Bằng chứng đầy đủ: [DRC và parity](t2_evidence/restored_2301_drc_parity.rpt), [ERC](t2_evidence/restored_2301_erc.rpt), [đối soát phần cứng](DOI_SOAT_T2_VA_NGAN_CHAN_CHE_TAO.md). Kết quả được chạy lại với `--schematic-parity --refill-zones` cho cùng số lượng, không lưu lại bản PCB.

Dấu vân tay khi kiểm tra:
- Schematic: `edd23cfb42d701fc7c3a6ebeecefc38ae818f4879c78954d6cc2d66fe8608fc6`
- PCB: `b3a597be33eac75e4489f53e773f757bb06f57e85bef09bc47ff98174c6916e5`

Các tệp chưa được Git theo dõi. Trước khi sửa, sao chép nguyên trạng cả thư mục dự án sang vị trí riêng, kể cả thư viện, project, outputs và các snapshot trong `docs/t2_evidence/`. Không chạy generator có thể ghi đè bản gốc. Kiểm tra dấu vân tay trước khi sử dụng báo cáo vì dự án có thể thay đổi.

## 0. Quy tắc thực hiện

- [ ] Làm việc trên bản sao; đọc project, schematic, PCB, thư viện, báo cáo, firmware và phần mềm liên quan. Bảo toàn các thay đổi khác của người dùng.
- [ ] Phân loại lỗi: nghiêm trọng, cần sửa, cần đo kiểm, cải thiện. Mỗi lỗi ghi vị trí, bằng chứng, nguyên nhân, cách sửa và kết quả kiểm tra lại.
- [ ] Không tắt rule, xóa cảnh báo, đổi tên net hay thay giá trị hiển thị đơn thuần để tạo kết quả giả. Giải thích mọi ngoại lệ hợp lệ.
- [ ] Không khẳng định thiết bị hoạt động, an toàn, đạt chuẩn y tế hoặc đạt sai số đồng bộ nếu chưa có phép thử tương ứng. Ghi rõ thiết bị, linh kiện và công cụ chưa có.

## 1. Đồng bộ schematic và PCB, ưu tiên đầu tiên

- [ ] Xuất netlist mới từ schematic đang sử dụng; so sánh toàn bộ reference, giá trị, footprint, pad và kết nối từng chân với PCB. Không dựa vào netlist hay báo cáo cũ khi dấu băm khác.
- [ ] Làm rõ hai phiên bản khác nhau: U3 schematic `MCP1700-2802E`, PCB/BOM `MCP1700-3002E`; J2 schematic so với J2A/J2B trên PCB. Xác minh ánh xạ chân, không mặc định hai hàng header tương đương footprint 2×19.
- [ ] Rà C3–C6, C8–C9, R3–R4, R8, R10–R17; các phần tử PCB có thêm J1A, C12–C17, R7, R18–R20. C3 schematic có chức năng RLD, trong PCB/BOM được ghi cho LPF: không đổi nhãn để che khác biệt topology.
- [ ] Parity trước đây cho biết C3 khác với giá trị đọc trực tiếp từ schematic. Đối chiếu trực tiếp netlist mới, symbol cache và tệp project trước khi quyết định nguyên nhân.
- [ ] Đối chiếu datasheet và chức năng, sửa schematic trước, cập nhật PCB từ schematic rồi chạy parity. Báo cáo giải thích từng khác biệt còn lại.

## 2. Xác minh mạch nguyên lý

- [ ] AD8232: đối chiếu pinout symbol và footprint đúng mã, EP và dấu chân 1; kiểm tra IN+/IN−, RLD/RLDFB, REFIN, REFOUT, OUT, SDN, FR, LOD+/LOD−, SW, HPSENSE và IAOUT. Kiểm tra vòng phản hồi OPAMP_N, khả năng bão hòa và phục hồi sau rời điện cực.
- [ ] Đối chiếu topology Cardiac Monitor với hình tham khảo AD8232, tính lại tần số cắt, hệ số Q và gain từ kết nối cùng trị số thực tế. Mạng phản hồi hiện tại chưa chứng minh gain 11; không mặc định công thức cũ áp dụng được.
- [ ] Kiểm tra mạch lead-off, RLD, tham chiếu, decoupling và jack RA/LA/RL theo đúng cáp dự định dùng. Xét bảo vệ, dung sai và lỗi đơn trên mọi đường dòng đến người.
- [ ] ADS1115: đối chiếu AIN0/AIN1, giới hạn từng chân theo GND/VDD, PGA, tải OUT/REFOUT, RC đầu vào, địa chỉ, ALERT/RDY và pull-up. Xét cả trường hợp một IC chưa có nguồn. Không coi PGA FSR là giới hạn điện áp an toàn của chân.
- [ ] Nguồn: chốt đúng phiên bản U3, pinout và footprint theo datasheet nhà sản xuất; tính dropout worst-case, điện áp đầu vào tối thiểu, tải, nhiệt và tụ ổn định. LDO **không phải cách ly điện**.
- [ ] Kiểm tra tương thích điện áp và trình tự cấp nguồn giữa ESP32 3,3 V và AD8232 nguồn analog thấp hơn, nhất là FR và các GPIO. Không dùng absolute maximum làm điều kiện vận hành bình thường.
- [ ] Xác minh đúng mẫu ESP32 DevKit và MAX30102: kích thước, thứ tự chân, nguồn, mức I/O, chức năng RD/IRD và pull-up trên module. Tính tổng trở kéo I²C, kiểm tra GPIO khởi động.
- [ ] Chạy ERC sau khi sửa, ghi phiên bản KiCad, lệnh, kết quả và mọi kiểm tra bị bỏ qua.

## 3. PCB và chữ lụa

- [ ] Chỉ cập nhật PCB sau khi schematic, topology và BOM được review. Kiểm tra từng pad, net, short, clearance, lỗ khoan, dấu chân 1, footprint, kích thước và lỗ gá.
- [ ] Đặt đầu nối điện cực, điện trở bảo vệ và các nút ECG trở kháng cao ngắn, cân đối, tránh nguồn nhiễu. Đặt ADS1115 và tụ decoupling gần khối liên quan, kiểm tra đường hồi dòng GND.
- [ ] Kiểm tra hình học vùng anten trên cả F.Cu và B.Cu với đúng DevKit thực tế; keepout hiện được ghi ở F.Cu, không mặc định đáy sạch đồng. Xem vùng đồng sau refill và Gerber.
- [ ] Xóa chữ cá nhân, dòng trang trí và phân vùng dài trên lụa; giữ nhãn RA/LA/RL, nguồn, GND, test point, pin 1, revision và cảnh báo an toàn. Không để chữ đè pad, lỗ, linh kiện hoặc ra ngoài mép bo.
- [ ] Kiểm tra 3D và in 1:1 đối chiếu module thật. Refill zone, chạy DRC và parity lần cuối không bỏ qua lỗi, ghi rule, cảnh báo và kết quả.

## 4. Firmware và phần mềm

- [ ] Đối chiếu cấu hình ADS1115, conversion-ready, kênh, PGA, tốc độ; đối chiếu MAX30102 kênh, tốc độ, FIFO, ngắt và đọc burst với datasheet.
- [ ] Kiểm tra lỗi I²C, rơi hàng đợi, mất gói, FIFO overflow, lead-off, các mẫu cũ hoặc bị bỏ lỡ; kiểm tra hợp đồng dữ liệu giữa firmware và Python.
- [ ] Phân biệt timestamp thời điểm ngắt, hoàn tất chuyển đổi và thời điểm tín hiệu vật lý; đánh giá sai lệch, độ trễ ADC, FIFO và firmware. Nội suy lên 1 kHz không chứng minh độ chính xác 1 ms. Không mặc định bù 5,6 ms hay khẳng định sai số ≤2 ms nếu chưa đo.
- [ ] Biên dịch firmware bằng toolchain tương ứng; chạy test phần mềm với dữ liệu tổng hợp và dữ liệu thật khi có. Ghi lệnh, phiên bản, kết quả và giới hạn; thiếu thiết bị hoặc công cụ thì đánh dấu chưa kiểm thử.
- [ ] Phân biệt PAT từ đỉnh R đến chân PPG với PTT thuần, vì PAT bao gồm PEP. Không suy luận huyết áp khi chưa có phương pháp và dữ liệu tham chiếu phù hợp.

## 5. Kiểm tra trên bàn sau khi nhận PCB

- [ ] Kiểm tra ngoại quan, hướng IC, cầu hàn, thông mạch và chập nguồn khi chưa cấp điện.
- [ ] Cấp nguồn có giới hạn dòng, chưa gắn điện cực; đo các rail và kiểm tra nhiệt.
- [ ] Kiểm tra địa chỉ I²C, đọc lại cấu hình ADS1115/MAX30102; kiểm tra mất mẫu và FIFO.
- [ ] Dùng máy giả lập ECG hoặc nguồn thử thích hợp để đo gain, nhiễu, bộ lọc, lead-off, bão hòa và phục hồi; kiểm tra PPG khi Wi-Fi bật/tắt.
- [ ] Dùng tín hiệu điện–quang tham chiếu đo sai số đồng bộ hai kênh; ghi thiết bị, điều kiện, cách hiệu chuẩn và dữ liệu thô.
- [ ] **Không nối điện cực lên người chỉ vì chạy pin hoặc mạch qua thử nghiệm bàn.** Cần đánh giá an toàn phù hợp, kể cả cách ly, nguồn, đường dòng và lỗi đơn. Không nối USB, sạc hoặc thiết bị đo có thể tạo đường dẫn tới điện lưới khi có điện cực gắn người.

## 6. Hồ sơ bàn giao bắt buộc

- [ ] File KiCad `.kicad_sch`, `.kicad_pcb`, `.kicad_pro` cùng thư viện đúng phiên bản; kèm netlist cuối.
- [ ] Báo cáo thay đổi có lỗi, lý do, file/vị trí, phương pháp và kết quả xác minh; ERC, DRC, parity thực tế kèm cảnh báo còn lại.
- [ ] BOM và centroid đúng thiết kế, đúng đơn vị và mã linh kiện được đối chiếu; chỉ rõ các module và đầu nối phải mua đúng mẫu. BOM cũ từng dùng cùng mã cho hai giá trị điện trở, cần xác minh toàn bộ.
- [ ] Ảnh PCB trước/sau, đặc biệt chữ lụa. Chỉ xuất Gerber và NC drill sau review; mở bằng Gerber viewer và đối chiếu các lớp với PCB cuối.
- [ ] Danh sách việc chưa kiểm chứng, dụng cụ và linh kiện cần có để thử mạch thật. Chỉ tuyên bố mạch chạy thật sau khi lắp và đo, không suy ra từ ERC/DRC.

**Tiêu chí hoàn thành:** schematic và PCB nhất quán về linh kiện, footprint và kết nối; thiết kế được review, kiểm tra ERC/DRC/parity theo rule được công bố và có thể gửi làm PCB thử nghiệm. Các nhận định về an toàn người và hiệu năng cần bằng chứng thử nghiệm riêng.
