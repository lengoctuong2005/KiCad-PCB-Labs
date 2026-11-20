# Điểm vào dữ liệu chế tạo hiện hành

Chỉ dùng [print_preflight_20261114](print_preflight_20261114/README.md) để kiểm bản PCB nguồn hiện tại 92 × 70 mm.

- [ZIP Gerber/drill phẳng](print_preflight_20261114/GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip): đúng 11 file cấp gốc, không PDF/BOM/firmware.
- [BOM](print_preflight_20261114/BOM.csv) và [placement](print_preflight_20261114/placement_mm.csv): dữ liệu CAD, chưa BOM/CPL PCBA được duyệt.
- [Bản lắp 1:1](print_preflight_20261114/Assembly_1to1.pdf): in actual size 100% để đối chiếu mẫu thực.
- [DRC](print_preflight_20261114/drc.json), [ERC](print_preflight_20261114/erc.rpt), [manifest](print_preflight_20261114/manifest.json).

Các bộ cũ đã chuyển vào `../_archive/legacy_20261113/outputs/`. Tra `../_archive/legacy_20261113/INDEX.json` để phục hồi theo đường cũ và hash. Không dùng report/manifest lịch sử như bằng chứng cho revision mới. Các hình/phân tích DSP còn ở cấp này không phải dữ liệu chế tạo.

CAD đã kiểm không đồng nghĩa được duyệt CAM, lắp ráp, đáp ứng analog/timing hay an toàn tiếp xúc cơ thể. Không dùng trên người.
