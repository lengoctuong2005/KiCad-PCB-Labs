# Gói kiểm trước đặt PCB trần và bộ tài liệu bench, cập nhật 18/11/2026

## Phạm vi bàn giao

PCB prototype 92 x 70 mm, hai lớp, dùng cho thử nghiệm bench với tín hiệu giả lập. Bản cập nhật ngày 18/11/2026 bổ sung đầy đủ thuộc tính `MPN` và `LCSC` đồng nhất trên toàn bộ 46 ký hiệu schematic và 46 footprint PCB, tạo `BOM_Orderable_LCSC.csv` đặt hàng LCSC, dựng bộ ảnh kiểm tra CAM từ dữ liệu Gerber và Excellon thực tế trong ZIP, và tạo bản đồ hàn lắp tương tác `Interactive_Soldering_Guide.html`. Không thay đổi `firmware/esp32_ptt_streamer/main.c` và `main/main.c`. Không chứng minh mạch hoạt động hoặc an toàn dùng trên người.

**File gửi CAM:** `GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip`. Có đúng 11 file cấp gốc: 9 Gerber và 2 Excellon, không PDF/README/BOM/build. `.gbrjob` nằm ngoài ZIP.

## Kiểm đã làm ngày 18/11/2026

- KiCad 10.0.8 DRC với `--refill-zones --all-track-errors --schematic-parity --severity-all --exit-code-violations`: 0 violation, 0 unconnected, 0 schematic parity kể cả `footprint_symbol_field_mismatch`, `ignored_checks` rỗng.
- ERC đạt 0 Errors và 0 Warnings; giữ hai kiểm không áp dụng `global label only appears once` và `SPICE model issue` trong `erc.rpt`.
- Kiểm profile tạm `min_silk_clearance` 0,15 mm, `silk_over_copper` = error, `silk_overlap` = error, `silk_edge_clearance` = error đạt 0 lỗi trong `drc_fab_silk15.json`.
- Bảy kiểm regression `tests/check_*.py` đều PASS và 10/10 cổng `tools/bench_bringup_verify.py --preflight` đều PASS.
- 90 lỗ/slot khớp PCB trong 0,0011 mm: 38 via drill 0,3 mm; 48 lỗ/slot tool 1 mm gồm 3 slot `G85` tại `J1`; 4 lỗ M3 3,2 mm có mạ. NPTH file rỗng là chủ ý.
- Dựng kiểm tra CAM trực tiếp từ các tệp giải nén trong ZIP bằng Pillow/Excellon parser tại `CAM_top.png`, `CAM_bottom.png`, `CAM_mask.png`, `CAM_paste.png` và lưu thông số vào `gerbv_logs.json`: xác nhận 3 slot `G85` ở `J1`, 38/38 via phủ mask kín trên cả `F.Mask` và `B.Mask`, và 4 cửa sổ stencil phân đoạn `1,05 x 1,05 mm` đạt 65,2% diện tích trên EP của `U1`. Môi trường chạy không cài `gerbv`, nên cần đối chiếu thêm bằng preview CAM của xưởng trước khi thanh toán.
- `BOM.csv` xuất đủ 6 cột `Reference,Value,Footprint,MPN,LCSC,Quantity` cho 46 hàng; `BOM_Orderable_LCSC.csv` gồm 20 dòng linh kiện đặt hàng với `J2` số lượng 2 thanh.
- `Interactive_Soldering_Guide.html` tạo từ tọa độ thực trong `.kicad_pcb` cùng bảng MPN/LCSC và điểm kiểm tra `TP1..TP7`.
- `manifest.json` lưu mã băm SHA-256 của toàn bộ tệp nguồn, test và gói xuất hiện hành.

## Cách đặt và hàn lắp

Đọc `../HUONG_DAN_IN_HAN_VA_NGHIEM_THU.md`, `DAT_PCB_TRAN.md` và `FAB_PROFILE.md`. In `Assembly_1to1.pdf` tỷ lệ 100% đối chiếu module thực và mở `Interactive_Soldering_Guide.html` khi hàn lắp.

## Các cổng chưa đóng

1. Trước thanh toán: xác nhận preview CAM của xưởng nhận đúng 92 x 70 mm, 2 lớp, 3 slot `G85` của `J1`, 38 via tented và 4 lỗ M3 mạ; kiểm tồn kho thực tế của `U2` `C37593`, `C6/C7` `C82282`, `R16/R17` `C23162`, `R18` `C38070` và khớp cơ khí `J1` `SJ1-3533N`.
2. Trước lắp và cấp nguồn: kiểm tra pinout 7 chân và pull-up của module `MAX30102` thực mua ngoài, kiểm tra khớp chân ESP32 DevKitC V4 38 chân với `J2`.
3. Sau lắp: chạy `tools/esp32_bench_diag/esp32_bench_diag.ino` kiểm tra I2C và ngưỡng LOD `1400 mV` trên `GPIO32`/`GPIO33`, thực hiện đo 7 bước bench với máy giả lập và giữ nguyên khóa PAT live do `TIMESTAMP_UNCERTAIN`.
