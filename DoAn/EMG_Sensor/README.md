# Đồ Án: Thiết Bị Đo Tín Hiệu Điện Cơ Bề Mặt (sEMG Analog Front-End)

## 1. Giới thiệu tổng quan
Dự án thiết kế hoàn chỉnh từ đầu (scratch) mạch thu nhận và xử lý tín hiệu điện cơ bề mặt (**Surface Electromyography - sEMG**) dùng trong các ứng dụng y sinh, điều khiển cánh tay robot sinh học (prosthetics), nhận diện cử chỉ cơ bắp và theo dõi vận động thể thao.

Thiết kế đạt **0 lỗi ERC** (Schematic Electrical Rules Check) và **0 lỗi DRC** (Design Rules Check) trên KiCad 8/10, sẵn sàng 100% cho gia công sản xuất công nghiệp (JLCPCB, PCBWay).

---

## 2. Thông số kỹ thuật chính (Specifications)

| Thông số | Giá trị | Ghi chú |
| :--- | :--- | :--- |
| **Điện áp nguồn ($V_{CC}$)** | 3.3V – 5.0V DC | Tương thích trực tiếp ESP32, STM32, Arduino |
| **Dòng tiêu thụ** | < 3.5 mA | Tiết kiệm năng lượng cho thiết bị đeo (wearable) |
| **Băng thông tần số EMG** | 20 Hz – 450 Hz | Chuẩn y tế loại bỏ nhiễu chuyển động và khử răng cưa |
| **Độ khuếch đại tổng (Total Gain)** | ~1010× (60.1 dB) | Tầng 1: $101\times$, Tầng 2: $10.1\times$ |
| **CMRR (Common Mode Rejection)** | > 100 dB @ 50/60 Hz | Nhờ khuếch đại vi sai AD623 & điện cực tham chiếu |
| **Tín hiệu đầu ra 1 (`RAW_EMG`)** | Centered @ $V_{\text{REF}}$ ($V_{CC}/2$) | Phân tích phổ tần số, mỏi cơ, FFT |
| **Tín hiệu đầu ra 2 (`ENV_EMG`)** | 0V – $V_{CC}$ DC Envelope | Đọc trực tiếp qua ADC vi điều khiển để trigger hành động |
| **Chỉ thị trực quan** | 2 LED SMD 0805 | LED xanh (Nguồn), LED đỏ (Cường độ co cơ) |
| **Kích thước bo mạch** | 50.0 mm × 30.0 mm | 2 lớp FR4 1.6mm, 4 lỗ bắt ốc M2 cách ly |

---

## 3. Kiến trúc mạch & Nguyên lý hoạt động

Mạch được thiết kế theo cấu trúc khối chuẩn công nghiệp:

```
[Điện cực IN+/IN-/REF]
         │
         ▼
[1. Khối lọc R-C EMI & Phân cực 10MΩ]
         │
         ▼
[2. Khuếch đại đo lường AD623ARZ (G1 = 101)]
         │
         ▼
[3. Mạch lọc thông cao chủ động HPF (fc ≈ 20 Hz)]
         │
         ▼
[4. Mạch lọc thông thấp Sallen-Key bậc 2 + Gain (fc ≈ 450 Hz, G2 = 10)]
         │
         ├─────────────────────────────────────────► [Đầu ra RAW_EMG (J3.3)]
         │
         ▼
[5. Mạch chỉnh lưu toàn sóng chính xác (Ideal Diode Detector)]
         │
         ▼
[6. Mạch lọc bao hình tích phân (Leaky Integrator, fc ≈ 5 Hz)]
         │
         ├─────────────────────────────────────────► [Đầu ra ENV_EMG (J3.4)]
         │
         ▼
[7. Đèn LED hiển thị lực co cơ (Red ACT LED)]
```

### Chi tiết các linh kiện cốt lõi:
1. **AD623ARZ (U1)**: IC khuếch đại đo lường vi sai chuyên dụng (Instrumentation Amplifier) đường nguồn đơn (Single-Supply Rail-to-Rail). Điện trở định độ lợi $R_8 = 1.0\text{ k}\Omega \Rightarrow G_1 = 1 + \frac{100\text{ k}\Omega}{1\text{ k}\Omega} = 101$.
2. **MCP6004-E/SL (U2)**: IC tích hợp 4 khuếch đại thuật toán Rail-to-Rail I/O độ ồn thấp:
   - **U2A**: Mạch đệm điện áp ảo ($V_{\text{REF}} = V_{CC}/2$) cung cấp đường mass ảo trở kháng cực thấp cho toàn hệ thống.
   - **U2B**: Mạch lọc thông thấp Sallen-Key bậc 2 tần số cắt 450 Hz kết hợp khuếch đại $10.1\times$ ($R_{12}=10\text{k}\Omega, R_{13}=91\text{k}\Omega$).
   - **U2C**: Mạch chỉnh lưu toàn sóng chính xác không suy hao diode kết hợp cặp diode xung $1N4148W$.
   - **U2D**: Mạch tích phân lọc bao hình cơ vân tần số cắt 4.8 Hz ($R_{18}=100\text{k}\Omega, C_{12}=330\text{nF}$).

---

## 4. Bố trí giắc cắm & Kết nối (Pinout)

### Giắc tín hiệu điện cực (J2 - 3 Pin 2.54mm):
- **Pin 1 (IN+)**: Điện cực đo dương (dán trên bắp cơ cần đo).
- **Pin 2 (IN-)**: Điện cực đo âm (dán dọc theo thớ cơ, cách điện cực dương 15-20mm).
- **Pin 3 (REF)**: Điện cực tham chiếu cơ thể (Body Reference / Ground, dán tại vùng xương trung tính như khuỷu tay hoặc cổ tay).

### Giắc cấp nguồn & đầu ra (J3 - 4 Pin 2.54mm):
- **Pin 1 (VCC)**: Điện áp nguồn 3.3V – 5.0V DC.
- **Pin 2 (GND)**: Mass nguồn hệ thống 0V.
- **Pin 3 (RAW)**: Tín hiệu thô đã lọc dải (20 Hz - 450 Hz), biên độ $\pm 1.5\text{V}$ quanh $V_{REF}$.
- **Pin 4 (ENV)**: Tín hiệu bao hình lực cơ bắp (0V - 3.3V/5V DC), tỷ lệ thuận với lực gồng cơ.

### Giắc nguồn phụ (J1 - 2 Pin 2.54mm):
- **Pin 1**: VCC | **Pin 2**: GND.

---

## 5. Kết quả kiểm tra thiết kế (Verification & Compliance)

| Công cụ kiểm tra | Lệnh thực thi | Kết quả | Đánh giá |
| :--- | :--- | :--- | :--- |
| **KiCad ERC** | `kicad-cli sch erc EMG_Sensor.kicad_sch` | **0 violations, 0 errors** | Đạt chuẩn điện Schematic |
| **KiCad DRC** | `kicad-cli pcb drc EMG_Sensor.kicad_pcb` | **0 violations, 0 unconnected** | Đạt chuẩn thiết kế PCB |
| **Netlist & Clearance** | Netclass default (0.20mm min) | **100% pass (≥ 0.25mm)** | Cách điện an toàn |
| **Mặt phẳng mass (GND)** | F.Cu & B.Cu thermal relief | **Đồng bộ hóa qua via stitching** | Giảm thiểu tối đa can nhiễu 50Hz |

---

## 6. Hồ sơ xuất xưởng (Outputs)

Tất cả các tệp phục vụ chế tạo bo mạch được xuất đầy đủ trong thư mục `outputs/`:
- **Gerber Files**: `EMG_Sensor-F_Cu.gbr`, `EMG_Sensor-B_Cu.gbr`, `EMG_Sensor-F_Mask.gbr`, `EMG_Sensor-B_Mask.gbr`, `EMG_Sensor-F_Silkscreen.gbr`, `EMG_Sensor-B_Silkscreen.gbr`, `EMG_Sensor-Edge_Cuts.gbr`.
- **Drill Files**: `EMG_Sensor.drl`, `EMG_Sensor-NPTH.drl`.
- **Danh mục linh kiện (BOM)**: `outputs/BOM_EMG_Sensor.csv` (41 linh kiện chi tiết).
- **Báo cáo kỹ thuật**: `outputs/drc_report.json`, `outputs/erc_report.rpt`.
- **Bản vẽ trực quan 2D**: `outputs/EMG_Sensor_Top.svg`, `outputs/EMG_Sensor_Bottom.svg`.
