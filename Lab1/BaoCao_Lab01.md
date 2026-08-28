<div class="cover-page">
<div class="uni-name">ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM<br>KHOA ĐIỆN TỬ - VIỄN THÔNG</div>

<div class="report-title">BÁO CÁO THỰC HÀNH<br>THIẾT KẾ MẠCH IN PCB VỚI KICAD</div>

<div class="lab-name">Lab 01: Giới thiệu KiCad và Phân tích mạch nguồn đa năng</div>

<table class="student-info">
<tr><td><b>Họ và tên:</b></td><td>Lê Ngọc Tường</td></tr>
<tr><td><b>MSSV:</b></td><td>23207124</td></tr>
<tr><td><b>Lớp:</b></td><td>23DTV_CLC3</td></tr>
<tr><td><b>Môn học:</b></td><td>Thiết kế mạch in PCB với KiCad (HK3/2025-2026)</td></tr>
</table>
</div>

## BÀI TẬP 1: MINH CHỨNG CÀI ĐẶT KICAD 10

### 1. Thông số môi trường cài đặt
* Phần mềm: KiCad EDA Suite
* Phiên bản: `KiCad 10.0.5, release build`
* Nền tảng: `wxWidgets 3.3.2 Unicode, Boost 1.90.0`
* Hệ điều hành: `Microsoft Windows 11 (build 26200), 64-bit`
* Đường dẫn cài đặt: `C:\Program Files\KiCad\10.0\`
* Các công cụ tích hợp: Schematic Editor, Symbol Editor, PCB Editor, Footprint Editor, Gerber Viewer, Image Converter, Calculator Tools, Drawing Sheet Editor, Plugin and Content Manager.

### 2. Hình ảnh thực tế từ hệ thống

#### Hình 1.1: Hộp thoại thông tin phiên bản KiCad (About KiCad 10.0.5)
![About KiCad 10.0.5](Pic/Cau1.png)

#### Hình 1.2: Giao diện quản lý dự án (KiCad Project Manager)
![KiCad 10 Project Manager](Pic/Cau1_1.png)

## BÀI TẬP 2: PHÂN TÍCH KHỐI CHỨC NĂNG VÀ DATASHEET

Mạch nguồn đa năng gồm 7 khối chức năng chính:

### 1. Khối nguồn đầu vào (Input Power)
* **Linh kiện chính:**
  * `USB1`: Cổng Micro-USB Type-B 5 chân SMD (`VBUS`, `D-`, `D+`, `ID`, `GND`).
  * `SW1`: Công tắc gạt SPDT 3 chân THT (SS12D00).
  * `C1`: Tụ gốm SMD 0805 10µF.
* **Chức năng:**
  * Lấy nguồn +5V DC từ cổng USB hoặc củ sạc.
  * `SW1` đóng ngắt nguồn toàn mạch.
  * Tụ `C1` lọc nhiễu và chống sụt áp khi cắm cáp.

### 2. Khối ổn áp tuyến tính 3.3V (Linear Regulator)
* **Linh kiện chính:**
  * `U2`: IC ổn áp `AMS1117-3.3`.
  * `C2`: Tụ gốm SMD 0805 100nF (lọc nhiễu ngõ vào).
  * `C3`: Tụ gốm SMD 0805 10µF (ổn định điện áp ngõ ra).
* **Chức năng:**
  * Hạ áp từ +5V xuống +3.3V DC.
  * Cấp nguồn cho IC CP2102 và vi điều khiển bên ngoài.
* **Thông số kỹ thuật (`AMS1117-3.3`):**
  * Điện áp ngõ vào tối đa: 15V.
  * Điện áp ngõ ra: 3.3V (dung sai ±1.5%).
  * Điện áp sụt áp (Dropout Voltage): 1.1V tại 800mA.
  * Dòng điện ngõ ra định mức: 1.0A.
  * Đóng gói: SOT-223-3 (Pin 1: GND, Pin 2 & Tab: VOUT, Pin 3: VIN).

### 3. Khối tạo nguồn âm -5V (Negative Voltage Inverter)
* **Linh kiện chính:**
  * `U1`: IC đảo áp `LM2776DBVR`.
  * `C4`: Tụ bơm điện tích (Flying Capacitor) 1µF gốm SMD 0805.
  * `C5`: Tụ lọc ngõ ra 1µF gốm SMD 0805.
* **Chức năng:**
  * Tạo nguồn -5V DC từ nguồn +5V bằng nguyên lý Switched-Capacitor.
  * Cùng với nguồn +5V tạo ra nguồn đối xứng ±5V cho các Op-Amp (LM358, TL072).
* **Thông số kỹ thuật (`LM2776`):**
  * Dải điện áp hoạt động: 2.7V đến 5.5V.
  * Điện áp ngõ ra: Xấp xỉ -VIN (-5V khi VIN = +5V).
  * Dòng ngõ ra tối đa: 200mA.
  * Tần số đóng ngắt nội: 2.0 MHz.
  * Đóng gói: SOT-23-6.

### 4. Khối chuyển đổi USB sang UART (USB-to-UART Bridge)
* **Linh kiện chính:**
  * `U3`: IC cầu nối `CP2102-GM`.
  * `C6, C7`: Tụ bypass 100nF và 4.7µF.
  * Các đường tín hiệu: `D+`, `D-` và `TXD`, `RXD`, `RTS`, `CTS`.
* **Chức năng:**
  * Chuyển đổi tín hiệu USB 2.0 sang UART logic 3.3V.
* **Thông số kỹ thuật (`CP2102-GMR`):**
  * Tốc độ truyền dữ liệu (Baud rate): 300 bps đến 1.0 Mbps.
  * Sử dụng xung nhịp nội (sai số ±0.25%), không cần thạch anh ngoài.
  * Tích hợp EEPROM 1024 bytes và bộ điều áp LDO 3.3V.
  * Đóng gói: QFN-28 (5x5 mm, bước chân 0.5 mm).

### 5. Khối tạo xung vuông NE555 (Astable Pulse Generator)
* **Linh kiện chính:**
  * `U4`: IC định thời `NE555` (SOIC-8).
  * `R3, R4`: Điện trở định thời (10 kΩ).
  * `C8`: Tụ định thời (tụ hóa 10 µF).
  * `C9`: Tụ lọc chân điều khiển (10nF).
* **Chức năng:**
  * Mạch Astable Multivibrator tạo xung vuông liên tục ở ngõ ra chân 3.
  * Cấp xung clock để test các mạch logic hoặc mạch đếm.
* **Tần số ngõ ra:**
  `f = 1.44 / ((R3 + 2*R4) * C8)`
  Với `R3 = 10kΩ`, `R4 = 10kΩ`, `C8 = 10µF`:
  `f = 1.44 / ((10000 + 20000) * 10 * 10^-6) = 4.8 Hz`
* **Thông số kỹ thuật (`NE555`):**
  * Điện áp hoạt động: 4.5V đến 16V.
  * Dòng ngõ ra tối đa: 200mA.

### 6. Khối LED hiển thị trạng thái
* **Linh kiện chính:**
  * `LED1`: Báo nguồn +5V (Đỏ).
  * `LED2`: Báo nguồn +3.3V (Xanh lá).
  * `LED3`: Báo nguồn -5V (Vàng).
  * `LED4, LED5`: Báo truyền nhận dữ liệu `TX`, `RX` (Xanh dương).
  * `LED6`: Báo trạng thái ngõ ra xung NE555.
  * `R1, R2, R5, R6, R7, R8`: Điện trở hạn dòng (330Ω - 1kΩ, SMD 0805).
* **Chức năng:**
  * Báo trạng thái nguồn và tín hiệu truyền nhận.

### 7. Khối Header và cổng kết nối (I/O Connectors)
* **Linh kiện chính:**
  * `J1, J2, J5`: Header đơn 1x3 bước chân 2.54mm.
  * `J3, J4`: Header đôi 2x3 bước chân 2.54mm.
  * Jumper Shunt 2.54mm.
* **Chức năng:**
  * Xuất các đường nguồn ra ngoài: `+5V`, `+3.3V`, `-5V`, `GND`.
  * Xuất tín hiệu UART: `TXD`, `RXD`, `DTR`, `RTS`.
  * Dùng jumper để cấu hình ngắt hoặc nối nguồn cho từng khối.

### 8. Bảng tổng hợp Package và Footprint trên KiCad 10

| Ký hiệu | Tên linh kiện | Đóng gói | Thư viện Footprint KiCad 10 | Hãng SX |
| :--- | :--- | :--- | :--- | :--- |
| **U1** | LM2776DBVR | SOT-23-6 | `Package_TO_SOT_SMD:SOT-23-6` | TI |
| **U2** | AMS1117-3.3 | SOT-223-3 | `Package_TO_SOT_SMD:SOT-223-3_TabPin2` | AMS |
| **U3** | CP2102-GM | QFN-28 | `Package_DFN_QFN:QFN-28-1EP_5x5mm_P0.5mm` | Silicon Labs |
| **U4** | NE555 | SOIC-8 | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | TI / ST |
| **USB1** | Micro-USB 5P | Micro-B SMD | `Connector_USB:USB_Micro-B_Molex-47346-0001` | Molex |
| **SW1** | SS12D00 | THT 1P2T | `Button_Switch_THT:SW_Slide_1P2T_...` | Phổ thông |
| **R1-R8** | Trở SMD | 0805 Metric | `Resistor_SMD:R_0805_2012Metric` | Yageo |
| **C1-C7** | Tụ gốm SMD | 0805 Metric | `Capacitor_SMD:C_0805_2012Metric` | Murata |
| **C8** | Tụ hóa 10µF | Radial D5.0 | `Capacitor_THT:CP_Radial_D5.0mm_P2.50mm` | Nichicon |
| **D1-D6** | LED SMD | 0805 Metric | `LED_SMD:LED_0805_2012Metric` | Everlight |
| **J1-J5** | Pin Header | Cắm 2.54mm | `Connector_PinHeader_2.54mm:PinHeader_...` | Phổ thông |

## BÀI TẬP 3: SƠ ĐỒ KHỐI CỦA MẠCH NGUỒN

![Sơ đồ khối mạch nguồn](Pic/Cau3_block_diagram.png)

## BÀI TẬP 4: BẢNG DỰ TOÁN CHI PHÍ VẬT TƯ (BOM)

| STT | Ký hiệu | Mã linh kiện | Mô tả chi tiết | SL | Đơn giá (VNĐ) | Thành tiền (VNĐ) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| 1 | `U1` | LM2776DBVR | IC Đảo áp -5V, SOT-23-6 | 1 | 31.000 | 31.000 |
| 2 | `U2` | AMS1117-3.3 | IC Ổn áp 3.3V, SOT-223 | 1 | 3.990 | 3.990 |
| 3 | `U3` | CP2102-GMR | IC USB sang UART, QFN-28 | 1 | 60.420 | 60.420 |
| 4 | `U4` | NE555 | IC Định thời, SOIC-8 | 1 | 3.420 | 3.420 |
| 5 | `USB1` | Micro-USB 5P | Cổng Micro-B SMD | 1 | 2.500 | 2.500 |
| 6 | `SW1` | SS12D00 | Công tắc gạt 1P2T | 1 | 1.800 | 1.800 |
| 7 | `R1-R7` | Trở 330Ω | Trở SMD 0805 (hạn dòng) | 5 | 150 | 750 |
| 8 | `R3, R4`| Trở 10kΩ | Trở SMD 0805 (định thời) | 2 | 150 | 300 |
| 9 | `R8` | Trở 1kΩ | Trở SMD 0805 | 1 | 150 | 150 |
| 10 | `C1, C3`| Tụ gốm 10µF | Tụ gốm SMD 0805 16V | 2 | 1.100 | 2.200 |
| 11 | `C2,C6,C7,C9` | Tụ gốm 100nF | Tụ gốm SMD 0805 | 4 | 250 | 1.000 |
| 12 | `C4, C5`| Tụ gốm 1µF | Tụ gốm SMD 0805 | 2 | 650 | 1.300 |
| 13 | `C8` | Tụ hóa 10µF | Tụ hóa Radial D5mm 25V | 1 | 800 | 800 |
| 14 | `D1-D3` | LED 0805 | LED báo nguồn (Đỏ, Xanh, Vàng) | 3 | 450 | 1.350 |
| 15 | `D4, D5`| LED 0805 | LED tín hiệu UART (Xanh dương) | 2 | 500 | 1.000 |
| 16 | `J1,J2,J5`| Header 1x3 | Rào cắm đơn 2.54mm | 3 | 800 | 2.400 |
| 17 | `J3, J4`| Header 2x3 | Rào cắm đôi 2.54mm | 2 | 1.500 | 3.000 |
| 18 | `Jumper`| Jumper | Cầu nối ngắn mạch 2.54mm | 3 | 400 | 1.200 |
| 19 | `PCB` | Gia công | Bo mạch FR-4 2 lớp | 1 | 35.000 | 35.000 |
| | **TỔNG** | | | **38** | | **151.280** |
