# AFE ECG + PPG PAT, prototype bench

Nguồn KiCad hiện hành là `AFE_ECG_PPG_PTT.kicad_sch`, `AFE_ECG_PPG_PTT.kicad_pcb` và `AFE_ECG_PPG_PTT.kicad_pro` tại thư mục này. PCB 92 x 70 mm hai lớp FR-4, một kênh ECG ba điện cực qua J1 và một kênh PPG rời qua dây J3. Không dùng trên người; dùng pin không thay thế đánh giá an toàn điện IEC 60601-1.

- [Hướng dẫn đặt PCB, hàn lắp và nghiệm thu bench](HUONG_DAN_IN_HAN_VA_NGHIEM_THU.md)
- [Bộ xuất hiện hành ngày 18/11/2026](outputs/print_preflight_20261114/README.md)
- [ZIP Gerber/drill phẳng](outputs/print_preflight_20261114/GERBER_ONLY_92x70_NOT_CAM_APPROVED.zip)
- [BOM đặt hàng LCSC](outputs/print_preflight_20261114/BOM_Orderable_LCSC.csv)
- [Bản đồ hàn lắp tương tác offline](outputs/print_preflight_20261114/Interactive_Soldering_Guide.html)
- [Danh sách linh kiện và đối chiếu MPN/LCSC](DANH_SACH_LINH_KIEN.md)
- [Báo cáo đồ án HTML](BaoCao_DoAn.html) và [PDF](BaoCao_DoAn.pdf)
- [Ghi chú kỹ thuật](docs/DESIGN_NOTES.md)
- [Công cụ nạp ESP32](tools/flash_esp32.sh), [sketch chẩn đoán Serial](tools/esp32_bench_diag/esp32_bench_diag.ino) và [script kiểm tra bench](tools/bench_bringup_verify.py)

CAD, ERC, DRC và 10 cổng `--preflight` đã PASS không đồng nghĩa đã có phê duyệt CAM của xưởng, lắp ráp hoặc nghiệm thu phần cứng thực tế. Chưa kiểm nghiệm thực tế module MAX30102/ESP32 mua rời, chưa đo analog/timing bench và PAT live trong `software/ptt_live_analyzer.py` vẫn bị khóa do cờ `TIMESTAMP_UNCERTAIN`. Không nén thư mục `firmware/build`, `.history` hoặc `_archive` làm gói chế tạo.
