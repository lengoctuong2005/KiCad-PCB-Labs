# Đối soát phần cứng t2: CHẶN CHẾ TẠO VÀ KẾT NỐI NGƯỜI

Ngày 2026-11-09. Trạng thái: **KHÔNG ĐẠT**. Các bảng sản xuất hiện có không phải gói phát hành; không đặt PCB, lắp ráp, cấp nguồn đo người hoặc sử dụng kết quả để khẳng định tuân thủ y tế.

## Phạm vi, sự cố và phục hồi

Bản [schematic hiện hành](../AFE_ECG_PPG_PTT.kicad_sch) và [PCB hiện hành](../AFE_ECG_PPG_PTT.kicad_pcb) là bản trước t2 sau sửa đổi của thành viên khác, không phải bằng chứng rằng thiết kế đúng. Tôi đã vô tình ghi đè schematic bằng generator thử nghiệm; sau đó đã bảo toàn bản lỗi và phục hồi chính xác snapshot mà captain xác nhận. Tôi cũng ghi đè PCB bằng các phương án route thử chưa đạt; tôi đã lưu bản thử cuối và khôi phục PCB từ cùng snapshot. Không có phương án thử nào được duyệt để chế tạo. Thư viện bị tôi thêm các symbol thử và đã phục hồi trùng byte với snapshot. Không hoàn tác các thay đổi có trước snapshot. Ba tệp PCB thử `test_clean`, `test_astar_board`, `test_astar_v2` ở thư mục dự án và các file dự án đi kèm là thí nghiệm chưa duyệt; giữ nguyên để truy vết, không dùng chế tạo. Khi chạy CLI tôi cũng đã ghi đè báo cáo ERC tên mặc định; báo cáo ERC lịch sử chạy riêng vẫn còn trong [erc_run.rpt](../erc_run.rpt).

| Dữ liệu | SHA-256 | Bản lưu |
|---|---|---|
| Schematic hiện hành | `edd23cfb42d701fc7c3a6ebeecefc38ae818f4879c78954d6cc2d66fe8608fc6` | [snapshot schematic](t2_evidence/pre_t2_schematic_20261109.kicad_sch) |
| PCB hiện hành | `b3a597be33eac75e4489f53e773f757bb06f57e85bef09bc47ff98174c6916e5` | [snapshot PCB](t2_evidence/pre_t2_PCB_20261109.kicad_pcb) |
| Thư viện symbol hiện hành | `18e73010d9470844275720d5428d208c8397bde4e22ed3a2fc29864b7f1963c4` | [thư viện hiện hành](../libs/afe.kicad_sym) |
| Schematic generator lỗi | `3bfd0073c13fb3e6a73d9d8ef09ed39e669a9b2cd5ee33f3ee947958f51c1ea5` | [bản lỗi, không sử dụng](t2_evidence/accidental_schematic_20261109.kicad_sch) |
| PCB route thử cuối | `da898124f0b1e1454f553027b191a12dc68e5a802966c898d9a103dac3280e2f` | [bản thử, không sử dụng](t2_evidence/INVALID_last_experimental_PCB_20261109.kicad_pcb) |

## Kết quả kiểm tra bằng KiCad CLI 10.0.8

- `kicad-cli pcb drc --severity-all --schematic-parity --exit-code-violations`: **301 vi phạm DRC**, **170 lỗi/cảnh báo parity**, thoát mã 5. Trong DRC có **71 `shorting_items` và 39 `tracks_crossing`**. Còn báo 0 unconnected pads nhưng điều đó không phủ nhận các chập mạch hay parity sai. [Báo cáo DRC đầy đủ](t2_evidence/restored_2301_drc_parity.rpt).
- `kicad-cli sch erc --severity-all --exit-code-violations`: 0 thông báo ở lần chạy này, nhưng báo cáo có **4 loại kiểm tra bị bỏ qua**, gồm global label chỉ xuất hiện một lần. ERC không xác nhận đúng topology hoặc tương ứng PCB. [Báo cáo ERC](t2_evidence/restored_2301_erc.rpt).
- [Kiểm tra lại bản route thử cuối theo đúng SHA-256 trên](t2_evidence/last_candidate_verified_drc_parity.rpt): **79 vi phạm, 33 pad chưa kết nối và 170 vấn đề parity**, mã thoát 5. Báo cáo chỉ cho thấy phương án thử không đạt, không dùng làm phương án chế tạo.
- Không sửa DRC/ERC rule hoặc dùng exclusion để che lỗi. Ground-plane liền mạch, phân vùng, cân bằng đường tín hiệu và keepout chưa được chứng minh trên thiết kế đạt parity.

## Netlist trước và sau sửa bên ngoài

[Netlist trước sửa lưu lúc 20:53](t2_evidence/prior_2053_netlist_unvalidated.net) là dữ liệu lịch sử chưa được xác nhận là thiết kế chuẩn. [Netlist XML schematic đã phục hồi](t2_evidence/restored_2301_netlist.xml) được xuất mới lúc 23:01. So sánh ref.pin, không giả định hai thiết kế có cùng chức năng theo tên linh kiện:

| Mạng | Trước sửa bên ngoài | Schematic phục hồi |
|---|---|---|
| `OPAMP_N` | U1.8, U1.9, U2.5, C6.2, R13.1, R13.2, R14.1, TP2.1 cùng mạng | U1.9, R13.1 |
| `REFOUT` | Không có mạng tách biệt tên này trong netlist | U1.8, U2.5, C6.2, R13.2, R14.1, TP2.1 |
| `AD_OUT` | U1.10, C5.2, R14.2, R15.1 | Không đổi |
| `HP_NODE` | C1.1, R6.2 | C1.1, R6.2, U1.6 |
| `HP_NODE2` | U1.6 | Không còn tên này |
| `HPSENSE` | U1.20, C1.2, C2.1 | Không đổi |
| `IAOUT` | U1.19, C2.2, R11.1 | Không đổi |
| `RLDFB` | U1.4, C3.1, R8.2 | Không đổi |
| `RLD_E` | U1.5, C3.2, R3.2, R8.1 | Không đổi |

Ở schematic phục hồi, U1.9 nối một đầu R13, đầu kia R13 nối `REFOUT`; R14 nối từ `REFOUT` sang `AD_OUT`. Vì vậy điểm `OPAMP_N` không nằm ở nút giữa R13/R14 như mạch phản hồi khuếch đại không đảo trong AD8232 Rev. D Figure 60. Kết luận **gain 11 của schematic hiện hành không được chứng minh**; không khôi phục nhãn cũ đơn thuần vì netlist trước đó chập U1.8 và U1.9. Cần thiết kế lại và review topology, sau đó đo hoặc mô phỏng.

Tương tự, U1.6 hiện tại gắn `HP_NODE` cùng C1.1/R6.2, còn U1.20 gắn C1.2/C2.1. AD8232 Rev. D Figure 55 mô tả SW nối đầu ra của mạng AC-coupling thứ hai. Sơ đồ này cần được đối chiếu lại theo topology chủ định trước khi xác nhận 0,5 Hz. Không suy ra giá trị fc từ một công thức áp cho mạch khác. Datasheet nhấn mạnh điều chỉnh thực tế và ảnh hưởng tải giữa các tầng.

## Các điểm cần giải quyết trước khi layout lại

1. **Parity:** schematic có 44 component, PCB có 56 footprint; J2 trong schematic là một symbol/footprint 2x19, còn PCB là J2A/J2B 1x19. Giá trị, chức năng và net của nhiều ref trùng tên khác nhau. Ví dụ C3 trong schematic là tụ 1 nF của RLD; C3 trên PCB/BOM là 22 nF trong LPF. Đồng bộ không thể làm an toàn bằng đổi tên đơn thuần. [Chi tiết parity](t2_evidence/restored_2301_drc_parity.rpt).
2. **Nguồn:** U3 schematic ghi `MCP1700-2802E`, PCB/BOM ghi `MCP1700-3002E`; cùng SOT-23 theo footprint hiện có. Netlist schematic hiện tại gán U3.1 GND, U3.2 +VS_A, U3.3 +3V3. Đối chiếu chân với datasheet của đúng mã/hãng và footprint thực tế, không chỉ dựa tên symbol. Phân tích sai số, tải, nhiệt, nguồn đầu vào min và dropout worst-case trước khi chấp thuận 3,3→3,0 V; tôi không có đầy đủ dữ liệu để kết luận. MCP1700 là LDO, **không phải cách ly điện**.
3. **Mức số:** schematic nối J2.9 `FR_PIN` trực tiếp U1.15; nếu GPIO 3,3 V điều khiển AD8232 nguồn 3,0 V thì 3,3 V chỉ bằng giới hạn tuyệt đối danh nghĩa `+VS + 0,3 V`, chưa tính sai số hay sequencing. AD8232 datasheet Rev. D Table 2 yêu cầu xét ngưỡng thấp hơn giữa `+VS+0,3 V` và giới hạn nguồn tuyệt đối; trường hợp mất nguồn analog cần xét riêng. Cần kiểm tra mọi giao diện, mức logic, trạng thái power-off và giải pháp tương thích; không coi giới hạn tuyệt đối là điều kiện vận hành.
4. **Điện cực và RLD:** trên schematic phục hồi RA và LA qua R1, R2 mỗi điện trở 180 kΩ tới chân U1.2/U1.3; RL qua R3 360 kΩ. Số R1+R3 và R2+R4 trong báo cáo cũ đã nhầm giữa hai thiết kế. Đánh giá an toàn hệ thống phải bao gồm mọi đường dòng, tình huống lỗi đơn, ESD, cách ly nguồn/giao tiếp, điện áp thực, sai số linh kiện và phép thử phù hợp; điện trở đơn lẻ không chứng nhận tuân thủ IEC.
5. **ADC:** ADS1115 PGA FSR không cho phép từng chân analog vượt nguồn: Recommended Operating Conditions yêu cầu mỗi AIN nằm giữa GND và VDD. Tính FSR và độ phân giải chỉ có ý nghĩa sau khi bias, biên độ và giới hạn analog đã được chứng minh. Lọc RC 7,95 kHz không phải bằng chứng anti-alias đủ ở tốc độ lấy mẫu 475/860 SPS.
6. **Module:** chưa có đúng model DevKit 38 chân và module MAX30102 đã chọn để chứng minh chiều, bước, pinout, RD/IRD, nguồn module, mức I/O hay vùng anten. Chưa được tùy ý kết luận chân RD/IRD là NC. GPIO ngắt không tự bảo đảm thời gian ≤2 ms; cần phép đo đồng bộ end-to-end.
7. **BOM/placement:** [BOM hiện có](../outputs/BOM_AFE_ECG_PPG_PTT.csv) gán C25804 cho cả 100 kΩ và 10 kΩ; [dữ liệu LCSC C25804](https://www.lcsc.com/product-detail/C25804.html) mô tả 10 kΩ, còn [C25803](https://www.lcsc.com/product-detail/C25803.html) mô tả 100 kΩ. Chỉ cập nhật BOM sau khi chốt lại sơ đồ và giá trị. [CPL hiện có](../outputs/AFE_ECG_PPG_PTT-pos.csv) không ghi đơn vị và C1 ghi 0,944882 khi PCB đặt 24 mm: số này tương ứng inch. Chưa xuất CPL mới vì PCB chưa duyệt.

## Nguồn đối chiếu

- [AD8232 Data Sheet Rev. D](https://www.analog.com/media/en/technical-documentation/data-sheets/AD8232.pdf), Figure 55, 56, 60, 66; Table 2 và cảnh báo tr. 28: mạch ví dụ không phải thiết kế hoàn chỉnh, cần công tác bổ sung về an toàn y tế.
- [TI ADS1115 Data Sheet](https://www.ti.com/lit/ds/symlink/ads1115.pdf), §§5.1, 5.3 và lưu ý về FSR/input voltage.
- Datasheet MCP1700: yêu cầu đối chiếu nguồn chính thức; lượt tải Microchip trong môi trường này trả 403, chưa xác thực giới hạn worst-case.
