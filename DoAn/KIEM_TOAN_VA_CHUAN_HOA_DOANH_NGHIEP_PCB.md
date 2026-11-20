# TÀI LIỆU KIỂM TOÁN KỸ THUẬT VÀ CHUẨN HÓA DOANH NGHIỆP (ENTERPRISE PCB AUDIT & DFM STANDARD)

**Dự án:** Hệ thống Cảm biến Y sinh & Mạch quản lý Nguồn Khóa Hè  
**Mã hồ sơ:** AUDIT-ENT-2026-REV3  
**Phạm vi kiểm toán:** 
1. Hệ thống thu nhận đồng thời ECG + PPG tính PAT/PTT (`DoAn/ECG_PPG_System`)
2. Thiết bị đo tín hiệu điện cơ EMG (`DoAn/EMG_Sensor`)
3. Mạch sạc pin Lithium USB-C TP4056 (`DoAn/USB_TypeC_TP4056_Charger`)
4. Đặc tả hệ thống mạch nguồn đa kênh (`THIET_KE_MACH_NGUON_SPEC.md`)

---

## PHẦN 1: BẢNG TỔNG HỢP KIỂM TOÁN VÀ PHÂN LOẠI LỖI (DEFECT MATRIX)

| Mã lỗi | Phân loại | Dự án | Mô tả khuyết tật | Hậu quả kỹ thuật / Doanh nghiệp | Biện pháp khắc phục chuẩn hóa |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ERR-01** | **Logic Analog** | `ECG_PPG_System` | Bộ so sánh $U_{3B}$ thiếu điện trở trễ (Hysteresis) | Rung đa xung (Comparator Chatter) khi sóng PPG biến thiên chậm qua ngưỡng, làm sai lệch thời gian PAT/PTT | Thêm điện trở hồi tiếp dương $R_{hyst} = 1\text{ M}\Omega - 2.2\text{ M}\Omega$ tạo trễ $\approx 20\text{ mV}$ (hoặc debounce $\ge 250\text{ ms}$ trên firmware) |
| **ERR-02** | **Quang học & Nguồn** | `ECG_PPG_System` | Điện trở phát LED $R_{19} = 220\ \Omega$ cố định | Dòng LED chỉ đạt $\approx 6.8\text{ mA}$ khi nuôi nguồn 3.3V, không đủ xuyên mô da dày | Nâng cấp $R_{19} = 120\ \Omega - 150\ \Omega$ hoặc thiết kế mạch nguồn dòng gương BJT/MOSFET |
| **ERR-03** | **DFM / Hình học** | `ECG_PPG_System` & `EMG_Sensor` | Đi dây góc vuông trực giao 90° trên toàn bộ mạch | Bẫy đọng axit (Acid traps) khi khắc hóa chất; tăng phát xạ EMI và méo trở kháng sóng y sinh | Vát góc 45° (Chamfered / Mitered) với $d = \min(0.35, L/2.1)$, triệt tiêu 100% góc vuông |
| **ERR-04** | **DFM / Tránh cầu chì hàn** | `EMG_Sensor` | Clearance cào bằng 0.20 mm; đệm nhiệt quá sát linh kiện dán | Đập mặt nạ hàn (solder mask dam) dễ bong tróc, gây dính cầu thiếc (solder bridge) khi hàn SMD | Tách netclass: đường nhạy cảm $\ge 0.5\text{ mm}$, phủ đồng $\text{clearance} = 0.25\text{ mm}$, $\text{thermal gap} = 0.25\text{ mm}$, $\text{bridge} = 0.40\text{ mm}$ |
| **ERR-05** | **DFM / Thoát chân (Fanout)** | `USB_TypeC_TP4056` | Track công suất $0.8\text{ mm}$ đâm thẳng vào pad connector USB-C pitch $0.5\text{ mm}$ | Gây 83 lỗi vi phạm đập hàn (solder mask bridge), chập chân $V_{BUS}$ sang $CC_1$, $CC_2$, $GND$ | Thoát chân (Fanout neck-down): thu hẹp track về $0.25\text{ mm}$ khi vào pad connector, ra khỏi pad $1\text{ mm}$ mới phình rộng $0.8\text{ mm}$ |
| **ERR-06** | **Tọa độ vật lý** | `USB_TypeC_TP4056` | Via `DW_OD` đặt tại `(7.5, 23.5)` cách pad chân 6 của $U_2$ chỉ $0.2\text{ mm}$ | Via có đường kính $0.8\text{ mm}$ đè trực tiếp lên pad IC, gây đoản mạch `DW_OD` vào `GND` | Dịch chuyển via sang vùng trống tại $x = 4.0\text{ mm}$ hoặc $y = 21.5\text{ mm}$ cách pad tối thiểu $0.6\text{ mm}$ |
| **ERR-07** | **Chuẩn SMT Doanh nghiệp** | Toàn bộ 4 bo | Thiếu điểm định vị quang học (Fiducial Markers) và Testpoint | Máy gắp linh kiện tự động (Pick & Place) không căn chỉnh tọa độ chính xác; khó kiểm thử tự động ICT | Bổ sung 3 điểm Fiducial Marker ở góc bo mạch và bổ sung Testpoint kiểm tra trên các bus tín hiệu |

---

## PHẦN 2: PHÂN TÍCH CHUYÊN SÂU HỆ THỐNG ECG + PPG (PAT/PTT)

### 1. Cơ chế tính thời gian truyền sóng mạch (PAT / PTT)
* **Khái niệm cốt lõi:**
  * **PAT (Pulse Arrival Time):** Khoảng thời gian từ lúc tâm thất trái khử cực (đỉnh R-peak trên tín hiệu ECG) đến khi sóng áp lực mạch máu truyền tới cảm biến quang PPG ngoại vi (đầu ngón tay hoặc dái tai).
  * **PTT (Pulse Transit Time):** Thời gian sóng mạch truyền qua một đoạn động mạch xác định (tỷ lệ nghịch với tốc độ sóng mạch PWV và độ cứng thành mạch, dùng để ước tính huyết áp không xâm lấn Cuffless Blood Pressure).
* **Kiến trúc phần cứng hiện tại:**
  * Kênh ECG: $U_1$ (AD623) có $\text{Gain} = 101$, tầng lọc HPF $0.48\text{ Hz}$, tầng Sallen-Key bậc 2 $\approx 40\text{ Hz}$ và Gain $10.1$ $\rightarrow$ Tổng độ khuếch đại: $A_{v} = 101 \times 10.1 \approx 1020$ lần. Tín hiệu đỉnh nhịp tim R-peak đạt biên độ $\approx 1.0\text{ V} - 2.5\text{ V}$ xoay quanh điện áp chuẩn $V_{REF}$.
  * Kênh PPG: Khối khuếch đại chuyển trở (TIA) $U_{2D}$ ($R_{18} = 1\text{ M}\Omega$, $C_{14} = 22\text{ pF}$) kết hợp tầng lọc dải bậc 2 và khuếch đại $U_{3A}$ ($A_v \approx 48$) $\rightarrow$ Tín hiệu sóng thể tích quang $PPG_{OUT}$ có biên độ đỉnh-đáy $0.5\text{ V} - 2.0\text{ V}$.
  * Kênh số $PULSE_{TRIG}$: Bộ so sánh $U_{3B}$ cắt ngưỡng $PPG_{OUT}$ để tạo sườn xung báo nhịp tim.
* **Lưu ý đo đạc chính xác:**
  * Để tính PAT/PTT chính xác trong nghiên cứu y sinh, **không được đo đơn thuần bằng khoảng cách thời gian giữa đỉnh R và sườn lên của $PULSE_{TRIG}$**, vì sườn của comparator phụ thuộc vào biên độ sóng PPG thay đổi theo trương lực mạch và áp lực đặt ngón tay.
  * **Chuẩn đo lường tối ưu:** Vi điều khiển (ESP32/STM32) phải đọc song song 2 kênh ADC (`ECG_OUT` và `PPG_OUT`) với tốc độ lấy mẫu $f_s \ge 1\text{ kHz}$. Sau đó chạy thuật toán tìm đạo hàm bậc nhất cực đại (Max Slope Point: $\frac{d(PPG)}{dt} = \max$) hoặc điểm chân sóng (Foot-to-Foot Method) để lấy thời điểm sóng mạch tới đích chuẩn xác dưới $1\text{ ms}$.

### 2. Sửa lỗi tầng so sánh (Comparator Hysteresis Modification)
Sơ đồ cải tiến tầng so sánh $U_{3B}$ chống hiện tượng rung xung:
```
           +-----------[ R_hyst = 1M - 2.2M ]------------+
           |                                             |
           |     |\                                      |
PPG_OUT ---+---->| \                                     |
                 |  \_________________ PULSE_TRIG -------+---> Ra Header J4 & LED D2
VREF_THR --------|- /
                 | /
                 |/ (U3B - MCP6002)
```
* **Tính toán độ trễ (Hysteresis Window):**
  * Điện áp bão hòa ngõ ra: $V_{OH} \approx V_{CC}$, $V_{OL} \approx 0\text{ V}$.
  * Khoảng trễ ngõ vào:
    $$\Delta V_H \approx (V_{OH} - V_{OL}) \times \frac{R_{in}}{R_{in} + R_{hyst}} \approx 3.3\text{V} \times \frac{10\text{ k}\Omega}{1000\text{ k}\Omega} \approx 33\text{ mV}$$
  * Biên độ trễ $33\text{ mV}$ lớn hơn biên độ nhiễu quang vi mô ($< 5\text{ mV}$), triệt tiêu hoàn toàn hiện tượng đóng mở chập chờn khi tín hiệu vượt ngưỡng.

---

## PHẦN 3: BỘ QUY TẮC THIẾT KẾ DOANH NGHIỆP (IPC & DFM STANDARDS)

Để các bản vẽ đủ điều kiện chuyển giao cho dây chuyền sản xuất công nghiệp hàng loạt (SMT Pick & Place, Reflow Oven, Wave Soldering), toàn bộ các đồ án phải tuân thủ nghiêm ngặt các quy tắc sau:

### 1. Quy chuẩn đi dây và phân tách Netclass (IPC-2221B Section 6 & 10)
* **Góc chuyển hướng đường mạch:**
  * Cấm tuyệt đối góc vuông $90^\circ$ và góc nhọn $< 90^\circ$.
  * Toàn bộ các góc đổi hướng phải vát $45^\circ$ (Chamfered) hoặc cung tròn (Curved).
* **Bề rộng đường mạch (Trace Width):**
  * Đường tín hiệu analog y sinh nhạy cảm (`EMG+`, `EMG-`, `RA_FILT`, `LA_FILT`, `PD_ANODE`): $0.25\text{ mm} - 0.30\text{ mm}$.
  * Đường tín hiệu số / logic (`PULSE_TRIG`, `PROG`): $0.25\text{ mm}$.
  * Đường nguồn công suất ($V_{BUS}$, $V_{BAT}$, $V_{CC}$): $0.60\text{ mm} - 1.00\text{ mm}$ (Đảm bảo độ sụt áp $< 1\%$ và nhiệt độ tăng $< 10^\circ\text{C}$ ở dòng $1\text{ A}$).
* **Khoảng cách cách ly (Clearance):**
  * Giữa các đường analog nhạy cảm với đường nguồn / xung số: $\ge 0.50\text{ mm}$ (20 mil).
  * Giữa linh kiện dán SMD với lớp phủ đồng GND: $0.25\text{ mm} - 0.30\text{ mm}$.
  * Giữa các pad của IC fine-pitch (pitch $0.5\text{ mm}$ - $0.65\text{ mm}$): $0.15\text{ mm} - 0.20\text{ mm}$.

### 2. Quy chuẩn thoát chân linh kiện chân dày (DFM Fanout & Neck-Down)
* Đối với các linh kiện chân dày như cổng USB Type-C 16-pin (pitch $0.5\text{ mm}$) và IC chân nhỏ (SOT-23-6, TSSOP-8, SOIC-8):
  * Đường mạch kết nối vào pad phải có bề rộng bằng hoặc nhỏ hơn bề rộng pad ($W \le 0.25\text{ mm}$).
  * Chiều dài đoạn thu hẹp (Neck-down length) tối thiểu $0.8\text{ mm} - 1.2\text{ mm}$ tính từ mép pad trước khi phình rộng ra kích thước đường nguồn chính.
  * Cấm tuyệt đối đi track vuông góc cắt ngang qua các pad lân cận.

### 3. Quy chuẩn lỗ khoan và Via (Via-in-Pad & Anti-Wicking)
* **Khoảng cách Via tới Pad (Via-to-Pad Clearance):** Tối thiểu $0.25\text{ mm}$ tính từ mép via đến mép pad dán SMD. Cấm đặt via chồng lên mép pad SMD để chống hiện tượng thoát thiếc (Solder Wicking - thiếc hàn chảy tụt xuống lỗ via làm hở chân linh kiện trong lò reflow).
* **Thermal Vias cho IC công suất:** IC sạc TP4056 có tản nhiệt đáy (Exposed Pad 9) phải bố trí ma trận $3 \times 3 = 9$ via tản nhiệt (đường kính $0.6\text{ mm}$, mũi khoan $0.3\text{ mm}$) nối trực tiếp xuống mặt phẳng đồng lớp dưới (B.Cu) để tản nhiệt khi sạc dòng $1\text{ A}$.

### 4. Điểm định vị quang học (Fiducial Markers - IPC-7351B)
* Mỗi bo mạch công nghiệp bắt buộc có **3 điểm Fiducial Marker** bố trí không đối xứng ở 3 góc bo mạch:
  * Điểm tròn đồng (Copper Pad): Đường kính $\varnothing 1.00\text{ mm}$.
  * Cửa sổ mở mặt nạ hàn (Solder Mask Opening): Đường kính $\varnothing 2.00\text{ mm}$.
  * Vùng cấm đi dây và cấm linh kiện xung quanh: Bán kính $3.00\text{ mm}$.

### 5. Điểm kiểm thử tự động (Testpoints for In-Circuit Testing - ICT)
* Đặt các Testpoint dạng pad tròn bề mặt SMD (đường kính $1.0\text{ mm} - 1.2\text{ mm}$) trên lớp `B.Cu` hoặc `F.Cu`:
  * `TP_VBUS`, `TP_VBAT`, `TP_VCC`, `TP_GND`.
  * `TP_VREF` (Kiểm tra điện áp chuẩn 1.65V / 2.5V).
  * `TP_ECG_OUT`, `TP_PPG_OUT`, `TP_PULSE_TRIG`.
  * `TP_EMG_RAW`, `TP_EMG_ENV`.

---

## PHẦN 4: HƯỚNG DẪN KHẮC PHỤC TRIỆT ĐỂ (STEP-BY-STEP REMEDIATION)

### 1. Bo mạch EMG Sensor (`DoAn/EMG_Sensor`)
* **Bước 1:** Kích hoạt script [DoAn/EMG_Sensor/scripts/apply_emg_chamfered.py](DoAn/EMG_Sensor/scripts/apply_emg_chamfered.py).
* **Bước 2:** Chạy lệnh KiCad CLI phủ lại đồng và kiểm tra DRC:
  ```bash
  kicad-cli pcb drc --output DoAn/EMG_Sensor/outputs/EMG_Sensor-drc.rpt DoAn/EMG_Sensor/EMG_Sensor.kicad_pcb
  ```
* **Bước 3:** Tái xuất bộ Gerber sạch góc 45° vào `DoAn/EMG_Sensor/outputs/`.

### 2. Bo mạch ECG + PPG System (`DoAn/ECG_PPG_System`)
* **Bước 1:** Áp dụng thuật toán vát góc chamfering tương tự lên file [DoAn/ECG_PPG_System/scripts/master_ecg_router.py](DoAn/ECG_PPG_System/scripts/master_ecg_router.py).
* **Bước 2:** Bổ sung điện trở trễ $R_{29} = 1\text{ M}\Omega$ song song giữa chân 5 và chân 7 của IC $U_3$ (MCP6002).
* **Bước 3:** Điều chỉnh $R_{19} = 120\ \Omega$ để tối ưu dòng phát quang khi nuôi hệ thống từ cổng 3.3V của ESP32.
* **Bước 4:** Xuất lại gói sản xuất nén [Gerber_ECG_PPG_System_Production.zip](DoAn/ECG_PPG_System/outputs/Gerber_ECG_PPG_System_Production.zip).

### 3. Bo mạch Sạc USB-C TP4056 (`DoAn/USB_TypeC_TP4056_Charger`)
* **Bước 1:** Dời via `DW_OD` tại tọa độ `(7.5, 23.5)` sang vị trí an toàn `(4.5, 22.0)`.
* **Bước 2:** Định tuyến lại các đường nguồn $V_{BUS}$ và $V_{BAT}$:
  * Đoạn thoát chân qua các pad $J_1$ (A4, B4, A9, B9) và $Q_1$ (pad 1, 2, 3) áp dụng neck-down $0.25\text{ mm}$.
  * Mở rộng lên $0.80\text{ mm}$ khi ra khỏi khu vực connector và IC.
* **Bước 3:** Xóa bỏ hoàn toàn 83 lỗi solder mask bridge và 8 lỗi unconnected items, đảm bảo DRC đạt 0 lỗi tuyệt đối trước khi đóng gói sản xuất.
