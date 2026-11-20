# AFE ECG + PPG PAT: ghi chú thiết kế

## Cập nhật đồng bộ schematic, layout DFM, MPN/LCSC và bộ công cụ bench ngày 2026-11-18

Gói hiện hành vẫn xuất tại `outputs/print_preflight_20261114/` cùng `AFE_ECG_PPG_PTT-drc.rpt` và `AFE_ECG_PPG_PTT-erc.rpt` ở thư mục gốc repo. Giữ nguyên outline 92 x 70 mm, 46 footprint, 151 node netlist, 90 lỗ/slot khoan, keepout anten hai lớp tại x = 60 đến 92 mm và y = 0 đến 12 mm, bốn via return `GND` và nhãn cảnh báo an toàn trên `F.SilkS`.

- Schematic `AFE_ECG_PPG_PTT.kicad_sch`: sắp xếp lại toàn bộ sub-circuit trên lưới 1,27 mm, loại bỏ toàn bộ 6 vị trí chồng ký hiệu quanh U1, R6, C1, C2, R12, C5, C6 và tách nhãn `PWR_FLAG`, `TP1..TP7`, `H1..H4`, `R9..R12`, `R16..R17`, `R18`, `R19` giữ nguyên 49 UUID và giữ cố định `J2` cùng điểm `no_connect` tại `(233.67999999999998, 68.58)`. Cập nhật title block rev `v1.1` ngày `2026-11-18` mang tên sinh viên thực hiện.
- PCB layout và DFM trong `AFE_ECG_PPG_PTT.kicad_pcb` và `AFE_ECG_PPG_PTT.kicad_pro`: xử lý góc 90 độ và góc nhọn tự do bằng vát góc 45 độ, dọn đoạn thừa `RA_IN`/`SCL`/`OPAMP_P` còn 0 góc tự do vuông hoặc nhọn; tăng bề rộng 19 đoạn trunk `+3V3` và 19 đoạn trunk `+VS_A` lên 0,40 mm giữ nguyên đoạn neck-down 0,20 mm tại pad mịn U1/U2/U3 và nhánh 0,50 mm `J2.1-J3.1`; bổ sung netclasses `Default`, `Power`, `Analog_ECG`, `Digital_I2C` trong `.kicad_pro`.
- Vùng phủ đồng `GND` trên `B.Cu`: tăng `clearance` từ 0,20 mm lên 0,25 mm, `thermal_gap` 0,25 mm và `thermal_bridge_width` 0,40 mm rồi refill; đạt 0 lỗi `starved_thermal`.
- Silkscreen và mô hình 3D `J2`: đặt lại toàn bộ 46 reference trên `F.SilkS` đạt 0 vi phạm dưới kiểm tra tạm `min_silk_clearance` 0,15 mm; đưa nhãn Value `F.Fab` của `J2` vào bên trong thân `(12.7, 22.86, 90)` trong thư viện `afe:ESP32_DevKitC_V4_38P` và PCB; gắn hai mô hình 3D `PinSocket_1x19_P2.54mm_Vertical.step` tại `x = 0` và `x = 25,4 mm` và xuất mới `Schematic.png`, `PCB_3D_Top.png`, `PCB_3D_Iso.png`.
- Đồng bộ MPN/LCSC và gói đặt hàng Phase 2: điền đầy đủ thuộc tính ẩn `MPN` và `LCSC` cho toàn bộ 35 linh kiện mua được và gắn `PCB_INTEGRATED`/`DNP` cho `H1..H4`, `TP1..TP7` đồng nhất trên cả `.kicad_sch` và `.kicad_pcb` với 0 cảnh báo `footprint_symbol_field_mismatch`. Xuất `BOM.csv` và tạo `BOM_Orderable_LCSC.csv` gồm 20 mã đặt hàng trong đó `J2` lấy số lượng 2 thanh `C429947` cắt xuống 1x19P, `C10` dùng `C5360793` 1 uF 50 V X7R giữ ổn định LDO, và `J1` chọn `SJ1-3533N` `C4992360` cần đối chiếu cơ khí với `SJ1-3533NG`.
- Kiểm tra CAM từ ZIP và bản đồ hàn lắp: do không có `gerbv`, bộ render Gerber/Excellon viết bằng Pillow kiểm trực tiếp các tệp trong `GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip`, xuất `CAM_top.png`, `CAM_bottom.png`, `CAM_mask.png`, `CAM_paste.png` cùng `gerbv_logs.json`, xác nhận 3 slot `G85` tại `J1`, 38/38 via phủ mask kín hai mặt và 4 cửa sổ stencil `1,05 x 1,05 mm` bằng 65,2% diện tích EP của `U1`. Tạo bản đồ hàn lắp tương tác offline `Interactive_Soldering_Guide.html` và hướng dẫn khép kín `HUONG_DAN_IN_HAN_VA_NGHIEM_THU.md`.
- Công cụ firmware và nghiệm thu bench: giữ nguyên byte `firmware/esp32_ptt_streamer/main.c` và `main/main.c`, thêm `main/Kconfig.projbuild`, bọc macro `CONFIG_*` trong `esp32_ptt_streamer.h` kèm ngưỡng `LOD_ADC_HIGH_THRESHOLD_MV = 1400` cho `GPIO32`/`GPIO33`, tạo `tools/flash_esp32.sh`, sketch Arduino `tools/esp32_bench_diag/esp32_bench_diag.ino` và CLI `tools/bench_bringup_verify.py` đạt `10/10` cổng `--preflight` cùng 7/7 `tests/check_*.py` PASS. Đã chỉnh `software/README.md` khớp CLI thực tế của `ptt_live_analyzer.py`, định dạng 8 trường `E`/`P`, LPF `R11 = R12 = 1 MΩ, C5 = 1.5 nF, C6 = 10 nF, f0 ≈ 41.09 Hz` và khóa PAT live khi `TIMESTAMP_UNCERTAIN`. Các cổng thực tế về tồn kho checkout LCSC, module `MAX30102`, phê duyệt CAM xưởng, đo analog/timing bench và an toàn cách ly điện vẫn chưa đóng.

## Kiểm trước đặt PCB trần ngày 2026-11-14

Bộ hiện hành: `outputs/print_preflight_20261114/`. Giữ outline 92 × 70 mm, copper/pad/net/footprint placement và rules điện. Chỉ sửa legend: chữ visible 1,0 mm, nét 0,15 mm, graphic silk ≥0,15 mm; dời reference TP3/C11 và hai dòng cảnh báo. Kiểm profile tạm silk clearance 0,15 mm đạt 0 vi phạm; source rules giữ nguyên.

Fresh DRC mọi severity/all-track-errors/refill/parity 0/0/0, ignored DRC rỗng; ERC 0 với hai loại không áp dụng. Bảy test CAD/package PASS; 90 lỗ/slot khớp, ZIP 11 member phẳng/CRC/byte khớp. Profile xưởng tham chiếu và hướng dẫn đặt ở `FAB_PROFILE.md`, `DAT_PCB_TRAN.md` cùng bộ xuất. Đủ dữ liệu gửi CAM/báo giá PCB trần prototype có điều kiện, chưa phải order approval hoặc PCBA/hardware đã nghiệm thu.

J3 được đối chiếu actual CAD: pin 1 +3V3, 2 SCL, 3 SDA, 4 INT_MAX, 5 RD NC, 6 IRD NC, 7 GND. Không dùng mô tả ngoài đã đảo SCL/SDA. C10 MPN, logic LOD worst-case và module thực vẫn là cổng lắp/bench; fit/CAM cần xác nhận trước quyết định thanh toán. Firmware không đổi, không claim build mới hoặc PAT timing chính xác.

## Bản return GND cục bộ trước đó ngày 2026-11-13

Bộ hiện hành: `outputs/return_path_review_20261113/`. Giữ 92 × 70 mm, schematic, footprint, net/value và rules. Thêm bốn via GND tented 0,6/0,3 mm ngoài pad tại (39,6;34,32), (40,85;32), (44,6;32,175), (14,7;64). Nhánh U1.16 tới via dài 0,653 mm; C4.2 có stub 1,075 mm, via cách mép đồng pad khoảng 0,325 mm. C11/C10 nối via trên đường GND có sẵn. Nhánh J2.1→J3.1 dài 5 mm tăng từ 0,2 lên 0,5 mm. Không xóa track GND hoặc thay các đường analog khác.

Fresh DRC mọi severity/all-track-errors/refill đạt 0 violation, 0 unrouted, 0 parity, ignored_checks rỗng; review độc lập chạy lại xác nhận. ERC 0 với hai loại không áp dụng ghi rõ. Bảy kiểm CAD/package PASS; 90 lỗ/slot khớp drill, tăng từ 86 do bốn via mới. ZIP Gerber-only phẳng có đúng 11 member và byte khớp file đã kiểm. Chưa được xưởng phê duyệt CAM, chưa đo mức giảm nhiễu.

J3 dùng dây tới đầu PPG rời; phải chốt module, nguồn, pull-up và pinout. C10/logic LOD còn cổng chọn linh kiện và worst-case, không tự đổi rail 2,8 V. Firmware giữ nguyên, PAT live vẫn khóa. Xem `REVIEW_CLAIMS_20261113.md` để phân biệt lỗi, giả thuyết và giới hạn.

Dữ liệu các revision trước đã chuyển vào `_archive/legacy_20261113/outputs/`; mapping đường cũ→mới và hash tại `_archive/legacy_20261113/INDEX.json`. Các phần dưới là lịch sử, chữ “hiện hành” và đường outputs trong đó chỉ áp dụng tại revision đã ghi, không chỉ gói đang dùng.

## Bản thu chiều ngang trước đó ngày 2026-11-13

Bộ hiện hành: `outputs/narrow_verified_20261113/`. PCB 92 × 70 mm, diện tích 6.440 mm², giảm 8% so với 100 × 70 mm và 19,5% so với 100 × 80 mm ban đầu. J2 dịch trái 8 mm tới (63; 16), H2/H4 tới (54; 6)/(54; 65). J1 và J3 giữ nguyên; cấu hình vẫn một ECG ba điện cực và một PPG. Keepout anten giữ kích thước, dịch cùng J2 về x=60…92, y=0…12 trên cả hai lớp. C8 có via GND mới tại (59,275; 46,1), cần đo nhiễu/đáp ứng thực.

Native DRC mọi severity và all-track-errors sau refill: 0 violation, 0 unrouted, 0 parity, ignored_checks rỗng; review độc lập xác nhận lại. ERC và năm test CAD PASS, 86 lỗ/slot khớp drill. Schematic, BOM và project rules không đổi. Bản 100 × 70 mm lưu tại `outputs/narrow_20261113/baseline/`. Ứng viên lỗi trực tiếp trong `outputs/narrow_20261113/` không được dùng chế tạo; chỉ `gap_candidate/` đã qua kiểm.

Chưa xác minh cơ khí module/plug/vỏ, RF, analog hoặc an toàn tiếp xúc cơ thể. Không dùng gói 100 × 70 mm cho PCB nguồn mới.

## Bản thu gọn trước đó ngày 2026-11-13

Bộ hiện hành: `outputs/compact_20261113/`. PCB 100 × 70 mm, giảm 12,5% diện tích từ 100 × 80 mm. J1 tại (14; 5,55) mm, hướng cắm ra cạnh trên; miệng jack theo F.Fab cách mép 0,35 mm. H3 tại (5; 65), H4 tại (62; 65) mm. Cụm analog và J2 giữ nguyên; vùng cấm anten x=68…100, y=0…12 trên hai lớp không đổi. Chỉ sửa dây LA_IN, RA_IN, RL_E và GND tới lỗ bắt vít. Schematic và project rules giữ nguyên byte.

DRC 0, unrouted 0, parity 0, ignored_checks rỗng; kiểm compact geometry và netlist PASS. Có 86 lỗ/slot khớp drill mới. Snapshot nguồn 100 × 80 mm nằm trong `outputs/compact_20261113/baseline/`; các gói trước đó là lịch sử, không dùng cho layout mới. `tools/rebuild_from_netlist.py` là công cụ dựng nền 100 × 80 mm chưa route, không tái tạo PCB thu gọn hiện hành.

Chưa xác nhận jack/plug, vỏ, module thực, đáp ứng analog hoặc an toàn tiếp xúc cơ thể. Thu diện tích không chứng minh giảm giá gia công khi chưa có báo giá.

## Cổng kiểm trước thu gọn ngày 2026-11-13

Bộ hiện hành: `outputs/final_verification_20261113/`. DRC 0, unrouted 0, parity 0 với `ignored_checks` rỗng, clearance 0.2 mm, silk/mask web 0.1 mm. ERC 0, còn hai kiểm tra không áp dụng được ghi rõ trong report. Gerber đã mở bằng viewer độc lập, 86 lỗ/slot được so với PCB; firmware ESP-IDF v5.5 target ESP32 compile/link và build kiểm lại PASS. Chưa xác nhận module/cáp thực, MPN passive, CAM/lắp ráp, phép đo bench hoặc an toàn tiếp xúc cơ thể. Build không đồng nghĩa nạp lên bo và chạy đạt.

## Trạng thái sửa ngày 2026-11-12

Chưa phát hành chế tạo. PCB cũ không khớp schematic và không được dùng để đặt bo. Các mục từ ngày 2026-11-09 phía dưới là lịch sử, không phải cấu hình hiện hành.

Schematic hiện hành đã được kiểm bằng `tests/check_feedback_netlist.py`, `tests/check_analog_netlist.py` và KiCad 10.0.8 ERC với `--severity-all --exit-code-violations`: hai test PASS, ERC 0 tại lần kiểm này.

- Hồi tiếp âm: U1.9 = R13.2 = R14.1; R13 = 100 kΩ về REFOUT, R14 = 1 MΩ về OUT. Gain tầng op-amp danh định là 11.
- LPF: R11 = R12 = 1 MΩ; C5 = 1.5 nF nối SK_N1–AD_OUT; C6 = 10 nF nối OPAMP_P–REFOUT. Theo mô hình Sallen-Key lý tưởng: f0 ≈ 41.09 Hz, Q ≈ 0.775. Đây không phải đáp ứng đo của toàn hệ thống.
- HPF theo Figure 66: C1 = C2 = 0.33 µF; R6 = R8 = 10 MΩ; R18 = 1.4 MΩ; chân SW nối nút C2.1/R18.2. Chưa đo tần số cắt thực tế.
- R1/R2/R3 = 360 kΩ. Không dùng phép chia điện áp/điện trở để tuyên bố đạt IEC 60601-1.
- U3 = MCP1700-2802E, rail analog 2.8 V; FR và SDN nối rail này. GPIO25/J2.9 không nối. LDO không cách ly điện.
- ADS1115 đo AIN0−AIN1 = ECG_OUT−REFOUT; ALERT có R19 = 10 kΩ kéo lên 3V3.
- J2 dùng footprint project `afe:ESP32_DevKitC_V4_38P`, hai hàng cách 25.4 mm. H1–H4 dùng footprint M3 có pad GND. Chưa xác nhận bằng mẫu module thực và bản in 1:1.
- `tests/check_pcb_netlist.py` đối chiếu từng ref, value, footprint ID, symbol path và pad/net với XML mới xuất từ schematic. Test đã PASS trên PCB dựng lại: 46 footprint, 151 node, hai lớp.
- PCB nguồn đã thay bằng bản dựng lại. KiCad DRC sau refill, toàn bộ severity và schematic parity: DRC 0, unrouted 0, parity 0. Bằng chứng, hash, Gerber/drill mới và placement mm nằm ở `outputs/repair_20261112/`. Không đồng nghĩa đã duyệt DFM, module thực hoặc an toàn.
- C11 bypass analog gần U1; C8 bypass 3V3 gần U2; C9 1 µF tại đầu vào U3, C10 1 µF tại đầu ra U3. B.Cu có vùng GND đã refill và keepout anten cả hai lớp.

MAX30102 cần xác nhận đúng module, mức logic, pull-up và thứ tự chân trước lắp. PAT chứa PEP, không phải PTT thuần và chưa có độ chính xác đồng bộ đo thực nghiệm.

Không gắn điện cực lên người chỉ vì dùng pin hoặc CAD đã sạch. Cần đánh giá an toàn phù hợp; không nối USB, bộ sạc hay thiết bị đo có thể tạo đường dẫn tới điện lưới khi đang gắn điện cực.

## Lịch sử ngày 2026-11-09, đã bị thay thế
Ngày: 2026-11-09

## Xác minh kỹ thuật (đã tính/chốt trong thiết kế)
- AD8232 LFCSP-20 pinout chuẩn ADI: 1 HPDRIVE,2 +IN,3 -IN,4 RLDFB,5 RLD,6 SW,7 OPAMP+,8 REFOUT,9 OPAMP-,10 OUT,11 LOD-,12 LOD+,13 SDN,14 AC/DC,15 FR,16 GND,17 +VS,18 REFIN,19 IAOUT,20 HPSENSE, EP 21.
- ADS1115 VSSOP-10: 1 ADDR,2 ALERT/RDY,3 GND,4 AIN0,5 AIN1,6 AIN2,7 AIN3,8 VDD,9 SDA,10 SCL. ADDR->GND = 0x48.
- MAX30102 module 7-pin thường gặp: VIN,SCL,SDA,INT,RD,IRD,GND (addr 0x57). **Phải đo module thực mua**.
- ESP32 DevKit 38-pin: SDA=GPIO21, SCL=GPIO22, ALERT=27, INT=26, LOD+=32, LOD-=33, FR=25, ECG backup=GPIO34 (ADC1). Tránh GPIO 0,2,5,12,15 (strapping) và ADC2 khi Wi-Fi. **Phải đo footprint/pinout board clone thực mua**.

## Tính toán (VERIFY vs AD8232 datasheet Fig.66 trước khi in)
- HP 2 cực ~0.482 Hz: mạng tích hợp DC restore, C_HP=0.33uF, R_HP=10M => 10/(2*pi*R*C).
- LP 2 cực ~41.4 Hz, gain 11: R11=R12=82k, C7=100nF, C8=22nF, R13=1M, R14=100k.
- Bảo vệ vào: R1=R2=180k đối xứng (**đối chiếu giới hạn dòng điện cực >=Vs/10uA**).
- DC leads-off: R3=R4=10M lên AVDD (AC/DC=GND).
- RLD: R5=360k, C3=1nF.
- REFIN: R6=R7=10M chia AVDD + C4=0.1uF.
- Anti-alias ADS1115: R15=R16=1k, C14=C15=10nF.
- Nguồn: LDO 3.0V (MCP1700-3002E SOT-23/TO-92) cấp AVDD cho AD8232; +3V3 cho ADS1115/MAX30102/ESP32. C1=0.33uF,C2=0.33uF,C5=0.33uF,C6=0.33uF,C9=0.1uF,C10=1uF,C11=0.1uF,C12=1uF,C13=1uF.

## An toàn
Chỉ dùng pin/power bank khi gắn điện cực. Không cắm USB máy tính nối điện lưới khi đo trên người.

## Checklist bắt buộc trước đặt PCB
1. Mở KiCad, hoàn tất/kiểm tra wiring schematic theo nhãn mạng và bảng chân; chạy ERC sạch lỗi kết nối thực.
2. Kiểm footprint U1 (LFCSP-20 EP 2.6mm, paste, pin 1), J2 (ESP32 thật), J3 (MAX30102 thật).
3. Route thủ công đường ECG IN+/IN-/REFIN/nút MΩ: ngắn, đối xứng, không có I2C/số cắt qua vùng analog; GND plane liền.
4. DRC sạch; in 1:1 đặt thử module; xem Gerber.
5. Kiểm tra lại toàn bộ giá trị RC/LPF/HPF/RLD/REFIN với AD8232 datasheet Figure 66.

## Files
- `hardware/AFE_ECG_PPG_PTT.kicad_pro/sch/pcb`
- `output/gerber/*`, `output/AFE_ECG_PPG_PTT_pcb.pdf`, `output/BOM.csv`
- `docs/CALC.json`, `firmware/src/main.cpp`, `software/src/ptt_process.py`
