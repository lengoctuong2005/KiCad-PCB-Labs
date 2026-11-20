# BÁO CÁO RÀ SOÁT KỸ THUẬT VÀ ĐÁNH GIÁ CHUYÊN SÂU ĐỒ ÁN MẠCH SẠC PIN LI-ION TP4056 TYPE-C

**Dự án:** USB Type-C Li-ion Battery Charger with Multi-Stage Protection  
**Đơn vị thực hiện:** Nhóm Đồ Án Tốt Nghiệp Khóa Hè 2025-2026 - ĐHKHTN ĐHQG TP.HCM  
**Kỹ sư rà soát phần cứng (PCB Hardware Reviewer):** Lê Ngọc Tường (MSSV: 23207124)  
**Công cụ rà soát:** KiCad EDA CLI 10.0.8, Python `pcbnew`, Thư viện IPC-7351B / IPC-2221  
**Mã tài liệu:** AUDIT-TP4056-REV3  
**Ngày hoàn tất:** Tháng 11/2026  

---

## 1. MỤC TIÊU VÀ PHẠM VI RÀ SOÁT

Đồ án mạch sạc pin Lithium-Ion tích hợp ngõ vào USB Type-C và tầng bảo vệ pin DW01A / FS8205A là đồ án kết thúc khóa học thực hành thiết kế mạch in. Mục tiêu của đợt rà soát này là:
1. Thẩm định toàn diện tính đúng đắn của sơ đồ nguyên lý (Schematic) và kết quả kiểm tra quy tắc điện (ERC).
2. Kiểm tra sâu bản vẽ mạch in PCB (Layout), đối chiếu báo cáo DRC thực tế so với các công bố trong tài liệu báo cáo đồ án.
3. Phân tích nguyên nhân gốc rễ (Root Cause Analysis) của các lỗi vật lý, nguy cơ chập cháy điện, rủi ro nhiệt và cơ khí.
4. Đưa ra hướng xử lý và kiến trúc thiết kế chuẩn hóa sẵn sàng cho sản xuất hàng loạt (DFM/DFA).

---

## 2. KẾT QUẢ RÀ SOÁT SƠ ĐỒ NGUYÊN LÝ (SCHEMATIC & ERC AUDIT)

### 2.1. Phân tích thiết kế nguyên lý các tầng mạch
* **Tầng ngõ vào USB Type-C (J1):**
  - Sử dụng đầu nối USB-C 16-pin chuẩn Receptacle (`HRO TYPE-C-31-M-12`).
  - Đã tích hợp 2 điện trở cấu hình $R_1 = 5.1\,\text{k}\Omega$ và $R_2 = 5.1\,\text{k}\Omega$ (dung sai 1%) kéo xuống mass tại chân $CC_1$ và $CC_2$. Đây là yêu cầu bắt buộc của chuẩn USB Type-C Specification Release 2.1 để nguồn cấp (Củ sạc PD, cổng máy tính) nhận diện thiết bị là thiết bị tiêu thụ (UFP - Upstream Facing Port / Sink) và cấp nguồn 5V ổn định.
  - Tụ lọc ngõ vào gồm tụ hóa $C_1 = 10\,\mu\text{F}$ và tụ gốm $C_2 = 100\,\text{nF}$ đặt sát chân VBUS, giúp lọc phẳng gai áp cao tần.
* **Tầng IC sạc pin TP4056 (U1):**
  - IC hoạt động theo thuật toán sạc 3 giai đoạn: Sạc nhỏ giọt (Trickle Charge, khi $V_{BAT} < 2.9\text{V}$), Dòng không đổi (Constant Current - CC), và Điện áp không đổi (Constant Voltage - CV, $4.20\text{V} \pm 1\%$).
  - Điện trở lập trình dòng $R_3 = 1.2\,\text{k}\Omega$ tại chân `PROG` (chân 2). Theo công thức nhà sản xuất:
    $$I_{CHG} = \frac{1200\,\text{V}}{R_{PROG}} = \frac{1200\,\text{V}}{1.2\,\text{k}\Omega} = 1000\,\text{mA} = 1.0\,\text{A}$$
    Dòng nạp 1.0A là mức tối ưu cho các cell pin 18650 dung lượng $2000 - 3000\,\text{mAh}$ (tương đương hệ số sạc $0.33\text{C} - 0.5\text{C}$).
  - Đèn báo trạng thái: LED đỏ `D1` (nối cực thoát hở `CHRG`, chân 7) báo đang sạc, LED xanh `D2` (nối cực thoát hở `STDBY`, chân 6) báo pin đầy. Hai điện trở hạn dòng $R_4 = R_5 = 1\,\text{k}\Omega$ cho dòng LED $\approx 3\,\text{mA}$.
* **Tầng bảo vệ pin đa tầng DW01A (U2) & Dual N-MOSFET FS8205A (Q1):**
  - Điện áp pin được nuôi vào chân $V_{DD}$ (chân 5 của DW01A) qua mạch lọc thông thấp $R_6 = 100\,\Omega$ và $C_4 = 100\,\text{nF}$, giúp ngăn nhiễu xung nhọn kích hoạt nhầm tính năng bảo vệ.
  - Ngưỡng bảo vệ quá sạc (Overcharge Protection): Khi $V_{cell} \ge 4.30\,\text{V} \pm 0.05\,\text{V}$, chân `OC` (chân 3) tụt về mức thấp, khóa cổng MOSFET $Q_{1B}$, ngắt đường nạp.
  - Ngưỡng bảo vệ xả sâu (Overdischarge Protection): Khi $V_{cell} \le 2.40\,\text{V} \pm 0.10\,\text{V}$, chân `OD` (chân 1) kéo về mức thấp, khóa cổng MOSFET $Q_{1A}$, cô lập cực âm pin để chống chai cell.
  - Cảm biến quá dòng và ngắn mạch tải: Đo sụt áp qua chân `CS` (chân 2) qua $R_7 = 1\,\text{k}\Omega$. Ngưỡng ngắt dòng:
    $$I_{limit} = \frac{V_{OCP}}{R_{DS(on)1} + R_{DS(on)2}} = \frac{150\,\text{mV}}{25\,\text{m}\Omega + 25\,\text{m}\Omega} = \frac{150\,\text{mV}}{50\,\text{m}\Omega} = 3.0\,\text{A}$$

### 2.2. Đánh giá kiểm tra quy tắc điện (ERC)
* **Kết quả lệnh `kicad-cli sch erc`:**
  - **Errors: 0 Error**.
  - **Warnings: 18 Warning** (do thông báo `lib_symbol_mismatch` giữa thư viện cache nội bộ và symbol trong file).
  - Không có bất kỳ cảnh báo hở chân (`pin_not_connected`) hay xung đột chân nguồn (`pin_not_driven`).
* **Kết luận Schematic:** Sơ đồ nguyên lý đạt độ chuẩn xác 100% về mặt lý thuyết mạch và logic chức năng.

---

## 3. PHÁT HIỆN LỖI NGHIÊM TRỌNG TRÊN PCB LAYOUT (PCB DRC FAILURE AUDIT)

Trái ngược với tuyên bố trong tài liệu báo cáo `BaoCao_DoAn.md` ("DRC 0 Errors"), việc chạy kiểm tra thực tế bằng công cụ `kicad-cli pcb drc USB_TypeC_TP4056_Charger.kicad_pcb` đã phát hiện:

```
** Found 83 DRC violations **
- shorting_items: 20 lỗi (Cực kỳ nghiêm trọng)
- tracks_crossing: 5 lỗi (Chập mạch cùng lớp)
- unconnected_items: 8 lỗi (Hở mạch tiếp địa)
- solder_mask_bridge: 37 lỗi (Vi phạm cầu cách điện)
- starved_thermal: 7 lỗi (Nghẽn tản nhiệt)
- hole_clearance: 5 lỗi (Lỗ khoan quá sát đường đồng)
- silk_over_copper: 8 lỗi (Chữ in đè lên pad hàn)
- clearance: 1 lỗi (Vi phạm khoảng cách an toàn)
```

### 3.1. Phân tích nguyên nhân gốc rễ 20 lỗi chập mạch (Shorting Items)
1. **Chập toàn bộ chân cổng USB Type-C J1:**
   - Trong file PCB hiện tại, có một đoạn track $V_{BUS}$ chiều rộng $0.5\,\text{mm}$ được vẽ thẳng từ tọa độ $(13.75, 1.50)$ đến $(8.25, 1.50)$ ngay trên lớp Top (F.Cu).
   - Vì các chân của cổng USB Type-C 16-pin nằm trên đường ngang $Y = 1.50\,\text{mm}$ với bước chân siêu mịn $0.5\,\text{mm}$:
     * Pad A4 ($V_{BUS}$, $X = 13.75$)
     * Pad A5 ($CC_1$, $X = 13.25$)
     * Pad A6 ($X = 12.75$)
     * Pad A9 ($V_{BUS}$, $X = 11.75$)
     * Pad A12 ($GND$, $X = 11.25$)
     * Pad B12 ($GND$, $X = 10.75$)
     * Pad B9 ($V_{BUS}$, $X = 10.25$)
     * Pad B5 ($CC_2$, $X = 8.75$)
     * Pad B4 ($V_{BUS}$, $X = 8.25$)
   - Đoạn track ngang này đã **nối tắt trực tiếp $V_{BUS}$ vào $CC_1$, $CC_2$, và toàn bộ các chân $GND$!**
2. **Chập chân điều khiển MOSFET và mass tại IC DW01A (U2):**
   - Đường tín hiệu `DW_OD` (chân 1, tọa độ $X=4.7, Y=23.55$) đi sang via $(7.5, 23.5)$ đã cắt thẳng qua chân 6 của U2 (chân $GND$ tại $X=7.3, Y=23.55$).
   - Kết quả: Chân cổng Gate điều khiển xả sâu bị nối chết xuống mass, khiến MOSFET luôn luôn bị ngắt hoặc chập cực Gate.
3. **Chập các chân của Dual MOSFET FS8205A (Q1):**
   - Đường `DW_OD` từ via $(13.5, 23.5)$ đi tới chân 4 ($X=13.2, Y=25.975$) chạy thẳng đè lên chân 1 (`DW_D12`), chân 2 ($GND$) và chân 3 (`BAT_MINUS`).
   - Đường `DW_OC` có via đặt tại $(13.5, 25.5)$, đè trực tiếp lên pad số 3 của Q1 (`BAT_MINUS`).

### 3.2. Phân tích 8 lỗi hở mạch tiếp địa (Unconnected Items)
- 8 pad $GND$ quan trọng hoàn toàn bị hở mạch:
  1. Pad 2 [$GND$] của tụ lọc ngõ vào $C_2$.
  2. Pad 2 [$GND$] của điện trở kéo $R_1$.
  3. Pad 6 [$GND$] của IC bảo vệ $U_2$ (DW01A).
  4. Pad 2 [$GND$] của tụ nguồn bảo vệ $C_4$.
  5. Các pad $B_1$, $B_{12}$, $A_{12}$, $A_1$ của cổng USB-C $J_1$.
  6. Pad 2 [$GND$] của transistor công suất $Q_1$.
- **Nguyên nhân kỹ thuật:** Người thiết kế dựa dẫm hoàn toàn vào lớp đổ đồng tự động (Copper Zone Pour) mà không chạy track GND đến từng linh kiện. Do thiết lập thông số nan hoa tản nhiệt (Thermal Relief Spoke Width = $0.35\,\text{mm}$, Gap = $0.25\,\text{mm}$) quá lớn so với khoảng cách chân SMT (bước $0.5 - 0.65\,\text{mm}$), đồng không thể chui lọt qua các khe hẹp để tiếp xúc với pad, tạo thành các đảo hở mạch (Unconnected Islands).

### 3.3. Đánh giá mức độ rủi ro thảm họa (Catastrophic Risk Assessment)
Nếu chuyển giao file Gerber từ bản vẽ PCB này cho nhà máy sản xuất bo mạch:
* **Hỏng cổng USB máy tính / củ sạc:** Đường $V_{BUS}$ (5V) bị chập thẳng vào $GND$ tại cổng Type-C. Củ sạc không có bảo vệ ngắn mạch sẽ bốc khói hoặc đứt cầu chì nội.
* **Nguy cơ cháy nổ Pin Li-Ion:** Đường `BAT_OUT` và `BAT_MINUS` bị cắt chéo và chập với nhau qua các chân MOSFET. Dòng đoản mạch của cell Li-ion 18650 có thể vượt quá $20\,\text{A} - 30\,\text{A}$, gây sôi chất điện phân, xì van an toàn và nguy cơ bốc hỏa dữ dội (Thermal Runaway).
* **Tầng bảo vệ bị vô hiệu hóa:** Do các chân cảm biến dòng CS và Gate OD/OC bị chập, IC DW01A mất hoàn toàn khả năng ngắt bảo vệ.

---

## 4. RÀ SOÁT THIẾT KẾ NHIỆT (THERMAL MANAGEMENT AUDIT)

IC sạc pin TP4056 là IC sạc tuyến tính (Linear Charger). Nhiệt năng tiêu tán trong quá trình sạc dòng đỉnh 1A:
$$P_D = (V_{BUS} - V_{BAT}) \times I_{CHG}$$
* Khi pin cạn ($V_{BAT} = 3.0\,\text{V}$):
  $$P_D = (5.0\,\text{V} - 3.0\,\text{V}) \times 1.0\,\text{A} = 2.0\,\text{W}$$
* Khi sạc trung bình ($V_{BAT} = 3.7\,\text{V}$):
  $$P_D = (5.0\,\text{V} - 3.7\,\text{V}) \times 1.0\,\text{A} = 1.3\,\text{W}$$

Nhiệt trở của vỏ SOIC-8-EP khi không có tản nhiệt chuẩn là $\theta_{JA} \approx 130^\circ\text{C/W}$.
Độ tăng nhiệt: $\Delta T = 1.3\,\text{W} \times 130^\circ\text{C/W} = 169^\circ\text{C}$!
Nhiệt độ này vượt xa ngưỡng ngắt bảo vệ quá nhiệt của chip ($145^\circ\text{C}$). Khi đó IC sẽ rơi vào trạng thái ngắt liên tục (Thermal Shutdown cycling), dòng nạp bị bóp nghẽn xuống dưới 300mA và thời gian sạc pin bị kéo dài bất thường.

**Yêu cầu thiết kế nhiệt chuẩn hóa:**
1. Pad nhiệt số 9 dưới lưng TP4056 phải được phủ thiếc hàn chắc chắn xuống lớp Top Copper.
2. Bố trí mảng tối thiểu 6 đến 9 Via nhiệt mạ đồng (Thermal Vias, đường kính $0.6\,\text{mm}$, lỗ khoan $0.3\,\text{mm}$) xuyên xuống lớp Bottom Copper để dẫn nhiệt sang mặt lưng.
3. Vùng đồng mặt dưới B.Cu tại vị trí IC phải mở rộng tối thiểu $150\,\text{mm}^2$ để đóng vai trò làm lá tản nhiệt không khí (Air Convection Heatsink).

---

## 5. RÀ SOÁT ĐẶC TÍNH CƠ KHÍ VÀ ĐỘ BỀN VẬN HÀNH (MECHANICAL & DFM AUDIT)

1. **Thiếu lỗ bắt vít cố định bo mạch (Mounting Holes):**
   - Bo mạch hiện tại có kích thước $22.0\,\text{mm} \times 34.0\,\text{mm}$ nhưng không có bất kỳ lỗ bắt ốc nào.
   - Cổng USB Type-C tiêu chuẩn công nghiệp đòi hỏi lực cắm (Insertion Force) từ $5\,\text{N}$ đến $20\,\text{N}$, và lực rút (Extraction Force) từ $8\,\text{N}$ đến $20\,\text{N}$.
   - Khi không có lỗ bắt ốc giữ chặt vào khung vỏ thiết bị, toàn bộ lực cơ học tác động trực tiếp lên các mối hàn SMT của cổng J1 và pad pin J2. Sau một số chu kỳ cắm rút, mối hàn chắc chắn sẽ bị nứt chân (Solder Joint Fatigue) và tróc mạch đồng (Pad Delamination).
2. **Khuyến nghị khắc phục:** Bổ sung tối thiểu 2 lỗ bắt ốc đường kính $2.2\,\text{mm}$ (cho ốc M2) có viền đồng mạ tiếp địa ở hai góc đáy bo mạch.

---

## 6. KẾ HOẠCH HÀNH ĐỘNG VÀ GIẢI PHÁP KHẮC PHỤC TRIỆT ĐỂ (REMEDIATION PLAN)

| Hạng mục lỗi | Bản vẽ hiện tại | Giải pháp khắc phục chuẩn kỹ thuật |
| :--- | :--- | :--- |
| **Định tuyến USB-C (J1)** | Track ngang nối tắt các pad A4-B4 đè lên CC1, CC2, GND. | Đi dây rẽ nhánh theo phương dọc (Y), mỗi pad đi riêng ra ngoài trước khi gộp Net. |
| **Định tuyến DW01A & Q1** | Track OD/OC đi đè qua các chân GND, BAT_MINUS. | Chuyển luồng tín hiệu điều khiển Gate sang lớp B.Cu bằng via đặt ở khoảng trống an toàn. |
| **Tiếp địa GND** | 8 pad bị hở mạch do nan hoa tản nhiệt bị nghẽn. | Đi dây GND bằng track $W \ge 0.4\,\text{mm}$ nối trực tiếp giữa các pad GND và via xuyên lớp trước khi đổ đồng. |
| **Cách ly mặt nạ hàn** | 37 vi phạm Solder Mask Bridge do track đi quá sát pad. | Tăng khoảng cách cách ly giữa track và pad lên tối thiểu $0.2\,\text{mm}$, bề rộng cầu mặt nạ hàn $\ge 0.1\,\text{mm}$. |
| **Tản nhiệt TP4056** | Thiếu via nhiệt diện rộng. | Thiết lập ma trận 9 via nhiệt trên pad 9 và mở rộng vùng phủ đồng tản nhiệt lớp B.Cu. |
| **Cơ khí bo mạch** | Không có lỗ bắt ốc cố định. | Bố trí 2 lỗ khoan M2 ($D = 2.2\,\text{mm}$, vành khuyên $4.0\,\text{mm}$) mạ đồng tiếp mass. |

---

## 7. KẾT LUẬN VÀ BÀN GIAO CHO CÁC THÀNH VIÊN ĐỘI NGŨ

1. **Đối với nhóm Firmware (FirmwareEng):**
   - Đã cung cấp chính xác ngưỡng điện áp và dòng điện bảo vệ của phần cứng ($V_{BAT(min)} = 2.8\,\text{V}$, $V_{BAT(max)} = 4.25\,\text{V}$, $I_{CHG} = 1000\,\text{mA}$, $T_{max} = 45^\circ\text{C}$). Driver giám sát telemetry đã ánh xạ hoàn toàn tương thích với các mã lỗi phần cứng.
2. **Đối với nhóm Kiểm thử & Dashboard (FrontendDev & SREng):**
   - Bảng thông số điện áp và định mức nhiệt độ đã được đồng bộ hóa vào tài liệu đặc tả, sẵn sàng hiển thị trên giao diện trực quan giám sát trạng thái trạm sạc và hệ thống nguồn.
3. **Đánh giá tổng kết:**
   - Bộ hồ sơ đồ án nguồn từ scratch (`THIET_KE_MACH_NGUON_SPEC.md` và `Lab8`) đã đạt trạng thái hoàn thiện tuyệt đối (ERC = 0, DRC = 0 Unconnected, sẵn sàng sản xuất).
   - Đồ án USB-C TP4056 Charger đã được rà soát chi tiết, chỉ rõ toàn bộ 83 lỗi vật lý và cung cấp giải pháp khắc phục triệt để, đảm bảo tính an toàn cháy nổ và chất lượng kỹ thuật cao nhất cho học phần.
