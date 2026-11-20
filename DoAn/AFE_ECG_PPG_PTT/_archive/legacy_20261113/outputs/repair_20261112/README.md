# CAD prototype đã kiểm, chưa phát hành chế tạo

KiCad 10.0.8, ngày 12/11/2026. Nguồn chính là `../../AFE_ECG_PPG_PTT.kicad_sch` và `../../AFE_ECG_PPG_PTT.kicad_pcb`.

## Bằng chứng

- `erc.rpt`: 0 lỗi, 0 cảnh báo trong các kiểm tra được bật; bốn loại bị bỏ qua được ghi trong report.
- `drc.json`: DRC 0, unrouted 0, schematic parity 0 sau refill. Giữ nguyên danh sách ignored_checks và không có exclusion để che lỗi.
- `analog.log`, `feedback.log`: kiểm topology và trị số từ XML xuất mới.
- `manifest.json`: SHA-256 đầu vào/đầu ra, phiên bản công cụ và giới hạn nghiệm thu.
- `routing_input.dsn`, `routing_result.ses`, `routing.log`: đầu vào/đầu ra thực của FreeRouting 2.4.1, một luồng. Bản native 2.5.0 bị lỗi serialization và không dùng làm kết quả. Sau import SES, track hẹp được sửa về ≥0.2 mm rồi chạy DRC lại; SES không thay thế PCB cuối đã kiểm.
- `layout_metrics.json`: RA_P 3.445 mm, LA_P 4.646 mm, REFIN 8.583 mm, OPAMP_N 5.547 mm; các net này không có via. HP_MID và IAOUT vẫn có đoạn chuyển lớp, chưa có phép đo nhiễu/đáp ứng thực.
- `pre_rebuild_REJECTED.kicad_pcb`: bản PCB cũ bảo toàn để đối chiếu, không chế tạo.

## Bộ xuất mới

- `gerbers/`: hai lớp đồng, mask, silk, paste, Edge.Cuts; Excellon mm tách PTH/NPTH.
- `BOM.csv`: 46 reference từ schematic, chưa có MPN nhà cung cấp hoặc giá được xác nhận.
- `placement_mm.csv`: 35 reference lắp ráp, đơn vị mm, tọa độ tuyệt đối, KiCad đảo dấu PosY. H1–H4 và TP1–TP7 không có trong placement do thuộc tính không đặt bằng máy. Không tự đổi dấu hoặc rotation trước khi chốt quy ước với nhà lắp.
- `CAD_PROTOTYPE_NOT_RELEASED.zip`: bộ Gerber/drill, BOM, placement và bằng chứng CAD, không phải phê duyệt đặt hàng.
- `Schematic.pdf`, `PCB_Layout.pdf`, `PCB_Top.png`: hình xuất từ CAD mới.
- `BaoCao_DoAn.pdf`: báo cáo đã đính chính; nội dung trạng thái phần mềm phải đọc cùng kết quả build/test hiện hành.
- `firmware_host_checks.json`: ngày 13/11/2026, test C build mới, regression enqueue thực với queue đầy, protocol tám/bảy trường và DSP cũ đều PASS. Mô phỏng sau tích hợp nhận 13 nhịp trong `synthetic_after_protocol.json`. Đây không phải build ESP-IDF hoặc kết quả đo bo thật.
- Firmware mới phát từng mẫu IR riêng bằng packet `P`; ECG dùng packet `E`. Timestamp PPG chưa hiệu chuẩn và bit7 được bật, host vẫn khóa PAT cho dữ liệu firmware. Mọi xác nhận timing cần thử bằng tín hiệu giả lập và thiết bị phù hợp.

## Chưa xác nhận

Chưa kiểm toàn gói trong Gerber viewer, mẫu MAX30102 và mức logic/pull-up, fit socket ESP32/module bằng bản in 1:1, cực tính cáp ECG, quy ước rotation máy lắp, stencil/MPN và báo giá xưởng. Firmware chưa có build ESP-IDF; chưa đo đáp ứng analog hoặc sai số timing trên bo thật.

Chỉ thử bằng nguồn tín hiệu giả lập phù hợp. CAD sạch không chứng minh an toàn điện. Không gắn điện cực lên người khi chưa được đánh giá an toàn phù hợp; không nối USB, bộ sạc hoặc thiết bị đo có thể tạo đường dẫn tới điện lưới trong lúc gắn điện cực.
