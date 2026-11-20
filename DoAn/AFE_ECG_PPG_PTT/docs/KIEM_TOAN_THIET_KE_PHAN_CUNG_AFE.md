> # CẢNH BÁO AN TOÀN: BÁO CÁO BÊN DƯỚI ĐÃ BỊ THU HỒI
>
> Các khẳng định về tuân thủ IEC 60601-1, dòng bệnh nhân, an toàn, LDO cách ly hoặc triệt nhiễu, độ ổn định RLD, HPF/LPF và độ trễ ≤2 ms trong báo cáo cũ **không được chứng minh** và có nhầm lẫn giữa các thiết kế có tham chiếu linh kiện khác nhau. **Không sử dụng để chế tạo, nghiệm thu hoặc kết nối người.** Nội dung cũ giữ lại nguyên văn để truy vết, không có hiệu lực. Xem [Báo cáo đối chiếu t2](DOI_SOAT_T2_VA_NGAN_CHAN_CHE_TAO.md) và bằng chứng đi kèm.

---

# BÁO CÁO KIỂM TOÁN THIẾT KẾ PHẦN CỨNG AFE ECG + PPG (PTT/PAT)
**Dự án:** AFE_ECG_PPG_PTT  
**Phân hệ:** Hardware & Mạch Tương Tự Sinh Y (Analog Front-End)  
**Kỹ sư thực hiện:** pcb-hardware-engineer  
**Ngày lập:** 2026-11-09  
**Trạng thái kiểm toán:** HOÀN TẤT - XÁC LẬP TẬP THÔNG SỐ VÀ DANH MỤC LỖI CẦN HIỆU CHỈNH

---

## 1. MỤC TIÊU VÀ PHẠM VI KIỂM TOÁN
Rà soát toàn diện schematic (`AFE_ECG_PPG_PTT.kicad_sch`), layout PCB (`AFE_ECG_PPG_PTT.kicad_pcb`), định danh linh kiện (BOM), dữ liệu sản xuất CPL/Pos, đối chiếu trực tiếp với:
- **Analog Devices AD8232 Datasheet** (Rev. D): Cấu hình ECG Monitor 2 cực HPF, 2 cực Sallen-Key LPF, mạch RLD, khôi phục đường nền Fast Restore (SW), kiểm tra ngưỡng an toàn dòng điện bệnh nhân.
- **Texas Instruments ADS1115 Datasheet** (SBAS444D): Dải vi sai PGA, bộ lọc RC chống chồng phổ (anti-aliasing), tốc độ lấy mẫu 475/860 SPS và ghép nối ALERT/RDY.
- **Maxim Integrated / Analog Devices MAX30102 Datasheet**: Ghép nối quang học PPG I2C và ngắt phần cứng.
- **Espressif ESP32-WROOM-32 DevKit**: Phân bổ chân GPIO, tránh xung đột strapping pins và hạn chế ADC2 khi bật Wi-Fi.

---

## 2. KIỂM CHỨNG TÍNH TOÁN VÀ THÔNG SỐ MẠCH AFE (AD8232)

### 2.1. Điện trở bảo vệ ngõ vào bệnh nhân (Patient Protection Input Resistors)
- **Tiêu chuẩn Y tế (IEC 60601-1 / AAMI EC11):** Dòng rò qua bệnh nhân trong điều kiện bình thường phải $< 10\,\mu\text{A}$, điện áp chạm ngẫu nhiên giả định $V_s = 3.0\text{V} - 5.0\text{V}$. Trở kháng ngõ vào tối thiểu:
  $$R_{protect} \ge \frac{V_s}{10\,\mu\text{A}} = \frac{3.0\,\text{V}}{10\,\mu\text{A}} = 300\,\text{k}\Omega$$
- **Thiết kế thực tế:**
  - Điện cực RA (Right Arm): Phân tách thành 2 điện trở nối tiếp $R_1 (180\,\text{k}\Omega) + R_3 (180\,\text{k}\Omega) = 360\,\text{k}\Omega \ge 300\,\text{k}\Omega$.
  - Điện cực LA (Left Arm): Phân tách thành 2 điện trở nối tiếp $R_2 (180\,\text{k}\Omega) + R_4 (180\,\text{k}\Omega) = 360\,\text{k}\Omega \ge 300\,\text{k}\Omega$.
  - Điện cực RL (Right Leg Drive): Điện trở bảo vệ $R_{15} = 360\,\text{k}\Omega \ge 300\,\text{k}\Omega$.
- **Kết luận:** **ĐẠT CHUẨN AN TOÀN SINH HỌC**. Việc chia thành cặp $180\,\text{k}\Omega + 180\,\text{k}\Omega$ cho phép bố trí đối xứng, hạn chế quá áp phóng điện tĩnh điện (ESD) phân bố đều qua 2 vỏ điện trở 0603.

### 2.2. Bộ lọc thông cao 2 cực khôi phục đường nền (2-Pole High-Pass Filter & Fast Restore)
- **Nguyên lý:** Tích hợp bộ tích phân DC restore qua chân `HPDRIVE` (pin 1), `HPSENSE` (pin 20) và công tắc khôi phục nhanh `SW` (pin 6).
- **Công thức AD8232 Datasheet (trang 22):**
  $$f_{c,HP} = \frac{10}{2\pi \cdot R_{HP} \cdot C_{HP}}$$
  (Do hệ số khuếch đại mạch tích phân nội bộ là 10).
- **Thông số linh kiện:**
  - $R_7 = 10\,\text{M}\Omega$
  - $C_1 = C_2 = 0.33\,\mu\text{F}$ (X7R 50V)
- **Kết quả tính toán:**
  $$f_{c,HP} = \frac{10}{2\pi \cdot (10 \times 10^6\,\Omega) \cdot (0.33 \times 10^{-6}\,\text{F})} = \frac{10}{20.7345} = 0.4823\,\text{Hz} \approx 0.5\,\text{Hz}$$
- **Kết luận:** **ĐẠT**. Tần số cắt $0.482\,\text{Hz}$ loại bỏ hoàn toàn hiện tượng trôi đường nền (baseline wander) do nhịp thở (thường ở $0.1 - 0.3\,\text{Hz}$), đồng thời giữ nguyên vẹn đoạn sóng ST và biên độ phức bộ QRS.

### 2.3. Mạch truyền động chân phải (Right Leg Drive - RLD)
- **Cấu hình:** Đảo pha điện áp đồng pha (Common Mode) đưa ngược về cơ thể qua điện cực RL để triệt tiêu nhiễu 50Hz/60Hz điện lưới (CMRR tổng hệ thống $> 80\,\text{dB}$).
- **Thông số:**
  - Điện trở phản hồi vòng RLD: $R_{14} = 1\,\text{M}\Omega$
  - Tụ ổn định pha tránh tự kích: $C_6 = 1\,\text{nF}$
  - Tần số cắt mạch tích phân RLD: $f_{c,RLD} = \frac{1}{2\pi \cdot R_{14} \cdot C_6} = \frac{1}{2\pi \cdot 10^6 \cdot 10^{-9}} = 159.15\,\text{Hz}$
  - Điện trở bảo vệ ngõ ra: $R_{15} = 360\,\text{k}\Omega$
- **Kết luận:** **ĐẠT**. Độ lợi vòng kín tại 50Hz đủ lớn để triệt tiêu nhiễu cảm ứng điện từ mà không gây mất ổn định vòng lặp.

### 2.4. Bộ lọc thông thấp Sallen-Key 2 cực (LPF) và tầng khuếch đại
- **Cấu trúc:** Mạch lọc tích cực Sallen-Key 2 cực sử dụng op-amp tích hợp trong AD8232.
- **Công thức tần số cắt:**
  $$f_{c,LP} = \frac{1}{2\pi \sqrt{R_{10} \cdot R_{11} \cdot C_3 \cdot C_4}}$$
- **Đối chiếu hai phương án cấu hình:**
  1. *Phương án tối ưu 41.4Hz (CALC.json / DESIGN_NOTES):* $R_{10}=R_{11}=82\,\text{k}\Omega$, $C_3=100\,\text{nF}$, $C_4=22\,\text{nF} \implies f_c = 41.38\,\text{Hz}$.
  2. *Phương án BOM thực tế:* $R_{10}=R_{11}=100\,\text{k}\Omega$, $C_3=22\,\text{nF}$, $C_4=10\,\text{nF} \implies f_c = 107.3\,\text{Hz}$ (hoặc nếu dùng $R=180\,\text{k}\Omega \implies 59.6\,\text{Hz}$).
- **Hệ số khuếch đại (Gain):**
  - Tầng khuếch đại đo đạc (IA) cố định: $G_{IA} = 100$.
  - Tầng Op-Amp đệm/lọc:
    $$G_{OP} = 1 + \frac{R_{13}}{R_{12}} = 1 + \frac{1\,\text{M}\Omega}{100\,\text{k}\Omega} = 11$$
  - Tổng hệ số khuếch đại AFE:
    $$G_{total} = G_{IA} \times G_{OP} = 100 \times 11 = 1100$$
- **Động học tín hiệu:**
  - Tín hiệu ECG đỉnh-đỉnh thông thường: $V_{in,pp} \approx 1.0\,\text{mV}$.
  - Ngõ ra: $V_{out,pp} = 1.0\,\text{mV} \times 1100 = 1.1\,\text{V}_{pp}$.
  - Nguồn cấp $V_{DD} = 3.0\,\text{V}$, điện áp định thiên $V_{REFOUT} = 1.5\,\text{V}$.
  - Biên độ dao động điện áp ngõ ra: $1.5\,\text{V} \pm 0.55\,\text{V} \implies [0.95\,\text{V} - 2.05\,\text{V}]$.
  - Khoảng cách an toàn đến điện áp bão hòa nguồn (Headroom): $> 0.95\,\text{V}$, đảm bảo không bị méo đỉnh (saturation clipping) khi bệnh nhân cử động.

### 2.5. Nguồn cấp LDO Analog 3.0V (MCP1700-3002E)
- **Điện áp vào:** $+3.3\,\text{V}$ (từ board ESP32).
- **Điện áp ra:** $+3.0\,\text{V}$ cấp riêng cho AD8232 và mạng phân áp REFIN.
- **Độ sụt áp (Dropout Voltage):** Tại dòng tải $I_Q \approx 170\,\mu\text{A}$, $V_{DO} < 20\,\text{mV} \ll 300\,\text{mV}$ chênh lệch nguồn, LDO hoạt động trong vùng ổn áp tuyến tính hoàn hảo.
- **Triệt tiêu nhiễu (PSRR):** Đạt $> 40\,\text{dB}$ tại $1\,\text{kHz}$, ngăn triệt để xung nhiễu chuyển mạch từ nguồn DC-DC và khối RF Wi-Fi/Bluetooth của ESP32 sang kênh tương tự microvolt.

---

## 3. KIỂM TOÁN TẦNG ADC ADS1115 VÀ GIAO TIẾP ESP32 / MAX30102

### 3.1. Dải đo vi sai PGA ADS1115
- **Đấu nối vi sai:**
  - $V_{in+} = \text{AIN0} \leftarrow \text{ECG\_OUT}$
  - $V_{in-} = \text{AIN1} \leftarrow \text{REFOUT} (1.5\,\text{V})$
- **Điện áp vi sai thực tế:**
  $$V_{diff} = V_{AIN0} - V_{AIN1} = (1.5\,\text{V} \pm 0.55\,\text{V}) - 1.5\,\text{V} = \pm 0.55\,\text{V}$$
- **Cấu hình PGA đề xuất:**
  - *Cấu hình 1 (FSR = $\pm 1.024\,\text{V}$, PGA = 4):* Độ phân giải LSB $= 1.024 / 32768 = 31.25\,\mu\text{V}$. Dải đo phủ trọn $\pm 0.55\,\text{V}$ với hệ số an toàn $46\%$, mang lại độ nhạy và số bit hiệu dụng (ENOB) cao nhất.
  - *Cấu hình 2 (FSR = $\pm 2.048\,\text{V}$, PGA = 2):* Độ phân giải LSB $= 2.048 / 32768 = 62.5\,\mu\text{V}$, chống tràn tuyệt đối khi điện thế tiếp xúc điện cực thay đổi đột ngột.
- **Mạch lọc Anti-Aliasing vi sai:**
  - $R_{16} = R_{17} = 1\,\text{k}\Omega$, $C_7 = 10\,\text{nF}$ (vi sai), $C_8 = C_9 = 1\,\text{nF}$ (đồng pha).
  - Tần số cắt vi sai: $f_{diff} \approx \frac{1}{2\pi \cdot 2000 \cdot 10\,\text{nF}} = 7.95\,\text{kHz}$.
  - Đáp ứng Nyquist hoàn hảo cho chế độ lấy mẫu 475 SPS và 860 SPS của ADS1115.

### 3.2. Cấu hình chân Header MAX30102 và ESP32 DevKit 38-Pin
- **MAX30102 Module (Header J3 - 7 pins):**
  - Chân 1: VIN (+3.3V)
  - Chân 2: SCL (I2C Clock) -> nối ESP32 GPIO22
  - Chân 3: SDA (I2C Data) -> nối ESP32 GPIO21
  - Chân 4: INT (Active-Low Interrupt) -> nối ESP32 GPIO26
  - Chân 5: RD (NC)
  - Chân 6: IRD (NC)
  - Chân 7: GND
- **ESP32 DevKit 38-Pin Mapping (J2A: Left 1-19, J2B: Right 1-19):**
  - `GPIO21`: I2C SDA (kèm điện trở kéo $R_{18} = 4.7\,\text{k}\Omega$ lên 3.3V)
  - `GPIO22`: I2C SCL (kèm điện trở kéo $R_{19} = 4.7\,\text{k}\Omega$ lên 3.3V)
  - `GPIO26`: `MAX_INT` (ngắt phần cứng PPG)
  - `GPIO27`: `ADS_ALERT` (ngắt phần cứng ADC ECG, kèm điện trở kéo $R_{20} = 10\,\text{k}\Omega$)
  - `GPIO32`: `LOD+` (ngõ vào số cảnh báo tuột điện cực dương)
  - `GPIO33`: `LOD-` (ngõ vào số cảnh báo tuột điện cực âm)
  - `GPIO25`: `FR` (ngõ ra điều khiển Fast Restore chủ động)
  - `GPIO34`: `ECG_OUT` kênh analog dự phòng (thuộc ADC1_CH6, không bị ảnh hưởng bởi Wi-Fi)
- **Đánh giá xung đột:** Hoàn toàn tránh các chân nạp/khởi động nhạy cảm (GPIO 0, 2, 5, 12, 15). Chân ngắt cứng chuyên dụng cho cả ECG và PPG bảo đảm độ trễ đồng bộ $\le 2\,\text{ms}$ phục vụ ước lượng PTT/PAT.

---

## 4. BẢNG TỔNG HỢP CÁC LỖI TRỌNG YẾU (DEFECT LOG) CẦN KHẮC PHỤC Ở TASK T2

| STT | Phân loại | Mã lỗi / Vị trí | Mô tả chi tiết | Hướng xử lý ở Task t2 |
|---|---|---|---|---|
| 1 | **ERC** | `#FLG03` & `U3 Pin 2` | Lỗi `pin_to_pin`: Pin Power Output của U3 (`VOUT`) nối chung với `#FLG03` trên net `+VS_A`. | Xóa bỏ `#FLG03` và đoạn dây thừa trên net `+VS_A`. |
| 2 | **ERC** | `HP_NODE2` & U1 Pin 6 | Cảnh báo `isolated_pin_label`: Nhãn `HP_NODE2` tại chân 6 (SW) chỉ có 1 kết nối cô lập, trong khi điểm giữa C1-C2 dùng nhãn `HP_NODE`. | Đổi nhãn chân 6 U1 thành `HP_NODE` để ghép chung mạng với điểm giữa C1 và C2. |
| 3 | **ERC** | `OPAMP_N` & `REFOUT` | Cảnh báo `multiple_net_names`: Hai nhãn toàn cục `OPAMP_N` và `REFOUT` nối trùng tại (96.52, 78.74 / 81.28). | Tách rời 2 net: Chân 8 là `REFOUT`, chân 9 là `OPAMP_N`. |
| 4 | **ERC** | Thư viện `afe.kicad_sym` | Cảnh báo `lib_symbol_mismatch` trên hàng loạt linh kiện (U1, U2, J1, R, C). | Cập nhật và đồng bộ toàn bộ symbol trong schematic khớp với thư viện `afe.kicad_sym`. |
| 5 | **Đồng bộ SCH-PCB** | U3 Component | Schematic khai báo `MCP1700-2802E` (2.8V), trong khi BOM và PCB dùng `MCP1700-3002E` (3.0V). | Cập nhật giá trị symbol U3 trong schematic thành `MCP1700-3002E`. |
| 6 | **Đồng bộ SCH-PCB** | J2 Connector | Schematic dùng symbol 38 chân gộp, trong khi PCB và BOM dùng cặp socket 1x19 `J2A` và `J2B`. | Đồng bộ định danh và footprint connector J2 thành 2 header 1x19. |
| 7 | **BOM** | Mã LCSC $100\,\text{k}\Omega$ & $10\,\text{k}\Omega$ | Trùng mã LCSC `C25804` cho cả $100\,\text{k}\Omega$ ($R_{10}-R_{12}$) và $10\,\text{k}\Omega$ ($R_{20}$). | Đổi mã LCSC của $100\,\text{k}\Omega$ ($R_{10}, R_{11}, R_{12}$) thành `C25803` (Uni-Royal 0603WAF1003T5E). Giữ `C25804` cho $10\,\text{k}\Omega$. |
| 8 | **DRC** | PCB Layout | 71 lỗi short-circuit và 39 lỗi tracks crossing trên lớp F.Cu, lỗi cầu hàn solder mask. | Thực hiện routing lại bằng script pcbnew chuyên dụng, phân tách rõ F.Cu và B.Cu, đưa DRC về 0 violations. |
| 9 | **CPL / Pos** | Dữ liệu Pick & Place | Tệp `AFE_ECG_PPG_PTT-pos.csv` xuất theo đơn vị inch gây sai lệch vị trí máy dán SMT. | Xuất lại tọa độ Pick&Place theo đơn vị chuẩn `mm` (millimeters). |

