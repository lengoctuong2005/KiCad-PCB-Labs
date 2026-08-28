---
title: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 04"
---

<style>
@page {
    size: A4 portrait;
    margin: 14mm 16mm 14mm 16mm;
    @bottom-right {
        content: "Trang " counter(page);
        font-family: 'Times New Roman', serif;
        font-size: 10pt;
        color: #555;
    }
    @bottom-left {
        content: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 04";
        font-family: 'Times New Roman', serif;
        font-size: 10pt;
        color: #555;
    }
}

@page:first {
    margin: 14mm 16mm 14mm 16mm;
    @bottom-right { content: none; }
    @bottom-left { content: none; }
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    font-size: 11pt;
    line-height: 1.4;
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
    min-height: 262mm;
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
    font-size: 12pt;
    color: #1e3a8a;
    border-bottom: 1.5px solid #1e3a8a;
    padding-bottom: 3px;
    margin-top: 8px;
    margin-bottom: 6px;
    text-transform: uppercase;
    page-break-after: avoid;
    break-after: avoid;
}
h3 {
    font-size: 10.5pt;
    color: #0f172a;
    margin-top: 6px;
    margin-bottom: 3px;
    page-break-after: avoid;
    break-after: avoid;
}
p {
    margin-top: 2px;
    margin-bottom: 3px;
    text-align: justify;
}
ul, ol {
    margin-top: 2px;
    margin-bottom: 3px;
    padding-left: 18px;
}
li {
    margin-bottom: 2px;
    text-align: justify;
}
code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1px 3px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
}
table.report-table {
    width: 100%;
    border-collapse: collapse;
    margin: 5px 0;
    font-size: 8.5pt;
    table-layout: fixed;
}
table.report-table th, table.report-table td {
    border: 1px solid #334155;
    padding: 3.5px 5px;
    line-height: 1.25;
    word-wrap: break-word;
    word-break: break-word;
}
table.report-table th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
    padding: 4px 4px;
}
table.report-table tbody tr:nth-child(even) {
    background-color: #f8fafc;
}
.figure-container {
    text-align: center;
    margin: 5px 0;
    page-break-inside: avoid;
}
.report-img {
    max-width: 96%;
    max-height: 98mm;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.figure-caption {
    font-size: 9.5pt;
    font-style: italic;
    color: #334155;
    margin-top: 3px;
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
        <div class="lab-name">Lab 04: Thiết lập PCB, Cấu hình Board Outline, Stackup, Design Rules và Net Classes</div>
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

## CÂU 1: HOÀN THÀNH ĐẦY ĐỦ CÁC BƯỚC THIẾT LẬP PCB CHO MẠCH NGUỒN ĐA NĂNG

Mục tiêu của bài tập là chuyển đổi toàn bộ sơ đồ nguyên lý mạch nguồn đa năng từ Schematic sang PCB Editor, thiết lập khung viền cơ khí bo mạch, cấu hình cấu trúc lớp vật lý (Physical Stackup) và phân loại các nhóm mạng (Net Classes).

### 1.1. Đồng bộ dữ liệu Schematic sang PCB Editor (Update PCB from Schematic)

* **Thao tác thực hiện:** Trong giao diện PCB Editor, mở menu `Tools -> Update PCB from Schematic...` (phím tắt `F8`).
* **Kiểm tra trạng thái:** Hộp thoại hiển thị danh sách toàn bộ footprint và mạng kết nối (netlist). Quá trình kiểm tra đạt `Total warnings: 0, errors: 0`, xác nhận không có xung đột hay thiếu footprint. Bấm **Update PCB** để nạp linh kiện vào vùng làm việc.

### 1.2. Thiết lập đường bao bo mạch trên lớp Edge.Cuts (Board Outline)

* **Nguyên tắc kỹ thuật:** Lớp `Edge.Cuts` xác định biên dạng cắt thực tế của bo mạch. Đường bao trên lớp này phải tạo thành một đa giác khép kín hoàn toàn và không tự giao cắt.
* **Các bước thực hiện:**
  1. Chuyển bước lưới (Grid) về giá trị 1.0 mm hoặc 0.5 mm để căn chỉnh kích thước chuẩn xác.
  2. Chọn lớp hoạt động là **`Edge.Cuts`** trên bảng điều khiển Appearance.
  3. Dùng công cụ *Draw Rectangle*, vẽ đường bao bo mạch kích thước 50 x 50 mm bao quanh toàn bộ linh kiện đã sắp xếp của mạch nguồn.

<div class="figure-container">
    <img class="report-img" src="Pic/gui_pcb_editor.png" alt="Giao diện KiCad PCB Editor sau khi đồng bộ linh kiện và vẽ Edge.Cuts" style="max-height: 100mm;">
    <div class="figure-caption">Hình 1. Giao diện KiCad PCB Editor sau khi hoàn tất đồng bộ từ Schematic, vẽ đường bao cơ khí Edge.Cuts và hiển thị đường nối mạng (Ratsnest)</div>
</div>

<div class="page-break"></div>

### 1.3. Cấu hình cấu trúc lớp bo mạch (Physical Stackup)

Vào `File -> Board Setup... -> Board Stackup -> Physical Stackup` để cấu hình cấu trúc lớp vật lý cho mạch nguồn:

* **Số lớp đồng (Copper Layers):** Chọn cấu hình **2 lớp** (`F.Cu` và `B.Cu`), đáp ứng hoàn toàn nhu cầu truyền dẫn dòng và tín hiệu, tối ưu chi phí gia công.
* **Vật liệu lõi cách điện:** Chuẩn công nghiệp **FR4** với hằng số điện môi xấp xỉ 4.5.

<table class="report-table">
    <thead>
        <tr>
            <th style="width: 8%;">STT</th>
            <th style="width: 25%;">Thành phần lớp</th>
            <th style="width: 22%;">Tên lớp trong KiCad</th>
            <th style="width: 18%;">Độ dày</th>
            <th style="width: 27%;">Chức năng kỹ thuật</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: center;">1</td>
            <td>Lớp phủ bảo vệ mặt trên</td>
            <td><code>Top Solder Mask</code></td>
            <td>0.010 mm (10 µm)</td>
            <td>Chống oxy hóa đồng, mở lỗ pad hàn</td>
        </tr>
        <tr>
            <td style="text-align: center;">2</td>
            <td>Lớp đồng mặt trước</td>
            <td><code>F.Cu (Front Copper)</code></td>
            <td>0.035 mm (1 oz Cu)</td>
            <td>Đi dây tín hiệu, đặt linh kiện SMD</td>
        </tr>
        <tr>
            <td style="text-align: center;">3</td>
            <td>Lõi cách điện trung tâm</td>
            <td><code>Dielectric Core (FR4)</code></td>
            <td>1.510 mm</td>
            <td>Cách điện và định hình cơ học bo mạch</td>
        </tr>
        <tr>
            <td style="text-align: center;">4</td>
            <td>Lớp đồng mặt sau</td>
            <td><code>B.Cu (Back Copper)</code></td>
            <td>0.035 mm (1 oz Cu)</td>
            <td>Đi dây nguồn, phủ đồng mặt phẳng mass (GND)</td>
        </tr>
        <tr>
            <td style="text-align: center;">5</td>
            <td>Lớp phủ bảo vệ mặt dưới</td>
            <td><code>Bottom Solder Mask</code></td>
            <td>0.010 mm (10 µm)</td>
            <td>Chống chạm chập mặt dưới khi hàn</td>
        </tr>
        <tr>
            <td colspan="3" style="text-align: right; font-weight: bold;">Tổng độ dày bo mạch:</td>
            <td style="font-weight: bold;">1.600 mm</td>
            <td style="font-weight: bold;">Độ dày tiêu chuẩn mạch FR-4 2 lớp</td>
        </tr>
    </tbody>
</table>

<div class="figure-container">
    <img class="report-img" src="Pic/gui_physical_stackup.png" alt="Hộp thoại cấu hình Physical Stackup trong Board Setup" style="max-height: 80mm;">
    <div class="figure-caption">Hình 2. Giao diện cấu hình cấu trúc lớp bo mạch Physical Stackup (2 lớp đồng, lõi FR4, tổng độ dày 1.6 mm)</div>
</div>

<div class="page-break"></div>

### 1.4. Phân nhóm và cấu hình lớp mạng (Net Classes)

Net Class quản lý luật thiết kế theo từng nhóm mạng điện, cho phép tự động áp dụng bề rộng đường mạch (*Track Width*), khoảng cách cách ly (*Clearance*) và kích thước lỗ via (*Via Size*) phù hợp cho từng loại tín hiệu:

* **Nhóm nguồn tải lớn (`Power_Main`):** Gồm `VBUS`, `+5V`, `+3.3V`, `-5V` và `GND`. Bề rộng track đặt 0.80 mm để giảm nội trở đường dây, hạn chế sụt áp và chịu dòng tải tốt.
* **Nhóm tín hiệu vi sai USB (`USB_Diff`):** Gồm cặp net `D+` và `D-` từ cổng Micro-USB. Bề rộng track 0.30 mm và khoảng cách vi sai 0.20 mm để phối hợp trở kháng đường truyền.
* **Nhóm tín hiệu UART và xung clock (`Signal_UART`):** Gồm `TXD`, `RXD`, `RTS`, `CTS`, `DTR` và `CLK_555`. Bề rộng track 0.30 mm để đường mạch gọn gàng và dễ layout.
* **Nhóm tín hiệu mặc định (`Default`):** Áp dụng cho các đường tín hiệu điều khiển còn lại với bề rộng track 0.40 mm.

Vào `File -> Board Setup... -> Design Rules -> Net Classes` để thiết lập các nhóm lớp mạng:

<table class="report-table">
    <thead>
        <tr>
            <th style="width: 15%;">Tên Net Class</th>
            <th style="width: 12%;">Clearance</th>
            <th style="width: 14%;">Track Width</th>
            <th style="width: 13%;">Via Diameter</th>
            <th style="width: 12%;">Via Drill</th>
            <th style="width: 34%;">Danh sách các Net được gán</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong><code>Default</code></strong></td>
            <td>0.20 mm</td>
            <td>0.40 mm</td>
            <td>0.60 mm</td>
            <td>0.30 mm</td>
            <td>Các net tín hiệu chưa phân lớp riêng</td>
        </tr>
        <tr>
            <td><strong><code>Power_Main</code></strong></td>
            <td>0.25 mm</td>
            <td><strong>0.80 mm</strong></td>
            <td><strong>0.80 mm</strong></td>
            <td><strong>0.40 mm</strong></td>
            <td><code>VBUS</code>, <code>+5V</code>, <code>+3.3V</code>, <code>-5V</code>, <code>GND</code></td>
        </tr>
        <tr>
            <td><strong><code>USB_Diff</code></strong></td>
            <td>0.20 mm</td>
            <td><strong>0.30 mm</strong></td>
            <td>0.60 mm</td>
            <td>0.30 mm</td>
            <td>Cặp tín hiệu vi sai <code>D+</code>, <code>D-</code></td>
        </tr>
        <tr>
            <td><strong><code>Signal_UART</code></strong></td>
            <td>0.20 mm</td>
            <td><strong>0.30 mm</strong></td>
            <td>0.60 mm</td>
            <td>0.30 mm</td>
            <td><code>TXD</code>, <code>RXD</code>, <code>RTS</code>, <code>CTS</code>, <code>DTR</code>, <code>CLK_555</code></td>
        </tr>
    </tbody>
</table>

<div class="figure-container">
    <img class="report-img" src="Pic/gui_net_classes.png" alt="Hộp thoại cấu hình Net Classes trong Board Setup" style="max-height: 78mm;">
    <div class="figure-caption">Hình 3. Giao diện phân loại và cấu hình thông số kỹ thuật cho các nhóm Net Classes trong KiCad</div>
</div>

<div class="page-break"></div>

## CÂU 2: THIẾT LẬP LẠI DESIGN RULES THEO CHUẨN NHÀ SẢN XUẤT PCB DỰ KIẾN

Thay vì sử dụng các giá trị mặc định của KiCad (thường quá chặt hoặc chưa phù hợp với năng lực sản xuất thực tế dẫn đến tăng chi phí hoặc lỗi DFM), các thông số ràng buộc thiết kế (*Design Rules Constraints*) được cấu hình lại theo đúng thông số công bố của nhà sản xuất PCB tiêu chuẩn (JLCPCB / PCBWay 2-layer standard process).

Vào `File -> Board Setup... -> Design Rules -> Constraints` để thiết lập các giới hạn kích thước tối thiểu:

<table class="report-table">
    <thead>
        <tr>
            <th style="width: 28%;">Thông số ràng buộc</th>
            <th style="width: 18%;">Mặc định KiCad</th>
            <th style="width: 20%;">Chuẩn xưởng gia công</th>
            <th style="width: 34%;">Ý nghĩa kỹ thuật</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Minimum clearance</strong></td>
            <td>0.00 mm</td>
            <td><strong>0.20 mm</strong> (8 mil)</td>
            <td>Khoảng cách an toàn giữa hai đường đồng khác net</td>
        </tr>
        <tr>
            <td><strong>Minimum track width</strong></td>
            <td>0.20 mm</td>
            <td><strong>0.25 mm</strong> (10 mil)</td>
            <td>Bề rộng nhỏ nhất của đường mạch, tránh đứt khi ăn mòn</td>
        </tr>
        <tr>
            <td><strong>Minimum via diameter</strong></td>
            <td>0.50 mm</td>
            <td><strong>0.60 mm</strong> (24 mil)</td>
            <td>Đường kính vòng khuyên ngoài nhỏ nhất của lỗ via</td>
        </tr>
        <tr>
            <td><strong>Minimum via drill size</strong></td>
            <td>0.30 mm</td>
            <td><strong>0.30 mm</strong> (12 mil)</td>
            <td>Đường kính mũi khoan nhỏ nhất của via chuyển lớp</td>
        </tr>
        <tr>
            <td><strong>Copper to hole clearance</strong></td>
            <td>0.25 mm</td>
            <td><strong>0.30 mm</strong> (12 mil)</td>
            <td>Khoảng cách từ mép đường đồng đến mép lỗ khoan</td>
        </tr>
        <tr>
            <td><strong>Copper to edge clearance</strong></td>
            <td>0.50 mm</td>
            <td><strong>0.50 mm</strong> (20 mil)</td>
            <td>Khoảng cách từ đường đồng đến đường cắt viền bo Edge.Cuts</td>
        </tr>
        <tr>
            <td><strong>Hole to hole clearance</strong></td>
            <td>0.25 mm</td>
            <td><strong>0.30 mm</strong> (12 mil)</td>
            <td>Khoảng cách giữa hai mép lỗ khoan để tránh nứt phôi FR4</td>
        </tr>
    </tbody>
</table>

<div class="figure-container">
    <img class="report-img" src="Pic/gui_design_rules.png" alt="Hộp thoại thiết lập Design Rules Constraints trong Board Setup" style="max-height: 80mm;">
    <div class="figure-caption">Hình 4. Giao diện thiết lập ràng buộc luật thiết kế Constraints theo thông số xưởng sản xuất</div>
</div>

<div class="page-break"></div>

### KIỂM TRA MÔ HÌNH 3D VÀ ĐÁNH GIÁ TRỰC QUAN BO MẠCH

Sau khi hoàn tất toàn bộ các bước thiết lập trong Bài tập về nhà (đồng bộ Schematic, vẽ Board Outline, cấu hình Layer Stackup, Design Rules và Net Classes), mô hình 3D của bo mạch được mở và kiểm tra trực quan bằng công cụ **3D Viewer** tích hợp trong KiCad (`Alt + 3`).

<div class="figure-container">
    <img class="report-img" src="Pic/gui_3d_viewer.png" alt="Giao diện cửa sổ 3D Viewer trong KiCad" style="max-height: 92mm;">
    <div class="figure-caption">Hình 5. Cửa sổ công cụ 3D Viewer trong KiCad kiểm tra hình học và sự phân bố linh kiện trên khung viền cơ khí</div>
</div>

<div class="figure-container" style="margin-top: 8px;">
    <img class="report-img" src="Pic/3d_board_isometric.png" alt="Phối cảnh 3D bo mạch Isometric View" style="max-height: 85mm;">
    <div class="figure-caption">Hình 6. Mô hình 3D góc phối cảnh Isometric toàn bo mạch nguồn đa năng sau khi hoàn thiện toàn bộ thiết lập</div>
</div>
