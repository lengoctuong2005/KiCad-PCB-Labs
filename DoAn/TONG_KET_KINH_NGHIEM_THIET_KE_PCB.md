# CẨM NANG TỔNG KẾT KINH NGHIỆM THIẾT KẾ PCB THỰC CHIẾN (HARDWARE & PCB LESSONS LEARNED)

**Dự án:** Tổng hợp Đồ án Thiết kế Phần cứng & Cảm biến Y sinh  
**Tài liệu tham chiếu:** HW-HANDBOOK-2026-FINAL  
**Tác giả:** Kỹ sư Trưởng Thiết kế Phần cứng & DFM

---

## LỜI NÓI ĐẦU
Trong quá trình rà soát, kiểm toán và hoàn thiện 4 đồ án phần cứng trong workspace (`EMG_Sensor`, `ECG_PPG_System`, `USB_TypeC_TP4056_Charger` và `Mạch nguồn đa kênh`), chúng ta đã bóc tách hàng loạt các khuyết tật từ mức độ nguyên lý mạch (Schematic), hình học đường mạch (Layout Routing), đến khả năng chế tạo gia công (DFM/DFA) và an toàn y sinh.

Tài liệu này đúc kết **7 Trụ cột Kinh nghiệm Thiết kế PCB Xương Máu** giúp kỹ sư tránh lặp lại các sai lầm kinh điển khi chuyển giao bản vẽ từ màn hình máy tính sang dây chuyền sản xuất công nghiệp thực tế.

---

## 1. TRỤ CỘT 1: HÌNH HỌC ĐƯỜNG MẠCH & BẪY ĂN MÒN AXIT (ROUTING GEOMETRY)

### 1.1. Tại sao cấm tuyệt đối góc vuông 90° và góc nhọn (< 90°)?
* **Bẫy đọng axit (Acid Traps):**
  * Trong quy trình ăn mòn mạch in bằng hóa chất (Etching), dung dịch ăn mòn lọt vào góc nhọn hoặc góc vuông bên trong sẽ bị giữ lại do sức căng bề mặt.
  * Khi bo mạch đi qua công đoạn rửa nước, hóa chất tại khe hẹp 90° không thoát ra kịp, tiếp tục ăn mòn ngầm chân đường đồng sau khi đã phủ sơn hàn. Hậu quả là đường mạch bị mỏng dần và **tự đứt ngầm sau 3 - 6 tháng sử dụng**.
* **Bất liên tục trở kháng (Impedance Discontinuity):**
  * Tại góc rẽ 90°, bề rộng hiệu dụng của đường mạch tăng đột ngột lên gấp $\sqrt{2} \approx 1.414$ lần so với đoạn thẳng.
  * Sự tăng diện tích này làm tăng điện dung ký sinh tại góc ($C_{corner}$), gây giảm đột ngột trở kháng đặc tính $Z_0$, tạo ra sóng phản xạ (signal reflection) và phát xạ nhiễu điện từ (EMI) đối với các xung số sườn dốc (như xung $PULSE\_TRIG$).
* **Méo hài tín hiệu vi sai y sinh:**
  * Với tín hiệu điện thế cơ bắp EMG hoặc điện tim ECG (biên độ micro-Volt), góc 90° tạo ra sự lệch pha vi mô giữa hai nhánh vi sai (`EMG+` và `EMG-`), làm suy giảm nghiêm trọng hệ số nén đồng pha (CMRR).

### 1.2. Quy tắc chuẩn hóa:
* **Luôn vát góc 45° (Chamfered / Mitered Traces):** Thay thế 1 góc vuông 90° bằng 2 góc uốn $135^\circ$ với khoảng cách vát $d = \min(0.35\text{ mm}, L/2.1)$.
* **Bo cong góc (Curved Traces):** Đối với các đường vi sai analog nhạy cảm, ưu tiên đi dây theo cung tròn mượt mà (Circular Arc Routing).

---

## 2. TRỤ CỘT 2: KHOẢNG CÁCH CÁCH LY, ĐẬP PHỦ HÀN & ĐỆM NHIỆT (CLEARANCE & DFM)

### 2.1. Bẫy cào bằng Clearance 0.20 mm
* Việc áp dụng một khoảng cách cách ly duy nhất $0.20\text{ mm}$ (8 mil) cho toàn bộ bo mạch là sai lầm phổ biến:
  * **Với nguồn & mass:** $0.20\text{ mm}$ là quá sát đối với các vùng phủ đồng lớn, làm tăng điện dung ký sinh xuống mass.
  * **Với tín hiệu y sinh:** Đường điện cực cực nhạy đặt cách đường nguồn 5V chỉ $0.20\text{ mm}$ sẽ bị ghép nhiễu xung (capacitive crosstalk) từ gợn sóng nguồn.
* **Quy tắc phân tầng Netclass:**
  * *Tín hiệu vi sai y sinh:* Clearance $\ge 0.50\text{ mm}$ (20 mil) và có đường bao chắn mass (Guard Ring).
  * *Đường nguồn công suất:* Clearance $0.30\text{ mm} - 0.40\text{ mm}$.
  * *Tín hiệu logic thông thường:* Clearance $0.25\text{ mm}$.

### 2.2. Đập cản mặt nạ hàn (Solder Mask Dam) & Cầu thiếc (Solder Bridge)
* Khi nhà máy phủ lớp sơn hàn (Solder Mask), khoảng hở giữa 2 chân dán SMD liền kề phải đủ lớn để lớp sơn bám dính tạo thành một "con đê" ngăn cách (gọi là Solder Mask Dam).
* Nếu khoảng hở mặt nạ hàn $< 0.10\text{ mm}$ (4 mil), lớp sơn sẽ bị bong tróc trong quá trình gia công. Khi hàn tay hoặc hàn quét thiếc, thiếc hàn nóng chảy sẽ trào qua và dính hai chân IC lại với nhau (**Hiện tượng Solder Bridge**).
* **Đệm nhiệt (Thermal Relief):**
  * Khi chân linh kiện nối vào vùng phủ đồng lớn (Copper Pour GND), phải dùng hoa đệm nhiệt (Thermal Relief) gồm 4 cầu nối:
    * Khoảng hở nhiệt (`thermal_gap`): $\ge 0.25\text{ mm}$.
    * Bề rộng cầu nhiệt (`thermal_bridge_width`): $0.40\text{ mm}$.
  * Không nối trực tiếp pad vào mặt phẳng đồng (Solid Connection) trừ pad tản nhiệt, vì nhiệt độ mỏ hàn sẽ bị mặt phẳng đồng hút sạch, dẫn đến hiện tượng **mối hàn nguội (Cold Solder Joint)**, thiếc không ngấu chân linh kiện.

---

## 3. TRỤ CỘT 3: KỸ THUẬT THOÁT CHÂN LINH KIỆN DÀY (TRACE ESCAPE & FANOUT NECK-DOWN)

### 3.1. Bài học xương máu từ cổng USB Type-C 16-pin (0.5 mm pitch)
* Cổng USB Type-C 16-pin có khoảng cách giữa tâm 2 chân liên tiếp chỉ $0.50\text{ mm}$, khoảng hở giữa mép 2 pad dán chỉ khoảng $0.20\text{ mm}$.
* **Nguyên nhân gây 83 lỗi DRC trên mạch TP4056:** Script cũ đã kéo đường mạch nguồn $0.80\text{ mm}$ nối thẳng từ chân 4 ($V_{BUS}$) sang chân 9 ($V_{BUS}$). Bề rộng $0.80\text{ mm}$ lớn gấp 4 lần khoảng cách chân, đè ngang qua 4 chân ở giữa ($CC_1, D+, D-, SBU$), gây chập mạch và phá vỡ hoàn toàn mặt nạ hàn!
* **Nguyên tắc vàng khi thoát chân (Fanout Neck-Down):**
  1. Đường mạch khi chạm vào pad dán của IC chân dày hoặc connector USB-C **bắt buộc phải có bề rộng $\le$ bề rộng của pad** ($W_{escape} \le 0.25\text{ mm}$).
  2. Đường mạch phải đi thẳng vuông góc thoát ra khỏi cụm chân linh kiện ít nhất $1.0\text{ mm} - 1.5\text{ mm}$.
  3. Chỉ sau khi đã ra khỏi vùng chân dày, đường mạch mới được phép phình to lên kích thước $0.60\text{ mm} - 1.00\text{ mm}$ để gộp dòng.

---

## 4. TRỤ CỘT 4: QUY TẮC ĐẶT VIA & CHỐNG HIỆN TƯỢNG THOÁT THIẾC (SOLDER WICKING)

### 4.1. Bẫy đặt Via đè lên Pad dán SMD
* Trong lò hàn nung đối lưu (Reflow Oven), kem hàn (solder paste) in trên pad SMD sẽ nóng chảy thành chất lỏng.
* Nếu đặt lỗ via đè lên mép pad SMD hoặc quá sát pad ($< 0.20\text{ mm}$): Do hiện tượng mao dẫn (Capillary action), toàn bộ thiếc hàn nóng chảy sẽ **chảy tụt qua lỗ via xuống mặt đáy PCB** (Hiện tượng **Solder Wicking**). Kết quả là chân linh kiện SMD phía trên không còn thiếc hàn, gây hở mạch hoàn toàn (Tombstoning hoặc Open Pin).
* **Quy chuẩn:** Giữ khoảng cách từ mép via đến mép pad dán SMD tối thiểu $0.25\text{ mm} - 0.30\text{ mm}$. Nếu bắt buộc phải đặt via trong pad (Via-in-Pad đối với chip BGA), phải yêu cầu nhà máy gia công công nghệ bít lỗ via bằng nhựa epoxy mạ đồng phẳng (Capped & Plated Vias - IPC-4761 Type VII).

### 4.2. Ma trận Via tản nhiệt (Thermal Vias)
* Đối với IC công suất có miếng đồng tản nhiệt dưới bụng (như chân số 9 của TP4056): Bắt buộc bố trí ma trận $3 \times 3 = 9$ via (đường kính $0.6\text{ mm}$, mũi khoan $0.3\text{ mm}$) nối trực tiếp xuống lớp đồng đáy (Bottom Copper) để thoát nhiệt, tránh kích hoạt tính năng giảm dòng ngắt sạc do quá nhiệt.

---

## 5. TRỤ CỘT 5: THIẾT KẾ ANALOG Y SINH NHẠY CẢM (BIOPOTENTIAL AFE)

### 5.1. Bẫy rung lắc dây cáp điện cực (Cable Motion Artifact)
* Tín hiệu EMG co cơ chỉ có biên độ từ $50\ \mu\text{V} - 2\text{ mV}$. Khi người dùng cử động, dây cáp dẫn điện cực bị uốn cong và cọ xát với quần áo sinh ra điện tích tĩnh điện (Triboelectric Effect) lên tới $50\text{ mV}$ ở tần số thấp ($5 - 20\text{ Hz}$).
* Nhiễu rung cáp này có biên độ lớn gấp 50 lần tín hiệu sinh học thật, làm bão hòa tầng tiền khuếch đại AD623.
* **Giải pháp chuẩn:** Học tập thiết kế MyoWare 2.0: Tích hợp trực tiếp khuy bấm kim loại (Snap Plugs) lên mặt đáy bo mạch để dán chặt toàn bộ mạch lên cơ bắp, loại bỏ 100% dây cáp trung gian.

### 5.2. Mạch so sánh (Comparator) bắt buộc phải có trễ Hysteresis
* Tín hiệu thể tích quang PPG biến thiên rất chậm (khoảng 1 - 2 nhịp/giây) và luôn có nhiễu vi mô.
* Nếu dùng bộ so sánh không có trễ: Khi tín hiệu chạm ngưỡng so sánh, nhiễu vi mô sẽ làm điện áp ngõ vào trồi sụt qua lại ngưỡng hàng chục lần trong vài mili-giây $\rightarrow$ Ngõ ra phát ra một chùm xung liên tục (Hiện tượng **Comparator Chatter**), làm vi điều khiển đếm sai nhịp tim và phá hỏng phép tính thời gian truyền sóng PAT/PTT.
* **Giải pháp:** Luôn mắc điện trở hồi tiếp dương $R_{hyst} \approx 1\text{ M}\Omega - 2.2\text{ M}\Omega$ từ ngõ ra về ngõ vào không đảo để tạo cửa sổ trễ $\Delta V_h \approx 20\text{ mV} - 35\text{ mV}$.

### 5.3. Chuẩn đo PAT/PTT khoa học:
* Không đo PAT/PTT bằng xung cắt ngưỡng của Comparator.
* Lấy mẫu sóng qua bộ ADC tốc độ $\ge 500\text{ Hz}$ và chạy giải thuật tìm điểm đạo hàm cực đại $\frac{d(PPG)}{dt} = \max$ hoặc điểm chân sóng (Foot-to-Foot) đối chiếu với đỉnh R-peak của ECG để sai số thời gian $< 1\text{ ms}$.

---

## 6. TRỤ CỘT 6: QUẢN LÝ NĂNG LƯỢNG & SẠC PIN LITHIUM (POWER-PATH MANAGEMENT)

### 6.1. Bẫy chia dòng khi sạc pin (The Load Sharing Dilemma)
* Trong các mạch sạc pin đơn giản (như module TP4056 phổ thông), ngõ ra $V_{BAT}$ vừa nối vào pin vừa nối thẳng vào tải nuôi vi điều khiển (ESP32).
* **Hậu quả nghiêm trọng:**
  * Khi cắm sạc: Dòng từ TP4056 vừa sạc pin vừa nuôi ESP32 ($150\text{ mA}$).
  * Khi pin đầy $4.2\text{V}$, dòng nạp pin giảm dần về 0. Tuy nhiên vì ESP32 vẫn tiếp tục ăn $150\text{ mA}$, tổng dòng ra khỏi TP4056 không bao giờ giảm xuống dưới ngưỡng ngắt sạc $100\text{ mA}$ ($I_{TERM} = C/10$).
  * TP4056 **không bao giờ ngắt sạc**, ngâm pin liên tục ở điện áp cực đại $4.2\text{V}$ trong nhiều ngày $\rightarrow$ Pin bị chai cực nhanh, phồng pin và nguy cơ cháy nổ!
* **Giải pháp:** Bắt buộc bổ sung mạch **Power-Path (Load Sharing)** dùng 1 P-MOSFET (AO3401) + 1 Schottky Diode (SS34) + 1 Điện trở kéo lên $100\text{ k}\Omega$. Khi cắm sạc USB, tải được cấp nguồn trực tiếp từ USB $5\text{V}$, ngắt pin ra khỏi tải để TP4056 ngắt sạc an toàn.

---

## 7. TRỤ CỘT 7: TIÊU CHUẨN DOANH NGHIỆP CHO SẢN XUẤT HÀNG LOẠT (SMT & ICT)

### 7.1. Điểm định vị quang học (Fiducial Markers - IPC-7351B)
* Máy gắp linh kiện tự động (SMT Pick & Place) sử dụng camera quang học độ nét cao để nhận diện tọa độ bo mạch trước khi gắp chip.
* Bắt buộc bố trí **3 điểm Fiducial Marker** ở 3 góc bo mạch không đối xứng:
  * Điểm đồng tròn: Đường kính $\varnothing 1.00\text{ mm}$.
  * Vùng mở mặt nạ hàn: Đường kính $\varnothing 2.00\text{ mm}$.
  * Vùng cấm đi dây xung quanh: Bán kính $3.00\text{ mm}$.

### 7.2. Điểm kiểm tra tự động (Testpoints for ICT)
* Đặt các điểm kiểm tra dạng pad tròn bề mặt SMD ($\varnothing 1.0\text{ mm} - 1.2\text{ mm}$) trên lớp đáy (B.Cu) để máy kiểm thử kim que (Bed-of-Nails Tester) có thể đo tự động:
  * Nguồn: `TP_VBUS`, `TP_VBAT`, `TP_3V3`, `TP_GND`.
  * Tín hiệu: `TP_VREF`, `TP_ECG_RAW`, `TP_PPG_RAW`, `TP_PULSE_TRIG`, `TP_EMG_ENV`.

### 7.3. Ký hiệu phân cực và định vị trên lớp in lụa (Silkscreen Polarity)
* Tất cả linh kiện có phân cực bắt buộc phải có ký hiệu rõ ràng trên lớp in lụa:
  * IC: Đánh dấu chấm tròn tại Pin 1 hoặc vát góc thân chip.
  * Diode/LED: Đánh dấu vạch dày tại cực Cathode.
  * Tụ hóa / Tụ Tantalum: Đánh dấu dấu cộng (+) tại cực dương.
  * Connector: In rõ tên tín hiệu của từng chân (`GND`, `VCC`, `TX`, `RX`).

---

## BẢNG TỔNG KẾT QUY CHUẨN KỸ THUẬT SẢN XUẤT (QUICK REFERENCE CARD)

| Thông số thiết kế | Giá trị tối thiểu cho phép | Giá trị đề xuất công nghiệp (Recommended) |
| :--- | :--- | :--- |
| **Bề rộng đường mạch tín hiệu (Trace Width)** | $0.15\text{ mm}$ (6 mil) | $0.25\text{ mm} - 0.30\text{ mm}$ (10 - 12 mil) |
| **Bề rộng đường nguồn 1A (Power Trace)** | $0.50\text{ mm}$ (20 mil) | $0.80\text{ mm} - 1.00\text{ mm}$ (32 - 40 mil) |
| **Khoảng cách cách ly (Clearance)** | $0.15\text{ mm}$ (6 mil) | $0.25\text{ mm} - 0.30\text{ mm}$ (10 - 12 mil) |
| **Khoảng cách cách ly tín hiệu y sinh** | $0.30\text{ mm}$ (12 mil) | $\ge 0.50\text{ mm}$ (20 mil) + Guard Trace |
| **Đập cản mặt nạ hàn (Solder Mask Dam)** | $0.08\text{ mm}$ (3.15 mil) | $\ge 0.10\text{ mm}$ (4 mil) |
| **Độ mở mặt nạ hàn (Solder Mask Clearance)**| $0.025\text{ mm}$ (1 mil) | $0.05\text{ mm}$ (2 mil) |
| **Khe hở đệm nhiệt (Thermal Relief Gap)** | $0.20\text{ mm}$ (8 mil) | $0.25\text{ mm}$ (10 mil) |
| **Bề rộng cầu nhiệt (Thermal Bridge Width)** | $0.30\text{ mm}$ (12 mil) | $0.40\text{ mm}$ (16 mil) |
| **Khoảng cách Via tới Pad SMD (Via-to-Pad)** | $0.20\text{ mm}$ (8 mil) | $\ge 0.25\text{ mm}$ (10 mil) (Chống thoát thiếc) |
| **Đường kính lỗ khoan via tối thiểu (Drill)** | $0.30\text{ mm}$ (12 mil) | $0.30\text{ mm} - 0.40\text{ mm}$ |
| **Vát góc chuyển hướng** | Tuyệt đối không dùng 90° | Luôn vát góc $45^\circ$ hoặc bo cong |
