# TÀI LIỆU PHÂN TÍCH ĐỐI SÁNH THƯƠNG MẠI & KINH NGHIỆM THIẾT KẾ PHẦN CỨNG Y SINH / NGUỒN (BENCHMARKING & HARDWARE LESSONS LEARNED)

**Tác giả:** Kỹ sư Trưởng Thiết kế Phần cứng & Hệ thống Nhúng  
**Mã tài liệu:** HW-BENCHMARK-2026-REV1  
**Phạm vi:** Đối sánh kỹ thuật chi tiết giữa 4 đồ án trong workspace với các sản phẩm thương mại hàng đầu thế giới (Texas Instruments, Analog Devices, SparkFun, MyoWare, OpenBCI, Apple/Fitbit).

---

## MỤC LỤC
1. [Đối sánh Kỹ thuật Thiết bị đo Điện cơ EMG (EMG Sensor)](#1-doi-sanh-ky-thuat-thiet-bi-do-dien-co-emg)
2. [Đối sánh Kỹ thuật Hệ thống ECG + PPG tính PAT/PTT](#2-doi-sanh-ky-thuat-he-thong-ecg--ppg-tinh-patptt)
3. [Đối sánh Kỹ thuật Mạch Quản lý Sạc Pin USB-C Li-ion](#3-doi-sanh-ky-thuat-mach-quan-ly-sac-pin-usb-c-li-ion)
4. [Các Bẫy Thiết kế Phần cứng Thực chiến (Hardware Traps & Lessons Learned)](#4-cac-bay-thiet-ke-phan-cung-thuc-chien)
5. [Lộ trình Nâng cấp Chuẩn Công nghiệp Hóa (Industrial Grade Roadmap)](#5-lo-trinh-nang-cap-chuan-cong-nghiep-hoa)

---

## 1. ĐỐI SÁNH KỸ THUẬT THIẾT BỊ ĐO ĐIỆN CƠ EMG

### 1.1. Bảng đối sánh với các sản phẩm thương mại

| Tiêu chí kỹ thuật | Mạch Đồ án Hiện tại (`DoAn/EMG_Sensor`) | MyoWare 2.0 (Advancer Tech / SparkFun) | DFRobot Gravity EMG Sensor | Delsys Trigno Wireless EMG (Chuẩn Y tế / Nghiên cứu) |
| :--- | :--- | :--- | :--- | :--- |
| **Kiến trúc mạch** | Analog rời: AD623 + MCP6004 + ICL7660 | ASIC/Op-Amp tích hợp chuyên dụng | Analog rời: AD8221 / TLC2272 | Cảm biến thông minh: Active Electrode + 16-bit A/D + Bluetooth LE |
| **Tầng tiền khuếch đại** | $U_1$ (AD623ARZ) In-Amp rời | Low-power Instrumentation Amp | AD8221 Precision In-Amp | Custom Ultra-low-noise Bio-potential AFE |
| **Hệ số nén đồng pha (CMRR)** | $\approx 90\text{ dB}$ (tại Gain = 100) | $\ge 100\text{ dB}$ | $\approx 100\text{ dB}$ | $> 110\text{ dB}$ (ở 50/60 Hz) |
| **Mức nhiễu nền (Noise Floor)** | $\approx 1.5\ \mu\text{V}_{RMS}$ | $\approx 1.0\ \mu\text{V}_{RMS}$ | $\approx 1.2\ \mu\text{V}_{RMS}$ | $< 0.75\ \mu\text{V}_{RMS}$ (Siêu tĩnh) |
| **Băng thông lọc (Bandwidth)** | $20\text{ Hz} - 500\text{ Hz}$ (Bandpass bậc 4) | $20\text{ Hz} - 450\text{ Hz}$ | $15\text{ Hz} - 1500\text{ Hz}$ | $20\text{ Hz} - 450\text{ Hz}$ (Chuẩn SENIAM) |
| **Ngõ ra tín hiệu (Outputs)** | **Kép:** `RAW_EMG` + `ENV_EMG` (Envelope) | **Kép:** RAW + Rectified Envelope | `ENV` đơn kênh (Đã tích phân) | Kỹ thuật số số hóa tại chỗ (Digital Data Stream) |
| **Cách tiếp xúc điện cực** | Dây dẫn cáp cắm từ Header J1 | **Snap trực tiếp trên bo** (Gắn thẳng lên da) | Cáp cắm jack 3.5mm ra 3 điện cực | Thanh bạc nguyên chất gắn mặt đáy (Dry Silver Bars) |
| **Bảo vệ ESD điện cực** | Chưa tích hợp diode TVS kẹp dòng | Tích hợp kẹp diode TVS đa kênh | Tích hợp kẹp diode kép | Đạt chuẩn an toàn y tế IEC 60601-1 (ESD 15kV) |

### 1.2. Đánh giá ưu điểm và nhược điểm thực tế
* **Ưu thế của mạch đồ án:**
  * Việc tích hợp **khối tách bao hình tín hiệu chủ động (Active Envelope Detector)** với bộ chỉnh lưu toàn kỳ dùng Op-Amp lý tưởng giúp triệt tiêu hoàn toàn điện áp sụt $0.7\text{V}$ của diode thông thường. Điều này cho phép vi điều khiển phổ thông (Arduino, ESP32) lấy mẫu tín hiệu cơ bắp ở tốc độ rất chậm ($100\text{ Hz}$) qua ADC để điều khiển tay giả hoặc cơ cấu chấp hành mà không cần thuật toán lọc số phức tạp.
  * Việc có sẵn chip tạo nguồn âm `ICL7660` giúp mạch chạy được với nguồn đơn $5\text{V}$ nhưng vẫn có điện áp đối xứng $\pm 5\text{V}$, giúp tín hiệu `RAW_EMG` dao động đối xứng quanh 0V mà không bị cắt ngọn.
* **Hạn chế lớn nhất so với MyoWare 2.0:**
  * **Nhiễu rung dây cáp (Cable Motion Artifact):** Mạch đồ án dẫn dây từ điện cực vào bo mạch. Trong thực tế, khi cơ bắp co giật hoặc người dùng chạy nhảy, dây cáp cọ xát và rung lắc sinh ra điện tích tĩnh điện (hiệu ứng áp điện / triboelectric) với biên độ có thể lên tới $50\text{ mV}$ ở dải tần số thấp ($5 - 30\text{ Hz}$). MyoWare giải quyết triệt để vấn đề này bằng cách gắn trực tiếp 3 cúc bấm kim loại (Snap connectors) ngay dưới đáy PCB $\rightarrow$ Toàn bộ bo mạch dán chặt lên cơ bắp, không có 1 milimét dây dẫn nào bị rung lắc.

---

## 2. ĐỐI SÁNH KỸ THUẬT HỆ THỐNG ECG + PPG TÍNH PAT/PTT

### 2.1. Bảng đối sánh với các giải pháp công nghiệp

| Tiêu chí | Mạch Đồ án Hiện tại (`ECG_PPG_System`) | TI Reference Design (TIDM-BIOSIGNAL / TIDA-01580) | ADI Solution (AD8232 + MAX30102 / ADPD188GG) | Thiết bị đeo tay thương mại (Apple Watch, Withings) |
| :--- | :--- | :--- | :--- | :--- |
| **Cấu trúc phần cứng** | Op-Amp rời: AD623 + MCP6004 + MCP6002 | Hybrid: ADS1292R (ECG) + AFE4490/4404 (PPG) | Modular: AD8232 (AFE analog) + MAX30102 (Quang I2C) | SoC tích hợp tùy biến (Custom ASIC + DSP + PMU) |
| **Đồng bộ thời gian (Sync)** | Phụ thuộc ngắt MCU ngoài qua header J4 | **Phần cứng đồng bộ:** Chung Master Clock ($\Delta t < 1\ \mu\text{s}$) | Lệch pha phụ thuộc độ trễ bus I2C ($\sim 1 - 5\text{ ms}$) | Đồng bộ bằng bộ định thời nội hardware timer |
| **Chế độ phát LED PPG** | **DC liên tục:** Điện trở hạn dòng $220\ \Omega$ | **Pulsed Current Mode:** Xung lập trình ($50 - 200\ \mu\text{s}$) | **Pulsed Mode:** DAC dòng điều khiển tự động | Xung điều chế thích nghi theo màu da & cử động |
| **Triệt tiêu ánh sáng môi trường** | Không có (Phải che chắn quang học) | **Ambient Light Cancellation (ALC) tự động** | Tích hợp bộ lọc quang học + trừ nền số | Tích hợp thuật toán Ambient Subtraction đa bước sóng |
| **Kênh chân Right Leg (DRL)** | $U_{2B}$ Inverting Driver ($R_{12} = 390\text{ k}\Omega$) | Tích hợp trong ADS1292 (RLD Amplifier nội) | Chân RLD tích hợp trên AD8232 | Điện cực vòng mặt lưng khung vỏ đồng hồ |
| **Chỉ số đo lường** | Xuất dạng sóng analog + Xung so sánh | Truyền dữ liệu số 24-bit qua SPI | Dữ liệu nhịp tim số qua I2C + Sóng analog | Tính toán trực tiếp PAT/PTT $\rightarrow$ Huyết áp (Cuffless BP) |

### 2.2. Phân tích bẫy kỹ thuật trong việc đo PAT / PTT
1. **Bẫy đo PAT qua ngưỡng tĩnh Comparator:**
   * Trong mạch hiện tại, tầng $U_{3B}$ so sánh sóng PPG với điện áp $VREF\_THR$ cố định để tạo xung $PULSE\_TRIG$. 
   * **Sai số vật lý:** Biên độ sóng PPG thay đổi liên tục theo nhịp thở (hiệu ứng Respiratory-Induced Intensity Variations - RIIV), nhiệt độ ngón tay và độ co giãn của mạch máu. Khi biên độ PPG giảm xuống một nửa, thời điểm tín hiệu chạm ngưỡng $VREF\_THR$ sẽ **bị trễ đi từ $30\text{ ms} - 80\text{ ms}$** dù thời gian truyền sóng thực tế của máu không hề thay đổi!
   * **Chuẩn công nghiệp:** Không bao giờ dùng bộ so sánh cắt ngưỡng cố định để tính PAT. Các sản phẩm của TI và thiết bị y tế luôn số hóa dạng sóng PPG qua ADC với tốc độ $\ge 500\text{ Hz}$, sau đó áp dụng một trong 3 thuật toán nhận diện mốc thời gian sóng mạch:
     - *Phương pháp chân sóng (Foot-to-Foot Method):* Tìm điểm giao cắt của tiếp tuyến dốc nhất với đường đẳng điện (ít bị ảnh hưởng nhất bởi sóng phản xạ thành mạch).
     - *Phương pháp đạo hàm cực đại (Max Derivative Point):* Tìm điểm $\frac{d(PPG)}{dt} = \max$ (tương ứng với thời điểm vận tốc máu gia tăng nhanh nhất).
     - *Phương pháp đạo hàm bậc hai (Second Derivative PPG - APG):* Nhận diện đỉnh gia tốc sóng $a$-wave để lấy mốc thời gian chuẩn xác dưới $1\text{ ms}$.

2. **Bẫy ánh sáng môi trường (Ambient Light Interference):**
   * Do mạch dùng LED sáng liên tục, ánh sáng từ đèn tuýp huỳnh quang hoặc đèn LED trong phòng (chớp ở tần số $100\text{ Hz}$ hoặc $120\text{ Hz}$ do lưới điện xoay chiều) sẽ lọt vào photodiode.
   * Dù mạch có tầng lọc thông thấp, nhiễu quang này vẫn có thể tạo ra các gợn sóng hình sin đè lên tín hiệu PPG, gây kích hoạt sai bộ so sánh $U_{3B}$.

---

## 3. ĐỐI SÁNH KỸ THUẬT MẠCH QUẢN LÝ SẠC PIN USB-C LI-ION

### 3.1. Bảng đối sánh với các mạch sạc thương mại

| Tiêu chí | Mạch Đồ án Hiện tại (`USB_TypeC_TP4056`) | Module Phổ thông (HW-373 / AliExpress) | Adafruit PowerBoost / Micro-Lipo (MCP73871) | Texas Instruments BQ24075 (Chuẩn Công nghiệp) |
| :--- | :--- | :--- | :--- | :--- |
| **Topology sạc** | Tuyến tính (Linear CC/CV) | Tuyến tính (Linear CC/CV) | Tuyến tính với Smart Power-Path | Switch-mode hoặc Linear Power-Path (DPPM) |
| **Quản lý đường nguồn (Power-Path)** | **KHÔNG CÓ:** Tải nối chung với pin | **KHÔNG CÓ** | **CÓ (Load Sharing):** Tự chuyển nguồn USB/Pin | **Dynamic Power-Path Management (DPPM)** |
| **Dòng sạc tối đa** | $1.0\text{ A}$ (cài bằng $R_{PROG} = 1.2\text{ k}\Omega$) | $1.0\text{ A}$ | $500\text{ mA} - 1.0\text{ A}$ | Lập trình từ $100\text{ mA} - 1.5\text{ A}$ qua chân ISET |
| **Cổng giao tiếp USB-C** | 16-pin USB-C có $R_{CC1}, R_{CC2} = 5.1\text{ k}\Omega$ | 16-pin (thường thiếu 1 trở CC gây kén sạc C-to-C) | Micro-USB hoặc USB-C chuẩn | USB-C PD tương thích hoàn toàn |
| **Hiệu suất năng lượng** | $\approx 65\% - 75\%$ (Tỏa nhiệt trên IC) | $\approx 65\% - 75\%$ | $\approx 70\% - 80\%$ | $> 90\%$ (ở các dòng sạc Switching) |
| **Giám sát nhiệt độ pin (NTC)** | Chân TEMP nối đất (Bỏ qua chức năng NTC) | Chân TEMP nối đất | Tích hợp chân đọc NTC thermistor | Tích hợp JEITA Profile (Tự giảm dòng khi pin nóng) |
| **Bảo vệ pin** | Độc lập: DW01A + FS8205A (Dual N-MOS) | DW01A + FS8205A | Tích hợp bảo vệ quá áp/ngắn mạch trên IC | Bảo vệ đa tầng: OVP, UVP, OCP, OTP, Timer Timeout |

### 3.2. Bẫy chia dòng và ngắt sạc (The Power-Path Dilemma)
* **Khuyết tật lớn nhất của mạch sạc không có Power-Path:**
  * Giả sử bạn cấp nguồn cho một hệ thống vi điều khiển (ESP32) ăn dòng $150\text{ mA}$ kết nối vào cổng $V_{OUT}$ của mạch sạc.
  * Khi cắm cáp USB sạc pin: IC TP4056 bơm dòng $1000\text{ mA}$. Dòng này bị chia làm hai nhánh: $150\text{ mA}$ nuôi ESP32 và $850\text{ mA}$ nạp vào pin.
  * Khi pin nạp đầy đến $4.2\text{V}$, theo nguyên lý chuẩn sạc Li-ion, dòng sạc sẽ giảm dần về $0$. TP4056 được lập trình để **ngắt sạc khi dòng sạc giảm xuống $10\%$ dòng định mức ($I_{TERM} = 100\text{ mA}$)**.
  * Tuy nhiên, vì ESP32 luôn rút $150\text{ mA}$, tổng dòng ra khỏi TP4056 luôn $\ge 150\text{ mA} > 100\text{ mA}$. Do đó, **TP4056 KHÔNG BAO GIỜ NGẮT SẠC (Never Terminate)**! Pin bị ngâm liên tục ở điện áp cực đại $4.2\text{V}$ và nhiệt độ cao trong nhiều ngày $\rightarrow$ Tăng tốc độ lão hóa pin, gây hiện tượng phồng pin hoặc cháy nổ (Thermal Runaway).
* **Bài học thương mại từ Adafruit & TI:**
  * Trong các sản phẩm chuyên nghiệp, luôn bố trí mạch **Power-Path (hoặc Load Sharing circuit)**:
    ```
    VBUS (USB 5V) ------+----[ Diodes / P-MOSFET ]----+---> Cấp nguồn TẢI (Load)
                        |                             |
                     [TP4056]                         |
                        |                             |
                      [Pin] --------------------------+ (Khi rút USB, mở P-MOSFET cấp pin cho tải)
    ```
  * Khi cắm USB: Tải được ngắt hoàn toàn khỏi pin và ăn điện trực tiếp từ USB $5\text{V}$. TP4056 chỉ nuôi duy nhất một mình viên pin, giúp phát hiện dòng ngắt sạc $100\text{ mA}$ chuẩn xác $100\%$.

---

## 4. CÁC BẪY THIẾT KẾ PHẦN CỨNG THỰC CHIẾN (HARDWARE TRAPS)

### Bẫy 1: Tản nhiệt kém trên IC sạc tuyến tính (Linear Charger Thermal Dissipation)
* **Hiện tượng:** Khi nạp cho pin cạn ($3.0\text{V}$) với dòng $1\text{ A}$ từ nguồn USB $5\text{V}$:
  $$P_{dissipated} = (V_{IN} - V_{BAT}) \times I_{CHG} = (5.0\text{V} - 3.0\text{V}) \times 1.0\text{A} = 2.0\text{ Watt}$$
* Với vỏ đóng gói ESOP-8 có nhiệt trở tiếp giáp $\theta_{JA} \approx 50^\circ\text{C/W}$:
  $$\Delta T = 2.0\text{W} \times 50^\circ\text{C/W} = 100^\circ\text{C} \implies T_{junction} \approx 25^\circ\text{C} + 100^\circ\text{C} = 125^\circ\text{C}$$
* TP4056 sẽ chạm ngay ngưỡng bảo vệ quá nhiệt ($140^\circ\text{C}$) và tự động giảm dòng sạc xuống còn $300 - 400\text{ mA}$.
* **Kinh nghiệm thực chiến:** Phải thiết kế **Thermal Pad (Pad 9)** dưới bụng IC với tối thiểu $3 \times 3 = 9$ lỗ via (đường kính $0.6\text{ mm}$, mũi khoan $0.3\text{ mm}$) nối trực tiếp sang lớp đồng đáy (Bottom Copper) có diện tích tản nhiệt $\ge 200\text{ mm}^2$.

### Bẫy 2: Không đồng bộ trở kháng da-điện cực (Impedance Imbalance) trên mạch ECG/EMG
* **Hiện tượng:** Trở kháng tiếp xúc của da người qua lớp tế bào chết dao động từ $10\text{ k}\Omega$ đến $200\text{ k}\Omega$ tùy độ ẩm và vị trí dán.
* Nếu điện cực dương ($RA$) có trở kháng $50\text{ k}\Omega$ nhưng điện cực âm ($LA$) có trở kháng $100\text{ k}\Omega$, thì nhiễu đồng pha từ lưới điện $50\text{ Hz}$ ($V_{CM}$) khi đi qua cầu chia trở kháng ngõ vào sẽ bị chuyển đổi thành **nhiễu vi sai (Differential Mode Noise)**:
  $$V_{diff\_noise} \approx V_{CM} \times \frac{\Delta Z_{skin}}{Z_{in\_amplifier}}$$
* Dù IC $AD623$ có CMRR lên tới $100\text{ dB}$, nhiễu $50\text{ Hz}$ vẫn lọt vào khuếch đại làm mất hoàn toàn sóng ECG/EMG!
* **Kinh nghiệm thực chiến:**
  1. Trở kháng ngõ vào của tầng tiền khuếch đại phải cực lớn ($Z_{in} \ge 10^{10}\ \Omega$ nhờ ngõ vào FET của In-Amp).
  2. Bắt buộc dùng **mạch lái chân phải DRL (Driven Right Leg)** để đảo pha nhiễu đồng pha và dập ngược lại cơ thể, nâng CMRR thực tế từ $60\text{ dB}$ lên $> 100\text{ dB}$.

### Bẫy 3: Bẫy ăn mòn axit (Acid Traps) và phản xạ sóng do góc đi dây 90°
* Khi đi dây góc vuông 90°, tại đỉnh nhọn góc trong, nước rửa bo mạch và hóa chất ăn mòn (Ferric Chloride hoặc Ammonium Persulfate) bị đọng lại do sức căng bề mặt. Lớp axit này tiếp tục ăn mòn ngầm chân đường đồng sau khi xuất xưởng, dẫn đến đứt mạch sau vài tháng sử dụng.
* Ngoài ra, góc 90° làm điện dung ký sinh tại góc tăng lên:
  $$C_{corner} \approx \frac{0.001 \times W \times \sqrt{\epsilon_r}}{1.414}$$
  gây ra sự bất liên tục trở kháng đối với các đường xung sườn dốc (như $PULSE\_TRIG$).
* **Kinh nghiệm thực chiến:** Luôn đặt chế độ đi dây góc vát $45^\circ$ hoặc bo tròn (Curved traces) cho toàn bộ bo mạch.

---

## 5. LỘ TRÌNH NÂNG CẤP CHUẨN CÔNG NGHIỆP HÓA (INDUSTRIAL ROADMAP)

Để đưa các bản thiết kế từ mức độ "Đồ án Khóa Hè" lên mức độ **"Sản phẩm Thương mại hóa / Chuyển giao Doanh nghiệp"**, lộ trình nâng cấp gồm 3 giai đoạn:

```
[ GIAI ĐOẠN 1: DFM CLEAN ]      --->   [ GIAI ĐOẠN 2: HARDWARE HARDENING ]   --->   [ GIAI ĐOẠN 3: EDGE INTELLIGENCE ]
- Sửa sạch 100% lỗi DRC                - Bổ sung Power-Path sạc pin                - Tích hợp BLE MCU (nRF52840/ESP32-S3)
- Vát góc 45 độ toàn bộ                - Bổ sung trễ Hysteresis cho xung           - Lọc thích nghi nhiễu cử động LMS
- Bổ sung Fiducials & Testpoints        - Bảo vệ ESD TVS kẹp điện cực               - Thuật toán tính PAT/PTT Foot-to-Foot
- Tách netclass clearance              - Tích hợp mạch kẹp sạc C-to-C              - Đồng bộ thời gian phần cứng < 10us
```

### 1. Nâng cấp Bo mạch EMG:
* Tích hợp 3 khuy bấm điện cực đúc kim loại (ECG/EMG Snap Plugs) trực tiếp lên mặt đáy của bo mạch.
* Bổ sung IC bảo vệ tĩnh điện TVS Diode chuyên dụng (như `USBLC6-2SC6` hoặc `TPD4E001`) bảo vệ 3 đường điện cực chống hiện tượng phóng tĩnh điện khi người dùng chạm tay vào điện cực.

### 2. Nâng cấp Bo mạch ECG + PPG:
* Thêm điện trở $R_{29} = 1.5\text{ M}\Omega$ tạo trễ cho tầng so sánh $U_{3B}$.
* Thêm một BJT/MOSFET điều chế xung LED (Pulsed LED) nối với một chân điều khiển từ Header J4 để vi điều khiển có thể chớp LED ở tần số $200\text{ Hz}$, tiết kiệm $80\%$ pin và loại bỏ $100\%$ nhiễu ánh sáng đèn phòng.

### 3. Nâng cấp Bo mạch USB-C Charger:
* Thiết kế lại bo mạch áp dụng kỹ thuật Fanout Neck-down giải quyết dứt điểm 83 lỗi solder mask bridge.
* Bổ sung mạch Load Sharing (1 P-MOSFET AO3401 + 1 Schottky Diode SS34) để cô lập pin khỏi tải khi đang cắm sạc.
