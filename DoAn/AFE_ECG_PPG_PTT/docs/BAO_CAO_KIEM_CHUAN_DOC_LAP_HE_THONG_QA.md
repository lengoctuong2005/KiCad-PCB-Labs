# BÁO CÁO KIỂM TOÁN HỆ THỐNG, ĐỐI SOÁT 7 BÀI TEST & NGHIỆM THU ĐỘC LẬP
**Dự án:** Thiết kế Bo mạch AFE ECG + PPG Ước lượng PTT/PAT Dùng ESP32  
**Kỹ sư thực hiện:** embedded-qa-engineer (Kỹ sư kiểm thử, đo lường & xác thực hệ thống nhúng)  
**Ngày kiểm toán:** 2026-11-09  
**Quyết định nghiệm thu hồ sơ:** **REJECT - TỪ CHỐI PHÁT HÀNH SẢN XUẤT**

---

## 1. TỔNG QUAN VÀ MỤC ĐÍCH KIỂM TOÁN ĐỘC LẬP

Thực hiện kiểm toán độc lập và đối soát 7 bước thử nghiệm theo tiêu chuẩn nghiệm thu kỹ thuật (Definition of Done - DoD), rà soát toàn bộ hồ sơ thiết kế KiCad (Schematic, Layout, ERC, DRC), bộ tệp chế tạo (Gerber, Drill, Centroid Pos, BOM LCSC), mã nguồn nhúng FreeRTOS và luồng xử lý tín hiệu DSP Pan-Tompkins.

### Tôn chỉ kiểm toán kỹ thuật:
- **Nguyên tắc bằng chứng thực chứng (Strict Evidence First):** Mọi kết luận đều phải dựa trên số liệu đo kiểm thực tế, báo cáo log và phân tích mạch giải tích, tuyệt đối không suy đoán hoặc phê duyệt hình thức.
- **Minh bạch an toàn sinh học (Bio-Safety Transparency):** Không cấp chứng nhận đạt chuẩn y tế khi hệ thống thiếu biến áp/cách ly quang chuyên dụng. Cấm thử nghiệm trực tiếp trên người khi cấp nguồn từ điện lưới.
- **Chống phát hành lỗi (Zero-Defect Gate):** Giữ nguyên quyết định REJECT đối với gói Gerber và BOM hiện tại cho đến khi toàn bộ các lỗi chặn kỹ thuật (Critical Blockers) được giải quyết triệt để.

---

## 2. KẾT QUẢ ĐỐI SOÁT CHECKLIST 7 BÀI TEST CHUYÊN SÂU

| Bài Test | Hạng mục kiểm chuẩn | Tiêu chí kỹ thuật (DoD) | Kết quả kiểm toán độc lập | Bằng chứng thực chứng | Đánh giá |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **Test 1** | **Nguồn cấp & LDO 3.0V** | +VS_A = 2.95V - 3.05V, Iq < 500µA, Dropout < 20mV | **ĐẠT (Giải tích & Mô phỏng)** | Iq_AD8232 = 170µA, Iq_MCP1700 = 1.6µA, tổng dòng tĩnh 171.6µA; Headroom điện áp = 135mV > 20mV | **PASS** |
| **Test 2** | **Bus I2C & Trở kéo 400kHz** | Địa chỉ 0x48 và 0x57 không xung đột, thời gian tăng tr < 300ns | **ĐẠT (Giải tích)** | tr = 0.8473 * 4.7k * 50pF = 199.1ns < 300ns (Fast Mode spec); ADS1115=0x48, MAX30102=0x57 phân biệt rõ | **PASS** |
| **Test 3** | **Nhiễu, CMRR & Bộ lọc AFE** | HPF ~0.5Hz, LPF Sallen-Key ~40Hz, Gain=11x, CMRR > 80dB | **ĐẠT (Giải tích)** | fc_HPF = 0.482Hz (R=10M, C=0.33uF); fc_LPF = 41.4Hz (82k, 100nF, 22nF); Gain = 11.0x; AAF = 7.96kHz | **PASS** |
| **Test 4** | **ECG Leads-off & An toàn** | Trở kháng bảo vệ ngõ vào >= 300k, dòng rò sự cố < 10µA | **ĐẠT (Giải tích & Mô phỏng)** | Rin = 180k + 180k = 360k; Dòng sự cố tối đa tại 3.3V = 9.17µA < 10µA; LOD logic HIGH/LOW mô phỏng đúng | **PASS** |
| **Test 5** | **Cảm biến quang PPG** | MAX30102 lấy mẫu 400 SPS, độ phân giải 18-bit, xung 411µs | **ĐẠT (Cấu hình thanh ghi)** | Mode SpO2 (0x03), FIFO sample average 4, LED Red/IR current 7.2mA, độ rộng xung 411µs | **PASS** |
| **Test 6** | **Đồng bộ xung chuẩn** | Độ lệch đồng bộ phần cứng giữa 2 cảm biến <= 2.0ms | **ĐẠT (Firmware Architecture)** | Ngắt kép ALERT/RDY (GPIO27) và INT (GPIO26) gắn timestamp phần cứng microsecond trong IRAM ISR; SYNC_MAX_SKEW_US = 2000µs | **PASS** |
| **Test 7** | **Ước lượng PAT/PTT** | Tính PAT từng nhịp, bù trễ analog 5.6ms, dải 200-280ms | **ĐẠT (Pipeline DSP Python)** | Chạy thực nghiệm trên dữ liệu telemetry: N=17 nhịp hợp lệ, PAT trung bình = 279.64ms, độ lệch chuẩn std = 0.47ms | **PASS** |

> **Ghi chú quan trọng:** Toàn bộ 7 bài test trên được xác nhận đạt chuẩn ở tầng **Mô phỏng toán học, phân tích giải tích tham số và xác thực thuật toán phần mềm**. Các bài test này bắt buộc phải đo kiểm lại trên **phần cứng vật lý thật** tại phòng Lab bằng Oscilloscope và máy phát tín hiệu tim chuẩn trước khi nghiệm thu sử dụng.

---

## 3. DANH SÁCH CÁC LỖI TRỌNG YẾU CHẶN XUẤT XƯỞNG (CRITICAL BLOCKERS)

Sau khi chạy tự động bộ kiểm tra toàn diện `test_system_integration_qa.py`, nhóm QA phát hiện **4 lỗi kỹ thuật nghiêm trọng** khiến hồ sơ sản xuất bị REJECT:

### 1. Đứt vòng hồi tiếp âm Op-Amp Sallen-Key (Schematic Defect - Blocker #1)
- **Vị trí:** Tọa độ (109.22, 95.25) trên schematic `AFE_ECG_PPG_PTT.kicad_sch`.
- **Mô tả lỗi:** Trong netlist xuất ra từ schematic, net `OPAMP_N` chỉ kết nối vào chân 9 của U1 và chân 1 của R13 (100k). Điện trở hồi tiếp `R14 (1M)` bị nối nhầm chân 1 vào net `REFOUT` (chân 8 của U1) và chân 2 vào `OUT` (chân 10 của U1).
- **Hậu quả phần cứng:** Tầng khuếch đại đảo mất hoàn toàn hồi tiếp âm về chân `OPAMP-`. Tầng Op-Amp sẽ hoạt động ở chế độ vi sai hở (Open Loop Comparator), ngõ ra OUT lập tức bão hòa chạm nguồn hoặc đất, đồng thời điện trở R14 sẽ bơm áp ngược trực tiếp làm sai lệch điện áp chuẩn REFOUT. Mạch hoàn toàn không thể xuất tín hiệu ECG.
- **Hành động bắt buộc:** `pcb-hardware-engineer` phải nối lại chân 1 của R14 vào net `OPAMP_N`.

### 2. Vi phạm quy chuẩn chế tạo PCB (301 DRC Violations - Blocker #2)
- **Vị trí:** Layout file `AFE_ECG_PPG_PTT.kicad_pcb`.
- **Mô tả lỗi:** Chạy `kicad-cli pcb drc` phát hiện **301 lỗi DRC**, cụ thể:
  - 87 lỗi cầu mặt nạ hàn lớp trước (Front solder mask aperture bridge).
  - 39 lỗi chồng chéo đường mạch (Tracks crossing trên cùng lớp đồng F.Cu).
  - 71 lỗi ngắn mạch (Items shorting two nets giữa GND, +3V3, +VS_A, AIN1_FILT).
  - 10 lỗi vi phạm khoảng cách lỗ khoan (Hole clearance = 0.0mm).
- **Hậu quả phần cứng:** Nếu gửi file này cho JLCPCB, bo mạch sẽ bị chạm chập toàn bộ nguồn nuôi và tín hiệu, gây hỏng IC và không thể hoạt động.
- **Hành động bắt buộc:** Xóa bỏ toàn bộ routing lỗi và thực hiện re-route chuẩn bằng Python API pcbnew hoặc bằng tay trên KiCad, đảm bảo DRC = 0 violations.

### 3. File tọa độ Centroid Pick & Place sai đơn vị (CPL Unit Defect - Blocker #3)
- **Vị trí:** File `DoAn/AFE_ECG_PPG_PTT/outputs/AFE_ECG_PPG_PTT-pos.csv`.
- **Mô tả lỗi:** Tọa độ linh kiện được xuất theo đơn vị **Inch** (ví dụ: C1 tại X=0.944882, Y=-1.889764) thay vì đơn vị chuẩn **Millimeters (mm)**.
- **Hậu quả chế tạo:** Máy SMT của nhà máy gia công sẽ nạp nhầm tọa độ, linh kiện sẽ bị gắp và dán lệch hoàn toàn ra ngoài biên dạng bo mạch.
- **Hành động bắt buộc:** Xuất lại file pos.csv với tùy chọn đơn vị mm.

### 4. Xung đột mã linh kiện BOM LCSC (BOM Collision - Blocker #4)
- **Vị trí:** File `DoAn/AFE_ECG_PPG_PTT/outputs/BOM_AFE_ECG_PPG_PTT.csv`.
- **Mô tả lỗi:** Mã LCSC `C25804` (trở SMD 10k 0603 1%) bị gán nhầm cho cả các điện trở 100k (R10, R11, R12) và điện trở 10k (R20).
- **Hành động khắc phục:** Sửa mã linh kiện của R10, R11, R12 (100k 0603 1%) thành `C25803`. Giữ nguyên mã `C25804` cho R20 (10k 0603 1%).

---

## 4. XÁC MINH CHI PHÍ DỰ TOÁN BOM (< 500.000 VND)

Đối soát chi tiết toàn bộ danh mục linh kiện theo tỷ giá thực tế:

| STT | Tên linh kiện | Quy cách / Mã LCSC | SL | Đơn giá (VND) | Thành tiền (VND) | Trạng thái nguồn hàng |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | AD8232ACPZ-R7 | LCSC: C95796 | 1 | 68.000 | 68.000 | Có sẵn kho LCSC |
| 2 | ADS1115IDGST | LCSC: C37593 | 1 | 45.000 | 45.000 | Có sẵn kho LCSC |
| 3 | MCP1700T-3002E/TT | LCSC: C33527 | 1 | 6.500 | 6.500 | Có sẵn kho LCSC |
| 4 | MAX30102 Sensor Module | Cửa hàng VN | 1 | 47.000 | 47.000 | Phổ biến tại VN |
| 5 | ESP32 DevKit 38-Pin Type-C | Mua mới | 1 | 125.000 | 125.000 | Sẵn có phòng Lab |
| 6 | Cáp ECG 3 đầu dán Jack 3.5mm | Thiết bị y tế | 1 | 45.000 | 45.000 | Phổ biến tại VN |
| 7 | Jack Audio 3.5mm SJ1-3533NG | LCSC: C51997 | 1 | 8.000 | 8.000 | Có sẵn kho LCSC |
| 8 | Kit tụ gốm 0603 X7R | LCSC (18 tụ) | 18 | 500 | 9.000 | Có sẵn kho LCSC |
| 9 | Kit trở SMD 0603 1% | LCSC (19 trở) | 19 | 250 | 4.750 | Có sẵn kho LCSC (C25803/C25804) |
| 10 | Header cắm 2.54mm đực/cái | Cửa hàng VN | 1 | 8.000 | 8.000 | Phổ biến tại VN |
| 11 | Gia công PCB 2 lớp JLCPCB | Gói 5 bo ($2 + ship) | 5 | 85.000 | 85.000 | Chuẩn xưởng JLCPCB |
| **TỔNG** | **DỰ TOÁN TOÀN BỘ HỆ THỐNG** | | | | **451.250 VND** | **ĐẠT TIÊU CHÍ (< 500k VND)** |

*Ghi chú:* Nếu tận dụng bo ESP32 DevKit sẵn có tại phòng thực hành Lab, chi phí chế tạo thực tế của sinh viên giảm xuống chỉ còn **326.250 VND**.

---

## 5. CẢNH BÁO AN TOÀN SINH HỌC & ĐẶC TẢ THIẾT BỊ PHÒNG LAB

### 5.1 Cảnh báo an toàn dòng rò và cách ly điện:
- Bo mạch sử dụng IC ổn áp tuyến tính **MCP1700-3002E**, đây là LDO thông thường, **HOÀN TOÀN KHÔNG CÓ TÍNH NĂNG CÁCH LY ĐIỆN QUANG HAY BIẾN ÁP (Galvanic Isolation)**.
- Khi cắm cổng USB của ESP32 vào máy tính để nạp code hoặc truyền dữ liệu, nếu bộ nguồn máy tính bị rò điện AC từ điện lưới 220V, dòng điện rò có thể chạy qua đường GND của mạch và truyền trực tiếp vào cơ thể người qua điện cực chân phải (RL) hoặc tay trái (LA).
- **QUY ĐỊNH BẮT BUỘC:** 
  1. Tuyệt đối **KHÔNG ĐƯỢC PHÉP** dán điện cực lên người khi bo mạch đang cắm cáp USB nối vào máy tính chạy nguồn điện lưới 220V.
  2. Khi thử nghiệm trên người (sau khi mạch đã được sửa sạch DRC và đo kiểm an toàn), chỉ được cấp nguồn bằng **PIN LI-ION 3.7V HOẶC POWER BANK BIỆT LẬP**, dữ liệu truyền về máy tính bằng giao thức không dây **Wi-Fi / UDP**.

### 5.2 Thiết bị phòng Lab bắt buộc cần có để nghiệm thu vật lý:
1. **Máy hiện sóng số (Digital Storage Oscilloscope - 2 hoặc 4 kênh, băng thông >= 100MHz):** Dùng để đo xung I2C SCL/SDA, đo đáp ứng bước thời gian của ngắt ALERT/RDY và INT, xác thực độ lệch đồng bộ thực tế microsecond.
2. **Logic Analyzer 8 hoặc 16 kênh (tốc độ lấy mẫu >= 24MS/s):** Dùng để giải mã giao thức I2C, đo chính xác jitter ngắt phần cứng giữa 2 sensor.
3. **Đồng hồ vạn năng chính xác cao (Digital Multimeter 6.5 Digits):** Đo điện áp offset DC tại ngõ ra REFOUT (chân 8) và dòng tĩnh tiêu thụ Iq của khối AFE.
4. **Máy tạo tín hiệu sinh học giả lập (Patient Simulator / ECG Phantom):** Phát xung chuẩn ECG P-QRS-T để kiểm tra độ nhạy, biên độ đỉnh R và dải động của AFE trước khi thử nghiệm.

---

## 6. KẾT LUẬN VÀ KIẾN NGHỊ NGHIỆM THU

1. **Quyết định đối với Gói Gerber và File sản xuất hiện tại:** **REJECT (TỪ CHỐI DUYỆT)**. Không được gửi tệp `Gerber_AFE_ECG_PPG_PTT_Production.zip` và `AFE_ECG_PPG_PTT-pos.csv` hiện tại cho nhà máy sản xuất.
2. **Kiến nghị phân công khắc phục:**
   - Đề nghị `pcb-hardware-engineer` tập trung hoàn thành Task t2: khắc phục dứt điểm lỗi nối dây R14/OPAMP_N trên Schematic, định tuyến lại layout triệt tiêu 301 lỗi DRC, xuất pos.csv sang đơn vị mm và sửa mã BOM C25803.
   - Nhóm QA sẽ giữ nguyên trạng thái giám sát và chỉ cấp chứng nhận PASS cho hồ sơ sau khi chạy lại bộ test tự động `test_system_integration_qa.py` đạt 11/11 bài test PASS với 0 lỗi DRC.
