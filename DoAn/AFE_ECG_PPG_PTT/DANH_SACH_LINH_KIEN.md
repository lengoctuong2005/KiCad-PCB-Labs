# Danh sách linh kiện cho 1 bo AFE ECG + PPG PAT

Đối chiếu trực tiếp BOM schematic tại `outputs/print_preflight_20261114/BOM.csv` và tệp đặt hàng LCSC tại `outputs/print_preflight_20261114/BOM_Orderable_LCSC.csv`.

**Mua theo cột Cần dùng; cột Nên mua chỉ là gợi ý dự phòng khi hàn.** Toàn bộ MPN và mã LCSC dưới đây đã tra cứu từ `jlcsearch` ngày 18/11/2026 với tổng đơn giá linh kiện ước tính 11,81 USD cho một bo chưa tính phí vận chuyển, gia công PCB trần và hai module rời ESP32 / MAX30102. Các mã báo `Kiểm tra live` ở cột tồn kho cần xác nhận trực tiếp tại trang checkout LCSC trước khi đặt.

## 1. Điện trở

Toàn bộ là **điện trở dán SMD 0603 imperial, tương đương 1608 metric, kích thước 1,6 x 0,8 mm**, sai số 1%. Không mua điện trở chân cắm.

| Trị số | Vị trí | MPN | LCSC | Công suất | Stock | Đơn giá USD | Cần dùng | Nên mua |
|---|---|---|---|---|---:|---:|---:|---:|
| 360 kΩ | R1, R2, R3 | `RCT03360KFLF` | `C177519` | 100 mW | 20007 | 0.0014 | 3 | 5 |
| 10 MΩ | R4, R5, R6, R8, R9, R10 | `AC0603FR-0710ML` | `C227547` | 100 mW | 59286 | 0.0082 | 6 | 10 |
| 1 MΩ | R11, R12, R14 | `CRCW06031M00FKEA` | `C844922` | 100 mW | 119733 | 0.0044 | 3 | 5 |
| 100 kΩ | R13 | `CRCW0603100KFKTA` | `C844120` | 100 mW | 3773 | 0.0231 | 1 | 5 |
| 1 kΩ | R15 | `ERJPA3F1001V` | `C441922` | 333 mW | 13066 | 0.0269 | 1 | 5 |
| 4.7 kΩ | R16, R17 | `0603WAF4701T5E` | `C23162` | 100 mW | Kiểm tra live | 0.0028 | 2 | 5 |
| 1.4 MΩ | R18 | `0603WAF1404T5E` | `C38070` | 100 mW | Kiểm tra live | 0.0019 | 1 | 5 |
| 10 kΩ | R19 | `CRGCQ0603F10K` | `C4210728` | 100 mW | 19719 | 0.0094 | 1 | 5 |
| **Tổng** | **18 điện trở** | | | | | | **18** | **45** |

`R7` không có trong thiết kế hiện hành. Không thay 1,4 MΩ hoặc 10 MΩ bằng trị số gần đúng khi chưa tính lại mạch.

## 2. Tụ điện

Toàn bộ là **tụ ceramic dán SMD 0603 imperial / 1608 metric**, không phân cực.

| Điện dung | Vị trí | MPN | LCSC | Thông số | Stock | Đơn giá USD | Cần dùng | Nên mua |
|---|---|---|---|---|---:|---:|---:|---:|
| 0.33 uF | C1, C2 | `0603B334K250CT` | `C384782` | 25 V X7R ±10% | 6754 | 0.0266 | 2 | 5 |
| 1 nF | C3 | `GCM1885C2A102JA16D` | `C437457` | 100 V C0G ±5% | 23390 | 0.0338 | 1 | 5 |
| 0.1 uF | C4, C8, C11 | `MT18B104K500CT` | `C323570` | 50 V X7R ±10% | 2603 | 0.0095 | 3 | 5 |
| 1.5 nF | C5 | `GRM1885C1H152JA01D` | `C162204` | 50 V C0G ±5% | 15788 | 0.0194 | 1 | 5 |
| 10 nF | C6, C7 | `0603CG103J500NT` | `C82282` | 50 V C0G ±5% | Kiểm tra live | 0.0355 | 2 | 5 |
| 1 uF | C9, C10 | `TCC0603X7R105K500CT` | `C5360793` | 50 V X7R ±10% | 41343 | 0.0285 | 2 | 5 |
| **Tổng** | **11 tụ** | | | | | | **11** | **30** |

`C10` chọn mã `TCC0603X7R105K500CT` định mức 50 V X7R để giảm suy giảm điện dung hiệu dụng do DC bias tại 2,8 V và giữ ESR nằm trong dải ổn định 0 đến 2 Ω theo MCP1700.

## 3. IC rời hàn lên bo

| Vị trí | Linh kiện | MPN | LCSC | Package | Stock | Đơn giá USD | Cần dùng |
|---|---|---|---|---|---:|---:|---:|
| U1 | AD8232 | `AD8232ACPZ-R7` | `C43216` | LFCSP-20 4x4 mm, EP 2.6x2.6 mm | 1755 | 6.7141 | 1 |
| U2 | ADS1115 | `ADS1115IDGSR` | `C37593` | VSSOP-10 DGS 3x3 mm | Kiểm tra live | 1.4023 | 1 |
| U3 | MCP1700-2802E | `MCP1700T-2802E/TT` | `C625349` | SOT-23 | 202 | 0.4973 | 1 |

## 4. Đầu nối, module ngoài và phụ kiện

| Vị trí / Mục | MPN | LCSC | Package / Quy cách | Stock | Đơn giá USD | Cần dùng | Ghi chú mua và lắp |
|---|---|---|---|---:|---:|---:|---|
| J1 | `SJ1-3533N` | `C4992360` | 8x14 mm TRS 3-pin TH | 3 | 2.6004 | 1 | Đối chiếu khớp cơ khí với footprint `SJ1-3533NG` trước khi đặt. Tồn kho snapshot thấp. |
| J2 | `22850120ANG1SYA01` | `C429947` | 1x20P P2.54mm Female | 2328 | 0.1737 | 2 | Đặt 2 thanh cho 1 bo và cắt bớt 1 chân thành 1x19P cho hai hàng chân ESP32 cách tâm 25,4 mm. |
| J3 | `2541WV-07P` | `C25503132` | 1x7P P2.54mm Male | 4173 | 0.0246 | 1 | Đấu dây tới đầu PPG rời. Chân 1..7 là +3V3, SCL, SDA, INT_MAX, RD NC, IRD NC, GND. |
| ESP32-DevKitC V4 | Mua ngoài | Ngoài LCSC | 38 chân, hai hàng cách 25,4 mm | N/A | N/A | 1 | Kiểm tra thứ tự chân và chiều cổng USB/anten trên `Assembly_1to1.pdf` trước khi cắm vào J2. |
| Module MAX30102 | Mua ngoài | Ngoài LCSC | Bo rời 7 chân I2C 0x57 | N/A | N/A | 1 | Phân biệt bản xanh MH-ET LIVE với bản đen; xác nhận chân 1..7, mức 3,3 V và điện trở kéo lên I2C/INT. |
| Cáp TRS 3.5 mm 3 dây | Mua ngoài | Ngoài LCSC | Tip=RA, Ring=LA, Sleeve=RL | N/A | N/A | 1 | Đo thông mạch dây trước khi đấu vào máy phát tín hiệu giả lập. |
| Vít và trụ đỡ M3 | Mua ngoài | Ngoài LCSC | M3 lỗ 3,2 mm | N/A | N/A | 4 | Phù hợp lỗ `H1..H4` có pad nối GND. |

Không dùng module MAX30100 hoặc MAX30105 thay cho MAX30102 nếu chưa chỉnh phần cứng và firmware.

## 5. Các mục trong BOM không cần mua

Các mục sau được đánh dấu `MPN = PCB_INTEGRATED` và `LCSC = DNP` trong `BOM.csv`:

- `H1..H4`: 4 lỗ bắt vít M3 có pad GND gia công sẵn trên PCB.
- `TP1..TP7`: 7 pad đo đường kính 1,5 mm trên mặt bo cho `ECG_OUT`, `REFOUT`, `LOD_P`, `LOD_N`, `+VS_A`, `+3V3` và `GND`.

## 6. Dụng cụ chuẩn bị, không tính vào linh kiện bo

- Nhíp, kính phóng đại, dụng cụ ESD, kem hàn và máy khò có thermocouple cho `U1` LFCSP-20.
- Cồn IPA 99% và bàn chải ESD vệ sinh kỹ các nút 10 MΩ chống dòng rò flux.
- Đồng hồ vạn năng, nguồn bench hạn dòng, Patient Simulator và Optical Phantom. Không ngắt protective earth của thiết bị đo và tuyệt đối không thử trên người.

Nguồn datasheet: [AD8232](https://www.analog.com/media/en/technical-documentation/data-sheets/AD8232.pdf), [ADS1115](https://www.ti.com/lit/ds/symlink/ads1115.pdf), [MCP1700](https://ww1.microchip.com/downloads/en/DeviceDoc/MCP1700-Low-Quiescent-Current-LDO-20001826E.pdf), [ESP32-DevKitC V4](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html).
