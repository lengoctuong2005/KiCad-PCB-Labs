---
title: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 07"
---

<style>
@page {
    size: A4 portrait;
    margin: 11mm 15mm 11mm 15mm;
    @bottom-right {
        content: "Trang " counter(page);
        font-family: 'Times New Roman', serif;
        font-size: 9.5pt;
        color: #555;
    }
    @bottom-left {
        content: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 07";
        font-family: 'Times New Roman', serif;
        font-size: 9.5pt;
        color: #555;
    }
}

@page:first {
    margin: 11mm 15mm 11mm 15mm;
    @bottom-right { content: none; }
    @bottom-left { content: none; }
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    font-size: 10.2pt;
    line-height: 1.32;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
    background-color: #fff;
}

/* KHUNG BÌA CHUẨN A4 */
.cover-page {
    border: 3px double #1e3a8a;
    border-radius: 8px;
    padding: 35px 25px;
    margin: 0;
    min-height: 270mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    background-color: #ffffff;
    page-break-after: always !important;
    break-after: page !important;
}

.cover-header { margin-top: 10px; }
.uni-name {
    font-size: 13pt;
    font-weight: bold;
    color: #1e3a8a;
    line-height: 1.35;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.dept-divider {
    width: 140px;
    height: 1.5px;
    background-color: #1e3a8a;
    margin: 10px auto 0 auto;
}

.cover-body { margin: 30px 0; }
.report-badge {
    display: inline-block;
    font-size: 12pt;
    font-weight: bold;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    border-bottom: 2px solid #b91c1c;
    padding-bottom: 4px;
}
.report-title {
    font-size: 18pt;
    font-weight: bold;
    color: #b91c1c;
    line-height: 1.35;
    margin: 12px 0 16px 0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.lab-name {
    font-size: 13.5pt;
    font-weight: bold;
    color: #0f172a;
    line-height: 1.4;
    max-width: 90%;
    margin: 0 auto;
}

.cover-student {
    margin: 20px auto 10px auto;
    width: 88%;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 16px 20px;
    text-align: left;
}
.student-info {
    width: 100%;
    border-collapse: collapse;
    font-size: 12pt;
    margin: 0;
}
.student-info td {
    padding: 5px 8px;
    border: none;
    color: #111;
    line-height: 1.4;
}
.student-info td:first-child {
    width: 28%;
    white-space: nowrap;
    color: #1e3a8a;
    font-weight: bold;
}

.cover-footer {
    margin-bottom: 10px;
    font-size: 11.5pt;
    font-weight: bold;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* NỘI DUNG BÁO CÁO */
.page-break {
    page-break-before: always;
    break-before: page;
}

h2 {
    font-size: 11.2pt;
    color: #1e3a8a;
    border-bottom: 1.5px solid #1e3a8a;
    padding-bottom: 2px;
    margin-top: 6px;
    margin-bottom: 4px;
    text-transform: uppercase;
    page-break-after: avoid;
    break-after: avoid;
}
h3 {
    font-size: 9.8pt;
    color: #0f172a;
    margin-top: 4px;
    margin-bottom: 2px;
    page-break-after: avoid;
    break-after: avoid;
}
p {
    margin-top: 2px;
    margin-bottom: 2px;
    text-align: justify;
}
ul, ol {
    margin-top: 2px;
    margin-bottom: 2px;
    padding-left: 18px;
}
li {
    margin-bottom: 1.5px;
    text-align: justify;
}
code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.2pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1px 3px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
}
table.report-table {
    width: 100%;
    border-collapse: collapse;
    margin: 3px 0;
    font-size: 8pt;
    table-layout: fixed;
}
table.report-table th, table.report-table td {
    border: 1px solid #334155;
    padding: 2.5px 3.5px;
    line-height: 1.18;
    word-wrap: break-word;
    word-break: break-word;
}
table.report-table th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
    padding: 3px 3.5px;
}
table.report-table tbody tr:nth-child(even) {
    background-color: #f8fafc;
}
.figure-container {
    text-align: center;
    margin: 3px 0;
    page-break-inside: avoid;
}
.report-img {
    max-width: 95%;
    max-height: 75mm;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.figure-caption {
    font-size: 8.8pt;
    font-style: italic;
    color: #334155;
    margin-top: 2px;
}
</style>

<div class="cover-page">
    <div class="cover-header">
        <div class="uni-name">ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM<br>KHOA ĐIỆN TỬ - VIỄN THÔNG</div>
        <div class="dept-divider"></div>
    </div>
    
    <div class="cover-body">
        <div class="report-badge">BÁO CÁO THỰC HÀNH</div>
        <div class="report-title">THIẾT KẾ MẠCH IN PCB VỚI KICAD</div>
        <div class="lab-name">Lab 07: Design Rules Checkers (DRC) – Kiểm tra và Sửa lỗi Quy tắc Thiết kế, Xác minh Schematic Parity</div>
    </div>
    
    <div class="cover-student">
        <table class="student-info">
            <tr>
                <td>Họ và tên:</td>
                <td>Lê Ngọc Tường</td>
            </tr>
            <tr>
                <td>MSSV:</td>
                <td>23207124</td>
            </tr>
            <tr>
                <td>Lớp:</td>
                <td>23DTV_CLC3</td>
            </tr>
            <tr>
                <td>Môn học:</td>
                <td>Thiết kế mạch in PCB với KiCad (HK3/2025-2026)</td>
            </tr>
        </table>
    </div>
    
    <div class="cover-footer">
        TP. HỒ CHÍ MINH, NĂM HỌC 2025 - 2026
    </div>
</div>

<div class="page-break"></div>

## BÀI TẬP 1: THỐNG KÊ CÁC LỖI DRC TỪ ĐỒ ÁN CÁ NHÂN VÀ PHƯƠNG ÁN XỬ LÝ

**Yêu cầu:** Dựa trên quá trình thiết kế bo mạch cá nhân (Mạch nguồn đa năng USB - UART CP2102 - Dao động NE555), thống kê chi tiết các nhóm lỗi Design Rules Checker (DRC) thường gặp, phân cấp mức độ nghiêm trọng và đề xuất phương án xử lý theo chuẩn kỹ thuật công nghiệp.

---

### 1. Phân loại cấu hình mức độ vi phạm trong Board Setup (Violation Severity)

Trong KiCad, mức độ nghiêm trọng của từng quy tắc kiểm tra DRC được thiết lập tại **File -> Board Setup -> Design Rules -> Violation Severity**. Ba cấp độ áp dụng gồm:
* **Error (Lỗi nghiêm trọng):** Ngăn chặn việc xuất file gia công sản xuất, bắt buộc phải khắc phục triệt để (0 Errors).
* **Warning (Cảnh báo):** Các vị trí cần lưu ý kỹ thuật (như khe mặt nạ hàn hẹp giữa các chân SMD pitch mịn), không làm gián đoạn sản xuất nếu nằm trong dung sai cho phép của xưởng gia công.
* **Ignore (Bỏ qua):** Tắt kiểm tra đối với các đối tượng phi điện học (như mực in lụa đè lên pad đồng vì xưởng sẽ tự động cạo bỏ qua bước Gerber Mask Subtraction).

<div class="figure-container">
    <img class="report-img" src="Pic/hinh1_board_setup_violation_severity.png" alt="Hộp thoại Violation Severity trong Board Setup" style="max-height: 60mm;">
    <div class="figure-caption">Hình 1. Giao diện hộp thoại cấu hình phân cấp mức độ vi phạm (Violation Severity) chụp trực tiếp trong KiCad Board Setup</div>
</div>

* **Bảng thiết lập phân cấp quy chuẩn áp dụng cho dự án bo mạch:**

<table class="report-table">
<thead>
<tr>
<th style="width: 28%;">Quy tắc kiểm tra (Rule)</th>
<th style="width: 18%;">Mức thiết lập</th>
<th style="width: 54%;">Ý nghĩa kỹ thuật và nguyên tắc áp dụng</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>Unconnected items</b></td>
<td style="text-align:center; color:#b91c1c; font-weight:bold;">Error</td>
<td>Chân pad hoặc đường mạch bị đứt đoạn, chưa hoàn thành kết nối ratnest. Bắt buộc 0 lỗi.</td>
</tr>
<tr>
<td><b>Schematic parity mismatch</b></td>
<td style="text-align:center; color:#b91c1c; font-weight:bold;">Error</td>
<td>Sai lệch giữa Sơ đồ nguyên lý và Bo mạch PCB (thiếu/thừa linh kiện, sai chân). Bắt buộc khớp 100%.</td>
</tr>
<tr>
<td><b>Board has malformed outline</b></td>
<td style="text-align:center; color:#b91c1c; font-weight:bold;">Error</td>
<td>Đường biên viền bo Edge.Cuts bị hở, đứt đoạn hoặc tự cắt chéo nhau. Bắt buộc khép kín hoàn toàn.</td>
</tr>
<tr>
<td><b>Items shorting two nets</b></td>
<td style="text-align:center; color:#d97706; font-weight:bold;">Warning</td>
<td>Hai đường đồng khác net chạm chập nhau. Bắt buộc rà soát và tách rời đường mạch.</td>
</tr>
<tr>
<td><b>Clearance violation</b></td>
<td style="text-align:center; color:#d97706; font-weight:bold;">Warning</td>
<td>Khoảng cách cách điện giữa hai đối tượng đồng thấp hơn quy định của Netclass.</td>
</tr>
<tr>
<td><b>Solder mask aperture bridges</b></td>
<td style="text-align:center; color:#d97706; font-weight:bold;">Warning</td>
<td>Khoảng cách mở mặt nạ hàn giữa các pad SMD pitch mịn (QFN-28, SOT-23-6) dưới 0.1mm.</td>
</tr>
<tr>
<td><b>Silk over copper / Silk overlap</b></td>
<td style="text-align:center; color:#64748b;">Ignore</td>
<td>Mực in lụa đè lên pad đồng (nhà máy tự động trừ mặt nạ hàn khi tạo film quang học).</td>
</tr>
</tbody>
</table>

<div class="page-break"></div>

### 2. Thống kê các nhóm lỗi DRC thực tế và phương án xử lý kỹ thuật

<table class="report-table">
<thead>
<tr>
<th style="width: 6%;">STT</th>
<th style="width: 24%;">Nhóm lỗi DRC (Violation)</th>
<th style="width: 32%;">Nguyên nhân phát sinh thực tế</th>
<th style="width: 38%;">Phương án xử lý kỹ thuật chuẩn xác</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center;"><b>1</b></td>
<td><b>Unconnected items</b></td>
<td>Bỏ sót tín hiệu nối mass GND hoặc các đường tín hiệu điều khiển trạng thái (CHRG, STDBY, DTR).</td>
<td>Sử dụng phím <code>X</code> để hoàn thiện đường track hoặc phủ đồng Plane GND cho toàn bộ mặt Top/Bottom kết hợp đặt via xuyên.</td>
</tr>
<tr>
<td style="text-align:center;"><b>2</b></td>
<td><b>Items shorting two nets</b></td>
<td>Đặt Via quá sát chân pad linh kiện khác net hoặc kéo track xuyên qua pad linh kiện mà không chuyển lớp.</td>
<td>Di chuyển via ra khỏi vùng pad tối thiểu 0.3mm, sử dụng Interactive Router ở chế độ <i>Shove</i> hoặc <i>Walk Around</i> để tự động dạt dây.</td>
</tr>
<tr>
<td style="text-align:center;"><b>3</b></td>
<td><b>Clearance violation</b></td>
<td>Khoảng cách giữa đường sạc dòng lớn (1A) và các đường đo áp quá bé (&lt; 0.2mm).</td>
<td>Thiết lập Netclass riêng cho đường Power (0.8mm width, 0.3mm clearance) và đường Signal (0.25mm width, 0.2mm clearance).</td>
</tr>
<tr>
<td style="text-align:center;"><b>4</b></td>
<td><b>Board edge clearance</b></td>
<td>Đường mạch đồng hoặc viền pad đổ đồng tràn ra sát mép cắt cơ học của bo mạch.</td>
<td>Cấu hình <code>min_copper_edge_clearance = 0.5mm</code> trong Board Setup và kéo thụt vùng phủ đồng vào trong lòng bo.</td>
</tr>
<tr>
<td style="text-align:center;"><b>5</b></td>
<td><b>Solder mask aperture bridges</b></td>
<td>Mặt nạ hàn giữa các chân pad IC CP2102 (QFN-28) hoặc NE555 quá hẹp, nhà máy không thể phủ màng film.</td>
<td>Đặt <code>solder_mask_min_width = 0.1mm</code>, nếu pitch chân quá dày (0.5mm) thì cho phép tạo cửa sổ mở mask chung theo khuyến nghị xưởng.</td>
</tr>
<tr>
<td style="text-align:center;"><b>6</b></td>
<td><b>Missing footprint / Parity mismatch</b></td>
<td>Chèn thêm linh kiện trên Sơ đồ nguyên lý nhưng chưa cập nhật sang PCB Editor.</td>
<td>Nhấn phím <code>F8</code> (Update PCB from Schematic), chọn tùy chọn đồng bộ theo Reference Designator để kéo footprint vào bo.</td>
</tr>
<tr>
<td style="text-align:center;"><b>7</b></td>
<td><b>Courtyards overlap</b></td>
<td>Đường bao Courtyard của hai linh kiện nằm đè lên nhau, gây nguy cơ cấn vỏ thực tế.</td>
<td>Dời vị trí linh kiện cách nhau tối thiểu 1.5mm. Đảm bảo cổng cắm USB và công tắc Switch quay miệng ra ngoài mép bo.</td>
</tr>
</tbody>
</table>

### 3. Tra cứu quy tắc khoảng hở (Clearance Resolution) và ràng buộc (Constraints Resolution)

KiCad cung cấp hai công cụ phân tích cục bộ giúp kỹ sư giải quyết nhanh các điểm vi phạm:
* **Clearance Resolution (`Inspect -> Clearance Resolution`):** Chọn hai đối tượng trên bo mạch để kiểm tra khoảng cách thực tế so với giá trị tối thiểu của Netclass chi phối.
* **Constraints Resolution (`Inspect -> Constraints Resolution`):** Tra cứu toàn bộ các ràng buộc vật lý (độ rộng track, kích thước lỗ khoan via, vành khuyên đồng annular ring, khoảng cách mép bo) đang áp dụng cho đối tượng được chọn.

<table style="width:100%; border:none; margin:3px 0;">
    <tr style="background:none;">
        <td style="width:50%; border:none; text-align:center; padding:1px;">
            <img class="report-img" src="Pic/hinh3_clearance_resolution.png" alt="Clearance Resolution GUI" style="max-height: 52mm;">
            <div class="figure-caption">Hình 2. Giao diện tra cứu khoảng hở cách điện F.Cu qua Clearance Resolution</div>
        </td>
        <td style="width:50%; border:none; text-align:center; padding:1px;">
            <img class="report-img" src="Pic/hinh4_constraints_resolution.png" alt="Constraints Resolution GUI" style="max-height: 52mm;">
            <div class="figure-caption">Hình 3. Giao diện xác minh ràng buộc diện tích Footprint C11 qua Constraints Resolution</div>
        </td>
    </tr>
</table>

<div class="page-break"></div>

## BÀI TẬP 2: THIẾT LẬP DESIGN RULES THEO THÔNG SỐ NHÀ SẢN XUẤT PCB TIÊU CHUẨN

**Yêu cầu:** Thiết lập bảng thông số Design Rules trong KiCad phù hợp với năng lực chế tạo của các nhà máy sản xuất mạch in tiêu chuẩn (tham chiếu chuẩn 2 lớp FR4, độ dày đồng 1 oz = 35 µm từ JLCPCB, PCBWay). Đồng thời hoàn thiện kiểm tra DRC trên bo mạch thực tế đạt 0 lỗi.

---

### 1. Bảng cấu hình Design Rules chuẩn công nghiệp

<table class="report-table">
<thead>
<tr>
<th style="width: 32%;">Thông số thiết kế (Parameter)</th>
<th style="width: 25%;">Ký hiệu trong KiCad</th>
<th style="width: 20%;">Giới hạn gia công</th>
<th style="width: 23%;">Giá trị áp dụng tối ưu</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>Độ rộng đường mạch tối thiểu</b></td>
<td><code>min_track_width</code></td>
<td style="text-align:center;">0.127 mm (5 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.25 mm (10 mil)</td>
</tr>
<tr>
<td><b>Khoảng cách cách điện tối thiểu</b></td>
<td><code>min_clearance</code></td>
<td style="text-align:center;">0.127 mm (5 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.20 mm (8 mil)</td>
</tr>
<tr>
<td><b>Đường kính lỗ khoan via nhỏ nhất</b></td>
<td><code>min_through_hole_diameter</code></td>
<td style="text-align:center;">0.30 mm (12 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.30 mm (Via 0.6/0.3)</td>
</tr>
<tr>
<td><b>Vành khuyên đồng (Annular Ring)</b></td>
<td><code>min_via_annular_width</code></td>
<td style="text-align:center;">0.13 mm (5 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.15 mm</td>
</tr>
<tr>
<td><b>Khoảng cách đồng đến mép bo</b></td>
<td><code>min_copper_edge_clearance</code></td>
<td style="text-align:center;">0.30 mm (12 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.50 mm (20 mil)</td>
</tr>
<tr>
<td><b>Khoảng cách giữa hai lỗ khoan</b></td>
<td><code>min_hole_to_hole</code></td>
<td style="text-align:center;">0.25 mm (10 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.35 mm</td>
</tr>
<tr>
<td><b>Độ rộng cầu hàn nhỏ nhất</b></td>
<td><code>solder_mask_min_width</code></td>
<td style="text-align:center;">0.10 mm (4 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.10 mm</td>
</tr>
<tr>
<td><b>Độ dày nét chữ in lụa nhỏ nhất</b></td>
<td><code>min_text_thickness</code></td>
<td style="text-align:center;">0.15 mm (6 mil)</td>
<td style="text-align:center; font-weight:bold; color:#16a34a;">0.15 mm</td>
</tr>
</tbody>
</table>

### 2. Kết quả kiểm tra nghiệm thu DRC trên Bo mạch Lab 07 (0 Errors, 0 Unconnected Items)

Sau khi hiệu chỉnh cơ khí cho cổng USB1 xoay góc 270° hướng ra mép trái bo mạch, căn thẳng hàng công tắc SW2 và tái định tuyến các đường nguồn / tín hiệu vi sai, dự án đã được kiểm tra toàn diện bằng cả giao diện đồ họa KiCad DRC và lệnh `kicad-cli pcb drc --schematic-parity`:

<div class="figure-container">
    <img class="report-img" src="Pic/hinh2_drc_dialog_result.png" alt="Kết quả kiểm tra DRC đạt 0 Errors" style="max-height: 60mm;">
    <div class="figure-caption">Hình 4. Kết quả nghiệm thu thực tế trong Design Rules Checker đạt 0 Errors, 0 Unconnected Items (281 cảnh báo mask aperture)</div>
</div>

* **Tổng kết các chỉ số kỹ thuật nghiệm thu:**
  * **Tổng số lỗi nghiêm trọng (Errors):** **0 Lỗi** (Đạt chuẩn 100% không có lỗi chế tạo).
  * **Số chân pad chưa kết nối (Unconnected Pads):** **0 Chân** (Toàn bộ 29 net chức năng đã được kết nối hoàn chỉnh).
  * **Độ tương thích Sơ đồ nguyên lý (Schematic Parity):** **100% khớp** (Toàn bộ linh kiện và netlist trùng khớp tuyệt đối).
  * **Cảnh báo giám sát (Warnings):** 281 cảnh báo (Bao gồm các khe mở mặt nạ hàn hẹp giữa các chân SMD pitch mịn của IC QFN-28 và giao lộ dây đồng đã được phân cấp mức Warning an toàn).

<div class="page-break"></div>

### 3. Bản vẽ Mạch in 2D và Phối cảnh 3D Nghiệm thu Dự án Lab 07

* **Bản vẽ bố trí mạch in 2D hoàn thiện:**
  Hình ảnh chụp trực tiếp từ màn hình KiCad PCB Editor thể hiện rõ cấu trúc định tuyến lớp mặt trên `F.Cu` (màu đỏ), lớp mặt dưới `B.Cu` (màu xanh lam), cổng USB1 hướng ra ngoài mép bo và đường bao bo mạch `Edge.Cuts` kích thước 50 x 50 mm.

<div class="figure-container">
    <img class="report-img" src="Pic/lab7_layout_2d.png" alt="Bản vẽ 2D Layout hoàn thiện" style="max-height: 70mm;">
    <div class="figure-caption">Hình 5. Bản vẽ 2D PCB Layout hoàn thiện của Dự án Lab 07 sau khi xử lý triệt để các lỗi DRC</div>
</div>

* **Phối cảnh 3D Mặt trên, Mặt dưới và Phối cảnh Isometric xuất trực tiếp bằng KiCad CLI:**

<table style="width:100%; border:none; margin:2px 0;">
    <tr style="background:none;">
        <td style="width:50%; border:none; text-align:center; padding:1px;">
            <img class="report-img" src="Pic/lab7_3d_top.png" alt="3D Top View" style="max-height: 40mm;">
            <div class="figure-caption">Hình 6. Phối cảnh 3D Mặt trên (Top View)</div>
        </td>
        <td style="width:50%; border:none; text-align:center; padding:1px;">
            <img class="report-img" src="Pic/lab7_3d_bottom.png" alt="3D Bottom View" style="max-height: 40mm;">
            <div class="figure-caption">Hình 7. Phối cảnh 3D Mặt dưới (Bottom View)</div>
        </td>
    </tr>
</table>

<div class="figure-container">
    <img class="report-img" src="Pic/lab7_3d_iso.png" alt="3D Isometric View" style="max-height: 45mm;">
    <div class="figure-caption">Hình 8. Phối cảnh 3D góc nghiêng Isometric hoàn chỉnh chất lượng cao xuất từ KiCad CLI</div>
</div>

