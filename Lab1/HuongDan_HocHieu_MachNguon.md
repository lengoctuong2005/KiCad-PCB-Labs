# HƯỚNG DẪN HỌC HIỂU TOÀN DIỆN MẠCH NGUỒN ĐA NĂNG
## MÔN HỌC: THIẾT KẾ MẠCH IN PCB VỚI KICAD (LAB 01)

> **Mục tiêu tài liệu:** Giúp bạn hiểu sâu bản chất nguyên lý hoạt động của mạch nguồn mẫu, tự tin vẽ sơ đồ khối trên giấy (Câu 3) và giải thích rành mạch chức năng của từng khối/linh kiện (Câu 2) khi giảng viên vấn đáp.

---

# PHẦN 1: BỨC TRANH TOÀN CẢNH — TẠI SAO CẦN MẠCH NGUỒN NÀY?

Trong thiết kế phần cứng điện tử và hệ thống nhúng (Embedded Systems), các kỹ sư thường xuyên cần:
1. **Nguồn +5V:** Cấp cho các cảm biến công nghiệp, relay, màn hình LCD, IC logic cổ điển.
2. **Nguồn +3.3V:** Cấp cho các vi điều khiển hiện đại (ESP32, STM32, Arduino ARM, cảm biến I2C/SPI). Nếu cấp 5V vào các chip này, chúng sẽ **cháy ngay lập tức**.
3. **Nguồn âm -5V:** Kết hợp với nguồn +5V để tạo **nguồn đối xứng đôi (±5V)**. Nguồn này bắt buộc phải có khi làm việc với các mạch khuếch đại thuật toán (Op-Amp), xử lý tín hiệu âm thanh (Audio AC) hoặc cảm biến tương tự (Analog Sensor).
4. **Cổng nạp USB - UART:** Giúp máy tính có thể gửi lệnh điều khiển, nạp chương trình và đọc dữ liệu từ vi điều khiển lên màn hình.
5. **Nguồn phát xung Clock (NE555):** Tạo ra tín hiệu sóng vuông để làm xung nhịp kiểm tra mạch đếm số hoặc đo đạc máy hiện sóng (Oscilloscope).

Bo mạch nguồn đa năng này tích hợp **toàn bộ 5 nhu cầu trên vào một bo mạch nhỏ gọn**, lấy nguồn trực tiếp từ cổng USB máy tính.

---

# PHẦN 2: GIẢI THÍCH CHI TIẾT 7 KHỐI CHỨC NĂNG (BÀI TẬP 2)

---

### KHỐI 1: KHỐI NGUỒN ĐẦU VÀO (POWER INPUT)
* **Linh kiện:** Cổng Micro-USB (`USB1`), Công tắc gạt (`SW1`), Tụ lọc ngõ vào (`C1` - 10µF).
* **Bản chất hoạt động:**
  * Cáp USB từ máy tính có 4 dây chính: Chân 1 (V_BUS = +5V), Chân 2 (D-), Chân 3 (D+), Chân 4 (GND). Cổng `USB1` tiếp nhận nguồn 5V này.
  * Công tắc `SW1` là công tắc chính (Master Switch). Khi gạt ON, dòng điện mới chạy vào toàn bộ bo mạch. Khi gạt OFF, mạch ngắt hoàn toàn để đảm bảo an toàn khi hàn hoặc cắm dây.
  * **Tại sao cần tụ C_1 (10µF)?** Khi bạn cắm cáp USB vào máy tính, sẽ xuất hiện hiện tượng "xung điện quá độ" (Voltage Spike) và sụt áp tức thời. Tụ C_1 đóng vai trò như một "bình tích nước", hấp thụ các xung áp cao và xả điện bù đắp tức thì, giúp đường nguồn 5V đầu vào luôn phẳng và ổn định.

---

### KHỐI 2: KHỐI ỔN ÁP 3.3V (LINEAR REGULATOR AMS1117-3.3)
* **Linh kiện:** IC `AMS1117-3.3` (`U2`), Tụ gốm ngõ vào `C2` (100nF), Tụ gốm ngõ ra `C3` (10µF).
* **Bản chất hoạt động:**
  * `AMS1117-3.3` là IC ổn áp tuyến tính kiểu LDO (Low Dropout). Nhiệm vụ của nó là nhận điện áp đầu vào +5V và ghìm điện áp đầu ra luôn chính xác ở mức **+3.3V DC** (dòng chịu tải tối đa 1 Ampe).
  * **Nguyên lý:** Nó hoạt động như một biến trở tự động. Phần điện áp thừa (5V - 3.3V = 1.7V) nhân với dòng điện tiêu thụ sẽ bị biến đổi thành **nhiệt năng** tỏa ra trên lưng IC (chân Tab tản nhiệt).
  * **Tại sao cần 2 tụ C_2 (100nF) và C_3 (10µF)?**
    * Tụ nhỏ C_2 = 100nF = 0.1µF (tụ gốm MLCC): Có trở kháng rất thấp ở tần số cao, chuyên dùng để **triệt tiêu nhiễu cao tần** từ máy tính.
    * Tụ lớn C_3 = 10µF: Đặt ở ngõ ra để **giữ ổn định vòng phản hồi** của IC AMS1117, chống hiện tượng mạch tự kích dao động (tự phát sinh sóng nhiễu).

---

### KHỐI 3: KHỐI TẠO NGUỒN ÂM -5V (CHARGE PUMP INVERTER LM2776)
* **Linh kiện:** IC `LM2776` (`U1`), Tụ bơm bay C_PUMP (`C4` - 1µF), Tụ lọc ngõ ra C_OUT (`C5` - 1µF đến 10µF).
* **Bản chất hoạt động:**
  * Bình thường, để tạo điện áp âm từ nguồn dương, người ta phải dùng biến áp hoặc cuộn cảm (rất to, nặng và sinh ra từ trường gây nhiễu).
  * IC `LM2776` sử dụng công nghệ **Bơm nạp điện tích (Switched-Capacitor Charge Pump)** với tần số đóng ngắt siêu nhanh (2 MHz):
    * **Nửa chu kỳ 1:** Các khóa điện tử bên trong chip đóng lại, nối tụ `C4` vào nguồn +5V và GND -> Tụ `C4` được nạp đầy điện thế 5V (cực dương ở chân trên, cực âm ở chân dưới).
    * **Nửa chu kỳ 2:** Các khóa bên trong đảo chiều: Chân dương của tụ `C4` bị dập xuống GND (0V) -> Lập tức chân âm của tụ `C4` bị tụt xuống thế điện -5V và xả toàn bộ năng lượng âm này sang tụ lưu trữ `C5`.
    * Quá trình này lặp lại 2 triệu lần mỗi giây (2 MHz) tạo ra đường nguồn **-5V DC liên tục** phẳng mịn.
* **Ý nghĩa:** Cung cấp nguồn âm cho các mạch Op-Amp (như LM358, TL072, NE5532) để xử lý tín hiệu xoay chiều hoàn chỉnh cả bán kỳ âm và bán kỳ dương mà không bị méo tiếng.

---

### KHỐI 4: KHỐI CHUYỂN ĐỔI USB SANG UART (CHIP CP2102)
* **Linh kiện:** IC `CP2102` (`U3`), Tụ lọc nguồn `C6` (100nF), `C7` (4.7µF).
* **Bản chất hoạt động:**
  * Máy tính giao tiếp bằng chuẩn **USB** (truyền vi sai 2 dây D+ và D- với các gói tin phức tạp).
  * Vi điều khiển lại giao tiếp bằng chuẩn **UART** (chuẩn truyền nối tiếp đơn giản gồm 2 chân TX - Truyền và RX - Nhận).
  * IC `CP2102` đóng vai trò là **"Thông dịch viên phần cứng"**:
    * Khi máy tính gửi dữ liệu qua USB -> CP2102 dịch thành chuỗi xung nhị phân UART đẩy ra chân TXD vào vi điều khiển.
    * Khi vi điều khiển gửi dữ liệu qua chân RXD -> CP2102 đóng gói lại theo chuẩn USB gửi ngược về máy tính hiển thị lên Serial Monitor.
  * `CP2102` đã tích hợp sẵn mạch dao động thạch anh bên trong chip nên bo mạch không cần hàn thêm thạch anh ngoài, giúp mạch cực kỳ gọn gàng.

---

### KHỐI 5: KHỐI TẠO XUNG VUÔNG ĐA HÀI PHI ỔN (IC NE555)
* **Linh kiện:** IC Định thì `NE555` (`U4`), Điện trở định thì `R3`, `R4` (10kΩ), Tụ định thì `C8` (10µF), Tụ chống nhiễu chân Control `C9` (10nF).
* **Bản chất hoạt động:**
  * Mạch mắc ở chế độ **Đa hài phi ổn (Astable Multivibrator)**: Mạch không có trạng thái ổn định nào mà liên tục tự động chuyển đổi qua lại giữa mức Cao (High ~ 5V) và mức Thấp (Low ~ 0V).
  * **Chu trình nạp - xả của tụ C_8:**
    1. Dòng điện từ nguồn 5V nạp vào tụ C_8 qua bộ đôi điện trở (R_3 + R_4). Điện áp trên tụ tăng dần từ (1/3)*V_CC lên (2/3)*V_CC. Trong thời gian này, ngõ ra chân 3 (`OUT`) ở mức **CAO** (LED sáng).
    2. Khi điện áp trên tụ đạt ngưỡng (2/3)*V_CC, bộ so sánh bên trong kích hoạt chân số 7 (`DISCHARGE`) dập xả điện tích của tụ C_8 qua điện trở R_4 xuống mass (GND). Điện áp tụ giảm từ (2/3)*V_CC xuống (1/3)*V_CC. Trong thời gian này, ngõ ra chân 3 chuyển về mức **THẤP** (LED tắt).
    3. Khi điện áp chạm đáy (1/3)*V_CC, chu trình nạp lại bắt đầu.
* **Công thức tính toán tần số dao động:**
  ```
f = 1.44 / ((R3 + 2*R4) * C8)
```
  *Ví dụ với mạch của chúng ta:* R_3 = 10kΩ, R_4 = 10kΩ, C_8 = 10µF = 10 x 10^-6F:
  f = (1.44 / (10000 + 2 x 10000) x 10 x 10^-6) = (1.44 / 30000 x 10^-5) = (1.44 / 0.3) = 4.8 Hz
  *(Nghĩa là đèn LED ngõ ra sẽ nhấp nháy khoảng 4.8 lần mỗi giây, mắt người có thể quan sát rõ ràng).*

---

### KHỐI 6: KHỐI LED HIỂN THỊ VÀ ĐIỆN TRỞ HẠN DÒNG
* **Linh kiện:** 5 Diode LED (`LED1` đến `LED5`) và các Điện trở hạn dòng `R1`, `R2`, `R5`, `R6`, `R7` (330Ω đến 1kΩ).
* **Bản chất hoạt động:**
  * LED (Light Emitting Diode) là linh kiện bán dẫn chỉ cho dòng điện chạy qua theo một chiều từ Anode sang Cathode khi điện áp phân cực thuận vượt qua điện áp mở ngưỡng (V_F ≈ 1.8V - 2.2V).
  * **Tại sao BẮT BUỘC phải có điện trở hạn dòng R?**
    * LED có nội trở gần như bằng 0 khi đã mở. Nếu đấu trực tiếp LED vào nguồn 5V mà không có điện trở, dòng điện qua LED sẽ tăng vọt vô hạn theo định luật Ohm -> **LED sẽ bốc khói và cháy ngay lập tức trong 1 giây**.
    * Điện trở R làm nhiệm vụ ghìm dòng điện ở mức an toàn khoảng 5mA - 10mA để LED vừa đủ sáng đẹp mà không bị nóng.
  * **Công thức tính điện trở hạn dòng:**
    R = (V_CC - V_LED / I_LED) = (5V - 2.0V / 0.01A) = 300 Ω -> Chọn điện trở chuẩn thị trường là  330 Ω.

---

### KHỐI 7: KHỐI HEADER VÀ CONNECTOR RA CHÂN NGOẠI VI
* **Linh kiện:** Các rào cắm đực `Pin Header` bước chân chuẩn 2.54mm (`J1` – `J5`), Cầu nối ngắn mạch `Jumper Shunt`.
* **Bản chất hoạt động:**
  * Chuẩn cắm **2.54mm (0.1 inch)** là tiêu chuẩn quốc tế của toàn bộ các bo mạch thử nghiệm (Breadboard) và dây cắm Dupont.
  * Khối này gom toàn bộ các kết quả xử lý của 6 khối trên đưa ra mép bo mạch:
    * Chân nguồn: `+5V`, `+3.3V`, `-5V`, `GND` để cắm cấp nguồn sang mạch khác.
    * Chân tín hiệu UART: `TXD`, `RXD`, `DTR`, `RTS`.
    * Chân tín hiệu xung Clock: `PULSE_OUT`.
  * `Jumper`: Dùng để cấu hình nhanh bằng tay (ví dụ: cắm jumper để chọn cấp nguồn 3.3V hoặc 5V cho vi điều khiển ngoại vi).

---

# PHẦN 3: HƯỚNG DẪN TỰ VẼ SƠ ĐỒ KHỐI TRÊN GIẤY (BÀI TẬP 3)

Để đạt điểm tối đa khi vẽ sơ đồ khối trên giấy, bạn hãy dùng thước kẻ và bút vẽ theo các bước chuẩn mực sau:

### 1. Bố cục không gian trên trang giấy:
* **Bên trái cùng:** Vẽ khối **NGUỒN VÀO (Micro-USB 5V & SW1)**.
* **Ở giữa:** Vẽ 4 khối xử lý song song xếp thẳng hàng từ trên xuống dưới:
  1. Khối Ổn áp 3.3V (`AMS1117-3.3`)
  2. Khối Nguồn âm -5V (`LM2776`)
  3. Khối Chuyển đổi USB sang UART (`CP2102`)
  4. Khối Tạo xung vuông (`NE555`)
* **Bên phải cùng:** Vẽ 2 khối tiếp nhận:
  1. Khối **LED Hiển thị trạng thái**
  2. Khối **Header & Connector ra chân cắm**

---

### 2. Sơ đồ mẫu chi tiết để vẽ theo:

```
[ CỔNG MICRO-USB 5V ]
         |
    [ CÔNG TẮC SW1 ]
         |
         +============================= ĐƯỜNG NGUỒN CHÍNH +5V ============================+
         |                                |                            |                  |
         v                                v                            v                  v
+-------------------+            +-------------------+        +-----------------+ +---------------+
|   KHỐI ỔN ÁP      |            |   KHỐI NGUỒN ÂM   |        | KHỐI USB-UART   | | KHỐI TẠO XUNG |
|   AMS1117-3.3     |            |     LM2776        |        |    CP2102       | |    NE555      |
+-------------------+            +-------------------+        +-----------------+ +---------------+
         |                                |                            |                  |
   [Nguồn +3.3V]                    [Nguồn -5V]                [Tín hiệu TX/RX]     [Xung vuông Out]
         |                                |                            |                  |
         +--------------------------------+----------------------------+------------------+
                                          |
                                          +----------------------------+
                                          |                            |
                                          v                            v
                               +---------------------+      +---------------------+
                               | KHỐI HEADER RA CHÂN |      | KHỐI LED BÁO NGUỒN  |
                               | (J1, J2, J3, J4, J5)|      |     VÀ TÍN HIỆU     |
                               +---------------------+      +---------------------+
```

---

# PHẦN 4: 10 CÂU HỎI VẤN ĐÁP THỰC HÀNH HAY GẶP NHẤT

Khi thầy cô kiểm tra bài Lab 1 hoặc duyệt sơ đồ ở các buổi sau, đây là 10 câu hỏi giảng viên hay hỏi nhất:

1. **Hỏi:** *Tại sao mạch này không dùng cuộn cảm hay máy biến áp mà vẫn tạo ra được điện áp âm -5V?*
   * **Trả lời:** Dạ thưa thầy/cô, mạch dùng IC `LM2776` hoạt động theo nguyên lý Bơm nạp điện tích (Switched-Capacitor Charge Pump), đóng ngắt tụ bay C_4 ở tần số cao 2MHz để đảo cực tính điện áp nạp, do đó không cần cuộn cảm.

2. **Hỏi:** *Tụ C_2 (100nF) và tụ C_3 (10µF) ở khối ổn áp AMS1117 khác nhau ở điểm nào?*
   * **Trả lời:** Tụ nhỏ 100nF (tụ gốm) có đáp ứng tần số cao tốt dùng để lọc nhiễu tần số cao; tụ lớn 10µF dùng để tích trữ bù năng lượng và giữ ổn định hồi tiếp ngõ ra của IC ổn áp.

3. **Hỏi:** *Tại sao chip CP2102 trong sơ đồ không thấy gắn thạch anh dao động bên ngoài?*
   * **Trả lời:** Do chip `CP2102` của Silicon Labs đã tích hợp sẵn mạch dao động nội (Internal Clock) độ chính xác cao ±0.25% bên trong lõi chip.

4. **Hỏi:** *Nếu muốn tăng hoặc giảm tần số nhấp nháy của IC NE555 thì phải thay đổi linh kiện nào?*
   * **Trả lời:** Ta thay đổi giá trị của điện trở định thì R_3, R_4 hoặc tụ điện C_8 theo công thức f = (1.44 / (R_3 + 2R_4)C_8). Tăng giá trị R hoặc C sẽ làm giảm tần số (chớp chậm hơn).

5. **Hỏi:** *Chân Tab to ở giữa của IC AMS1117 đóng gói SOT-223 nối với chân nào?*
   * **Trả lời:** Chân Tab tản nhiệt được nối thông trực tiếp với chân số 2 (V_OUT = +3.3V), vừa dẫn điện vừa giúp tản nhiệt ra mặt đồng PCB.

6. **Hỏi:** *Nếu vô tình nối ngược cực LED thì LED có bị cháy không?*
   * **Trả lời:** LED chịu được một mức điện áp ngược nhất định (thường khoảng 5V). Khi cắm ngược, LED không sáng và không bị cháy ngay nếu áp ngược không vượt quá giới hạn V_R(max) của LED.

7. **Hỏi:** *Tại sao cổng USB có 5 chân nhưng ta chỉ dùng 4 chân?*
   * **Trả lời:** Chân thứ 4 là chân ID (thường dùng cho chức năng USB OTG trên điện thoại). Ở mạch nhận nguồn thông thường, chân ID được để hở (NC - No Connect).

8. **Hỏi:** *Dòng điện ngõ ra tối đa của khối nguồn âm LM2776 là bao nhiêu?*
   * **Trả lời:** Dạ là 200 mA, đủ cấp cho các tầng tiền khuếch đại Op-Amp và mạch xử lý tín hiệu analog.

9. **Hỏi:** *Footprint của IC CP2102 là gì và có điểm gì đặc biệt khi hàn mạch in?*
   * **Trả lời:** Đóng gói dạng QFN-28 (5 x 5 mm). Điểm đặc biệt là các chân nằm dưới đáy chip và có một miếng đồng lớn (Exposed Pad) ở chính giữa đáy chip để nối đất (GND) và tản nhiệt, khi hàn PCB cần dùng máy khò nhiệt hoặc hàn đối lưu (reflow).

10. **Hỏi:** *Định luật Ohm được ứng dụng như thế nào trong khối LED hiển thị?*
    * **Trả lời:** Dùng để tính toán điện trở hạn dòng R = (V_CC - V_F / I_F) nhằm đảm bảo dòng qua LED không vượt quá dòng định mức (10mA - 20mA).
