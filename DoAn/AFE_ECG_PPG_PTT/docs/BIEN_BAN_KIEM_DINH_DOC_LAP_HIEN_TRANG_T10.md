# BIÊN BẢN KIỂM ĐỊNH ĐỘC LẬP TOÀN DIỆN HIỆN TRẠNG DỰ ÁN (TASK T10)
**Dự án:** Hệ thống Thu thập Đồng thời ECG và PPG Ước lượng PTT/PAT Dùng ESP32  
**Kiểm định viên độc lập:** embedded-qa-engineer  
**Thời điểm kiểm định:** 2026-11-09T23:25:00+07:00  
**Trạng thái phê duyệt chế tạo:** **REJECT (ĐÓNG BĂNG TOÀN BỘ GÓI XUẤT XƯỞNG CŨ, CHẶN CHẾ TẠO)**

---

## 1. MỤC TIÊU VÀ PHẠM VI KIỂM ĐỊNH (AUDIT SCOPE)

Thực hiện kiểm định độc lập lần cuối đối với hiện trạng toàn bộ dự án theo phân công Task t10:
1. Xác thực tính pháp lý và kỹ thuật của các hồ sơ chặn chế tạo tại `outputs/KHONG_SU_DUNG_DE_CHE_TAO.md` và `docs/DOI_SOAT_T2_VA_NGAN_CHAN_CHE_TAO.md`.
2. Kiểm tra và xác nhận trạng thái đóng băng của gói Gerber cũ (tạo lúc 19:49) cùng các rủi ro an toàn điện / y tế sinh học.
3. Đối soát độc lập kết quả kỹ thuật đã đạt được của Firmware FreeRTOS (Task t9) và Pipeline DSP PAT (Task t7).
4. Phân định rạch ròi ba cấp độ dữ liệu: **Đo đạc vật lý thực tế**, **Mô phỏng/Host test**, và **Khẳng định lý thuyết chưa kiểm chứng**.
5. Cập nhật báo cáo nghiệm thu kỹ thuật `BaoCao_DoAn.html` bảo đảm tính trung thực, khách quan và minh bạch tuyệt đối.

*Tuân thủ nghiêm ngặt chỉ thị của Captain:* Không chỉnh sửa hoặc can thiệp vào schematic, PCB layout, thư viện linh kiện, BOM hay thư mục `outputs/`.

---

## 2. XÁC THỰC CÁC HỒ SƠ CHẶN CHẾ TẠO VÀ ĐÓNG BĂNG GERBER CŨ

### 2.1 Kiểm tra hồ sơ cảnh báo chế tạo
- **Tệp `outputs/KHONG_SU_DUNG_DE_CHE_TAO.md`:** Đã kiểm tra trực tiếp. Tệp được ban hành lúc 23:08 ngày 2026-11-09, quy định rõ: *Các Gerber, drill, BOM, CPL và hình ảnh trong thư mục outputs/ là xuất phẩm cũ, không phải gói sản xuất đã duyệt; PCB có lỗi DRC và không khớp schematic; Nghiêm cấm đặt sản xuất, lắp ráp, cấp điện đo trên người*.
- **Tệp `docs/DOI_SOAT_T2_VA_NGAN_CHAN_CHE_TAO.md`:** Đã kiểm tra trực tiếp. Tệp dài 9.858 bytes phân tích chi tiết:
  1. Bản vẽ PCB hiện tại vi phạm 301 lỗi DRC (71 lỗi ngắn mạch short-circuit, 39 lỗi đè đường mạch tracks crossing, 87 lỗi cầu mặt nạ hàn).
  2. Sơ đồ nguyên lý Schematic có lỗi đứt hồi tiếp âm: Chân 1 của điện trở R14 (1M) đấu vào `REFOUT` thay vì `OPAMP_N` (pin 9 U1), biến tầng khuếch đại Sallen-Key thành bộ so sánh bão hòa nguồn (Open-loop Comparator).
  3. Tệp tọa độ dán linh kiện `AFE_ECG_PPG_PTT-pos.csv` xuất theo hệ Inch ($X=0.944882\text{ in}$) thay vì Milimet.
  4. Bảng linh kiện BOM trùng mã LCSC C25804 giữa trở 100k (R10-R12) và trở 10k (R20).
- **Trạng thái gói Gerber cũ (`outputs/Gerber_AFE_ECG_PPG_PTT_Production.zip`):** Tệp nén có kích thước 102.511 bytes tạo lúc 19:49 ngày 2026-11-09 mang mã băm SHA256: `18f837943ce14eb13fe9bcab6016186b72a4e213b1f5c6b65313a17e082cb75e`. Toàn bộ gói này được xác nhận **ĐÓNG BĂNG VÀ KHÔNG ĐƯỢC PHÉP SỬ DỤNG**.

### 2.2 Cảnh báo rủi ro an toàn điện và an toàn sinh học y tế
- **Thiếu cách ly điện (Galvanic Isolation):** Mạch nguồn AFE sử dụng IC ổn áp tuyến tính MCP1700-3002E chia sẻ chung đường đất GND với khối số và cổng USB ESP32. Thiết kế hoàn toàn **KHÔNG CÓ BIẾN ÁP CÁCH LY HAY BỘ GHÉP QUANG CHUẨN Y TẾ IEC 60601-1**.
- **Nguy cơ điện giật nguy hiểm:** Nếu cắm cáp USB nối vào máy tính sử dụng nguồn điện lưới AC 220V bị rò, dòng điện rò có thể chạy thẳng qua điện cực dán trên ngực người sử dụng.
- **QUY ĐỊNH BẮT BUỘC:** 
  - Tuyệt đối **NGHIÊM CẤM** gắn điện cực lên người khi bo mạch đang nối cáp cắm nguồn điện lưới 220V.
  - Khi thử nghiệm đo đạc thực tế (sau khi có bản mạch hoàn chỉnh), bắt buộc phải cấp nguồn độc lập bằng **PIN HOẶC POWER BANK BIỆT LẬP** và truyền dữ liệu qua giao thức Wi-Fi / UDP.

---

## 3. ĐỐI SOÁT ĐỘC LẬP FIRMWARE FREERTOS (TASK T9)

Đã đối soát trực tiếp mã nguồn tại `DoAn/AFE_ECG_PPG_PTT/firmware/esp32_ptt_streamer/` và kết quả thực thi kiểm thử:

1. **Khắc phục cấu hình MAX30102:** Firmware đã bổ sung việc xóa sạch con trỏ FIFO (ghi $0\text{x}00$ vào thanh ghi $0\text{x}04, 0\text{x}05, 0\text{x}06$) trước khi kích hoạt lấy mẫu, loại bỏ nguy cơ đọc dữ liệu cũ/lệch pha.
2. **Cấu trúc gói tin Telemetry UDP chuẩn hóa:** Đã bổ sung 6 cờ chẩn đoán chất lượng (`quality_flags` bitmask gồm: `sync_ok`, `lod_pos`, `lod_neg`, `saturated`, `fifo_burst`, `queue_drop`) và trường độ lệch thời gian có dấu `sync_skew_us` (int32).
3. **Kết quả kiểm thử Host Test Runner C99:** Chạy lệnh `make -C DoAn/AFE_ECG_PPG_PTT/firmware/esp32_ptt_streamer test` xác nhận **PASS 5/5 bài kiểm tra**:
   - Test 1: I2C Frequency Configuration (400kHz) -> PASS
   - Test 2: Dual ISR GPIO Interrupt & Timestamp Logic -> PASS
   - Test 3: FreeRTOS Telemetry Queue & Packet Drops Logic -> PASS
   - Test 4: UDP Packet Serialization & Struct Alignment -> PASS
   - Test 5: MAX30102 Register Sequences & FIFO Flush -> PASS
4. **Phân định minh bạch:** Các tuyên bố độ trễ $\le 2\text{ms}$ và $< 10\mu\text{s}$ trước đây là **chỉ tiêu thiết kế lý thuyết** được kiểm chứng qua host test mô phỏng; **CHƯA CÓ SỐ LIỆU ĐO THỰC TẾ TRÊN DAO ĐỘNG KÝ HOẶC LOGIC ANALYZER**. Môi trường hiện tại không có trình biên dịch chéo `xtensa-esp32-elf-gcc` / `idf.py`.

---

## 4. ĐỐI SOÁT ĐỘC LẬP PIPELINE DSP PAT (TASK T7)

Đã đối soát trực tiếp mã nguồn tại `DoAn/AFE_ECG_PPG_PTT/software/ptt_live_analyzer.py` và bộ kiểm thử `tests/test_dsp_ptt_pipeline.py`:

1. **Sửa lỗi đơn vị mẫu trong tính toán Tangent Foot:** Đã khắc phục lỗi chia nhầm khoảng lấy mẫu khiến giá trị chân sóng PPG trước đây bị lệch.
2. **Resampling nội suy 1000Hz:** Đã triển khai kiến trúc lưới nội suy $1000\text{Hz}$ để giải quyết bài toán hai nguồn xung clock bất đồng bộ giữa ADS1115 ($475\text{ SPS} \pm 10\%$ do dao động nội RC) và MAX30102 ($400\text{ SPS}$).
3. **Phân định luồng dữ liệu & Vô hiệu hóa PAT giả định:** Thuật toán chỉ tính toán PAT trên luồng dữ liệu mô phỏng tổng hợp (synthetic telemetry). Trên luồng dữ liệu firmware truyền về, tính năng tính PAT tự động bị khóa cho đến khi có phần cứng kiểm chuẩn nhãn thời gian vật lý.
4. **Tham số hóa bù trễ nhóm analog:** Giá trị bù trễ $5.6\text{ms}$ được cấu hình dạng tham số dòng lệnh `--ecg-relative-delay-ms` và ghi chú rõ đây là giá trị tính toán lý thuyết của bộ lọc Sallen-Key $41.4\text{Hz}$, cần hiệu chuẩn lại bằng thiết bị phát xung chuẩn ngoài phòng Lab.
5. **Kết quả kiểm thử Unit Test:** Chạy `python3 tests/test_dsp_ptt_pipeline.py` xác nhận **PASS 8/8 bài kiểm tra**:
   - Test 1: Pan-Tompkins QRS Detection -> PASS
   - Test 2: PPG Tangent Foot Detection -> PASS
   - Test 3: Delay Compensation Parameter -> PASS
   - Test 4: Artifact Rejection Filters -> PASS
   - Test 5: UDP Packet Parser & Flags Unpacking -> PASS
   - Test 6: Resampling Grid 1000Hz Integration -> PASS
   - Test 7: Output Summary JSON Metrics -> PASS
   - Test 8: End-to-End Pipeline Execution -> PASS

---

## 5. ĐỐI SOÁT DỰ TOÁN TÀI CHÍNH VÀ BOM

1. **Đối soát số học:** Tổng danh mục 11 khoản linh kiện liệt kê đạt con số $451.250\text{ VND}$ (hoặc $326.000\text{ VND}$ nếu có sẵn ESP32).
2. **Minh bạch tài chính:** Báo cáo kỹ thuật `BaoCao_DoAn.html` đã được hiệu chỉnh để nêu rõ đây là **dự toán lý thuyết danh mục linh kiện theo đơn giá catalog lẻ**, không phải là chi phí đặt hàng thực tế cuối cùng. Chi phí thực tế sẽ phụ thuộc vào cước vận chuyển quốc tế tối thiểu của LCSC ($\$15 - \$25$), phí đóng gói xử lý đơn hàng, thuế nhập khẩu và số lượng đặt hàng tối thiểu (MOQ) cho linh kiện cuộn SMD.

---

## 6. BẢNG PHÂN LOẠI MINH BẠCH BẰNG CHỨNG THỰC CHỨNG (STRICT EVIDENCE MATRIX)

| Hạng mục kỹ thuật | Bằng chứng đo đạc vật lý thực tế | Bằng chứng mô phỏng & Host Test | Tình trạng kiểm chứng |
| :--- | :---: | :---: | :---: |
| **Nguồn cấp +VS_A & LDO MCP1700** | Chưa có (chưa gia công bo) | Đạt (phân tích giải tích $I_q=171.6\mu\text{A}$, headroom $135\text{mV}$) | Cần đo DMM 6.5 digits tại phòng Lab |
| **Bus I2C 400kHz & Điện trở kéo 4.7k** | Chưa có | Đạt ($t_r=199.1\text{ns} < 300\text{ns}$ tại $C_b=50\text{pF}$) | Cần đo DSO 100MHz và Logic Analyzer |
| **Bộ lọc AFE HPF 0.48Hz & LPF 41.4Hz** | Chưa có | Đạt (công thức giải tích truyền dẫn $K=11\times$) | Cần đo máy phân tích mạng/phổ tín hiệu |
| **Bảo vệ ngõ vào & Dòng rò bệnh nhân** | Chưa có | Đạt (tính toán trở $360\text{k}\Omega$, $I_{fault}=9.17\mu\text{A} < 10\mu\text{A}$) | Cần đo thiết bị kiểm định an toàn điện y tế |
| **Độ trễ đồng bộ phần cứng $\le 2\text{ms}$** | Chưa có | Đạt (Host test runner logic ngắt IRAM ISR) | Cần đo DSO 2 kênh kích xung chuẩn |
| **Ước lượng PAT & Bù trễ nhóm 5.6ms** | Chưa có | Đạt (8/8 unit test trên synthetic telemetry) | Cần máy phát tín hiệu tim chuẩn Fluke/Rigol |
| **Quy chuẩn chế tạo PCB (DRC Clean)** | **KHÔNG ĐẠT (301 lỗi)** | Đã phát hiện 71 short-circuit, 39 tracks cross | **CHẶN CHẾ TẠO, REJECT GÓI GERBER** |
| **Tính toàn vẹn hồi tiếp Op-Amp R14** | **KHÔNG ĐẠT (Hở mạch)** | Đã phát hiện R14 nối nhầm vào REFOUT | **CHẶN CHẾ TẠO, BẮT BUỘC SỬA SCHEMATIC** |

---

## 7. KẾT LUẬN VÀ KIẾN NGHỊ NGHIỆM THU

1. **Kết luận kỹ thuật hiện trạng:**
   - Khối phần mềm & thuật toán (Firmware C99 và DSP Python) đã hoàn thiện tốt về mặt kiến trúc, giao thức truyền thông UDP 7 cờ và xử lý tín hiệu trên môi trường kiểm thử máy chủ.
   - Khối phần cứng PCB hiện tại tồn tại các lỗi chặn nghiêm trọng (301 lỗi DRC, đứt hồi tiếp âm R14) và gói xuất xưởng cũ (Gerber 19:49) **tiếp tục bị REJECT, đóng băng hoàn toàn**.
2. **Kế hoạch tiếp theo:**
   - Chuyển giao danh mục lỗi cho `pcb-hardware-engineer` để thực hiện vòng lặp thiết kế lại phần cứng theo yêu cầu của người dùng.
   - Nhóm QA sẽ thực hiện vòng kiểm định độc lập tiếp theo ngay khi nhận được bản phát hành phần cứng mới đã vượt qua kiểm tra DRC 0 lỗi và đồng bộ netlist với schematic.

---

## 8. HỒ SƠ BÀN GIAO TIẾP TỤC SỬA THIẾT KẾ PHẦN CỨNG (HANDOVER REPORT)

Hồ sơ bàn giao chi tiết cho agent / kỹ sư tiếp tục sửa mạch đã được ghi nhận tại:
- **Đường dẫn tệp bàn giao:** `DoAn/AFE_ECG_PPG_PTT/docs/BAN_GIAO_AGENT_SUA_MACH_ECG_PPG.md`
- **Bằng chứng DRC/Parity đính kèm:** `DoAn/AFE_ECG_PPG_PTT/docs/t2_evidence/restored_2301_drc_parity.rpt`
- **Bằng chứng ERC đính kèm:** `DoAn/AFE_ECG_PPG_PTT/docs/t2_evidence/restored_2301_erc.rpt`
- **Báo cáo đối soát phần cứng:** `DoAn/AFE_ECG_PPG_PTT/docs/DOI_SOAT_T2_VA_NGAN_CHAN_CHE_TAO.md`
- **Tệp cảnh báo chặn chế tạo tại thư mục đầu ra:** `DoAn/AFE_ECG_PPG_PTT/outputs/KHONG_SU_DUNG_DE_CHE_TAO.md`

Hồ sơ quy định rõ các bước sao lưu dự án, phân loại lỗi nghiêm trọng, đồng bộ schematic & PCB parity, sửa mạch nguyên lý AD8232/ADS1115/LDO và cam kết không tắt rule/bỏ qua cảnh báo để tạo kết quả giả.
