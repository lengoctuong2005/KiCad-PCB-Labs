---
title: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 06"
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
        content: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 06";
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
    margin-top: 10px;
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
        <div class="lab-name">Lab 06: Routing – Kỹ thuật Đi dây Mạch in, Cấu hình Trình đi dây Tương tác và Quản lý Via</div>
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

## BÀI TẬP VỀ NHÀ: HOÀN THIỆN VÀ TỐI ƯU HÓA ROUTING TRÊN PCB CÁ NHÂN

**Yêu cầu:** Thực hiện định tuyến (Routing) toàn bộ mạng dây cho bo mạch cá nhân (Mạch nguồn đa năng USB - UART - NE555) đảm bảo đầy đủ các nguyên tắc kỹ thuật: phân bổ Net Classes (IPC-2152), cấu hình Trình đi dây tương tác (Interactive Router), uốn góc 45°, quản lý chuyển lớp via tối ưu, dọn dẹp mạch in (Cleanup) và vượt qua kiểm tra DRC (0 Errors, 0 Warnings).

---

### 1. Cấu hình Trình đi dây Tương tác (Interactive Router)

Trình đi dây tương tác trong KiCad 10 cho phép định tuyến đường mạch bán tự động với khả năng kiểm soát va chạm theo thời gian thực dựa trên hệ thống Design Rules (DRC).

* **Ba chế độ định tuyến chính (Router Modes):**
  * **Highlight Collisions:** Đi dây thủ công, tô sáng màu xanh lá cây cảnh báo khi vi phạm khoảng cách an toàn (clearance).
  * **Shove (Chế độ tiêu chuẩn áp dụng):** Tự động đẩy các đường mạch hoặc via xung quanh dạt sang bên để mở lối đi cho đường mạch mới mà vẫn đảm bảo tuyệt đối khoảng cách an toàn. Đối với vật cản cố định (pad linh kiện hoặc track bị khóa), đường dây sẽ tự động luồn lách qua.
  * **Walk Around:** Tự động ôm sát biên dạng ngoài của các vật cản để tìm đường đi ngắn nhất mà không làm xê dịch đối tượng khác.

<div class="figure-container">
    <img class="report-img" src="Pic/hinh1_interactive_router_settings.png" alt="Hộp thoại Interactive Router Settings" style="max-height: 75mm;">
    <div class="figure-caption">Hình 1. Hộp thoại cấu hình Trình đi dây Tương tác (Interactive Router Settings) trong KiCad</div>
</div>

* **Bảng thiết lập tối ưu hóa đi dây trong Interactive Router:**

<table class="report-table">
<thead>
<tr>
<th style="width: 25%;">Tùy chọn (Option)</th>
<th style="width: 45%;">Ý nghĩa kỹ thuật</th>
<th style="width: 30%;">Thiết lập áp dụng</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>Mode</b></td>
<td>Chọn 1 trong 3 chế độ: Highlight collisions, Shove, Walk around</td>
<td><b>Shove</b> (để đi dây linh hoạt)</td>
</tr>
<tr>
<td><b>Shove vias</b></td>
<td>Cho phép đẩy via cùng với đường mạch khi phát sinh va chạm</td>
<td><b>Enabled</b> (tối ưu mật độ dây)</td>
</tr>
<tr>
<td><b>Jump over obstacles</b></td>
<td>Tự động nhảy vượt qua phía sau chướng ngại vật cố định</td>
<td><b>Enabled</b></td>
</tr>
<tr>
<td><b>Remove redundant tracks</b></td>
<td>Tự động xóa các vòng lặp (loops) dư thừa khi vẽ đường thay thế</td>
<td><b>Enabled</b> (chống tạo loop nhiễu)</td>
</tr>
<tr>
<td><b>Optimize pad connections</b></td>
<td>Tự động căn chỉnh hướng thoát dây ra khỏi pad, tránh góc nhọn</td>
<td><b>Enabled</b> (chống đứt gãy pad)</td>
</tr>
<tr>
<td><b>Smooth dragged segments</b></td>
<td>Làm mượt và gộp các đoạn dây khi kéo giãn để giảm số lần đổi hướng</td>
<td><b>Enabled</b></td>
</tr>
<tr>
<td><b>Allow DRC violations</b></td>
<td>Bỏ qua cảnh báo khoảng cách an toàn, cho phép đặt đè đường mạch</td>
<td><b>Disabled</b> (bảo đảm an toàn mạch)</td>
</tr>
</tbody>
</table>

<div class="page-break"></div>

### 2. Quy chuẩn Net Classes, Góc uốn 45° và Kỹ thuật Quản lý Via

#### 2.1. Tư thế đường mạch (Track Posture) và Góc uốn 45° (Corner Mode)
* **Tư thế đường mạch (Track Posture):** Sử dụng phím tắt **`/`** (*Switch Track Posture*) để đảo thứ tự ưu tiên giữa đoạn thẳng và đoạn chéo 45°.
* **Chế độ góc uốn 45°:** Sử dụng phím tắt **`Ctrl + /`** để thiết lập chế độ *45 degree*.
* **Nguyên tắc chống bẫy axit (Acid Traps) và giảm bức xạ EMI:** Toàn bộ đường mạch được vát góc 45° hoặc 135°, triệt tiêu tuyệt đối góc vuông 90° và góc nhọn (< 90°) nhằm ngăn chặn ứ đọng dung dịch ăn mòn hóa học gây đứt dây mạch và loại bỏ hiện tượng phát xạ nhiễu điện từ.

#### 2.2. Bảng phân bổ Net Classes và quy chuẩn bề rộng đường đồng (IPC-2152)

<table class="report-table">
<thead>
<tr>
<th style="width: 18%;">Tên Net Class</th>
<th style="width: 15%;">Độ rộng Track</th>
<th style="width: 15%;">Clearance</th>
<th style="width: 18%;">Via (Đường kính / Lỗ)</th>
<th style="width: 34%;">Các Net áp dụng & Chức năng</th>
</tr>
</thead>
<tbody>
<tr>
<td><b><code>Power_Main</code></b></td>
<td style="text-align: center; font-weight: bold;">0.80 mm</td>
<td style="text-align: center;">0.25 mm</td>
<td style="text-align: center;">0.80 / 0.40 mm</td>
<td><code>VBUS</code>, <code>+5V</code>, <code>+3.3V</code>, <code>-5V</code>, <code>GND</code> (Dòng tải lớn 1.0A-1.5A, chống sụt áp)</td>
</tr>
<tr>
<td><b><code>USB_Diff</code></b></td>
<td style="text-align: center; font-weight: bold;">0.30 mm</td>
<td style="text-align: center;">0.20 mm</td>
<td style="text-align: center;">0.60 / 0.30 mm</td>
<td><code>D+</code>, <code>D-</code> từ cổng Micro-USB (Cặp vi sai song hành, trở kháng vi sai 90 &Omega;)</td>
</tr>
<tr>
<td><b><code>Signal_UART</code></b></td>
<td style="text-align: center; font-weight: bold;">0.30 mm</td>
<td style="text-align: center;">0.20 mm</td>
<td style="text-align: center;">0.60 / 0.30 mm</td>
<td><code>TXD</code>, <code>RXD</code>, <code>RTS</code>, <code>CTS</code>, <code>DTR</code>, <code>CLK</code> (Tín hiệu logic 3.3V và xung NE555)</td>
</tr>
<tr>
<td><b><code>Default</code></b></td>
<td style="text-align: center; font-weight: bold;">0.40 mm</td>
<td style="text-align: center;">0.20 mm</td>
<td style="text-align: center;">0.60 / 0.30 mm</td>
<td>Các đường LED D1-D6, phân cực (Tín hiệu điều khiển chung trên bo mạch)</td>
</tr>
</tbody>
</table>

#### 2.3. Kỹ thuật Quản lý Via, Chuẩn bảo vệ IPC-4761 và Dọn dẹp mạch in (Cleanup)
* **Kỹ thuật chuyển lớp via:** Trong quá trình đi dây bằng lệnh **`X`**, nhấn phím **`V`** (*Place Via*) để chèn via xuyên lớp và chuyển đổi vùng làm việc giữa lớp mặt trên `F.Cu` và mặt dưới `B.Cu`.
* **Tiêu chuẩn bảo vệ Via (IPC-4761):** Áp dụng chế độ *Type I (Tenting)* phủ kín lớp mặt nạ hàn (Solder Mask) lên lỗ via chống oxy hóa; các via chịu dòng nguồn được tăng kích thước vành đồng lên 0.80 mm / lỗ 0.40 mm.
* **Dọn dẹp tối ưu hóa mạch in (Cleanup Tracks & Vias):** Chạy công cụ **Tools -> Cleanup Tracks & Vias...** để tự động gộp các đoạn thẳng hàng (*Merge co-linear tracks*), xóa các đoạn dây cụt bỏ lửng (*Delete tracks unconnected at one end*) và loại bỏ via trùng lặp (*Delete redundant vias*).

<div class="figure-container">
    <img class="report-img" src="Pic/hinh6_layer_via_switch.png" alt="Cấu hình kích thước Track và Via định sẵn" style="max-height: 58mm;">
    <div class="figure-caption">Hình 2. Hộp thoại cấu hình Track & Via Sizes</div>
</div>

<div class="page-break"></div>

<div class="figure-container">
    <img class="report-img" src="Pic/hinh13_cleanup_tracks_vias.png" alt="Hộp thoại Cleanup Tracks and Vias" style="max-height: 70mm;">
    <div class="figure-caption">Hình 3. Hộp thoại Cleanup Tracks & Vias</div>
</div>

### 3. Kết quả Thiết kế Bản vẽ 2D PCB Layout và Mô hình Phối cảnh 3D

Bo mạch nguồn đa năng kích thước 50 &times; 50 mm gồm 38 linh kiện và 29 nets đã được định tuyến hoàn chỉnh trên 2 lớp đồng (`F.Cu` và `B.Cu`), tích hợp đầy đủ khung bản vẽ Title Block chuẩn thông tin sinh viên.

#### 3.1. Bản vẽ Thiết kế 2D PCB Layout hoàn chỉnh

<div class="figure-container">
    <img class="report-img" src="Pic/lab6_layout_2d.png" alt="Bản vẽ 2D PCB Layout hoàn thiện" style="max-height: 120mm;">
    <div class="figure-caption">Hình 4. Bản vẽ 2D PCB Layout hoàn thiện (Lớp Top F.Cu màu đỏ, Lớp Bottom B.Cu màu xanh, Title Block cá nhân)</div>
</div>

<div class="page-break"></div>

#### 3.2. Phối cảnh 3D Render trực quan của Bo mạch hoàn thiện

<div class="figure-container">
    <img class="report-img" src="Pic/lab6_3d_top.png" alt="3D Top View" style="max-height: 65mm;">
    <div class="figure-caption">Hình 5. Phối cảnh 3D Mặt Trên (Top Layer F.Cu)</div>
</div>

<div class="figure-container">
    <img class="report-img" src="Pic/lab6_3d_bottom.png" alt="3D Bottom View" style="max-height: 65mm;">
    <div class="figure-caption">Hình 6. Phối cảnh 3D Mặt Dưới (Bottom Layer B.Cu)</div>
</div>

<div class="figure-container">
    <img class="report-img" src="Pic/lab6_3d_iso.png" alt="3D Isometric View" style="max-height: 65mm;">
    <div class="figure-caption">Hình 7. Phối cảnh 3D Đa góc nhìn (Isometric View) thể hiện độ hoàn thiện thực tế của bo mạch Lab 06</div>
</div>

<div class="page-break"></div>

### 4. Đánh giá Kiểm tra DRC và Chiến lược Tối ưu hóa Bo mạch

#### 4.1. Bảng Kiểm tra và Đánh giá Chất lượng Thiết kế

<table class="report-table">
<thead>
<tr>
<th style="width: 6%;">STT</th>
<th style="width: 32%;">Hạng mục kiểm tra</th>
<th style="width: 28%;">Tiêu chuẩn chất lượng</th>
<th style="width: 18%;">Kết quả thực tế</th>
<th style="width: 16%;">Đánh giá</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">1</td>
<td><b>Tỷ lệ kết nối mạng (Ratsnest)</b></td>
<td>100% các net được kết nối (0 unrouted)</td>
<td style="text-align: center; font-weight: bold;">0 unconnected</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
<tr>
<td style="text-align: center;">2</td>
<td><b>Góc chuyển hướng đường mạch</b></td>
<td>Vát góc 45° / 135°, triệt tiêu góc 90°</td>
<td style="text-align: center;">100% góc 45°</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
<tr>
<td style="text-align: center;">3</td>
<td><b>Độ rộng đường nguồn (<code>Power_Main</code>)</b></td>
<td>Bề rộng dây &ge; 0.80 mm theo Net Class</td>
<td style="text-align: center;">0.80 mm trục nguồn</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
<tr>
<td style="text-align: center;">4</td>
<td><b>Cặp vi sai USB (<code>D+</code>, <code>D-</code>)</b></td>
<td>Đi song hành đối xứng, cách ly nhiễu tốt</td>
<td style="text-align: center;">Song hành, không via</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
<tr>
<td style="text-align: center;">5</td>
<td><b>Bố trí Tụ lọc nguồn & Bypass</b></td>
<td>Nguồn &rarr; Tụ lọc &rarr; Chân cấp IC</td>
<td style="text-align: center;">Tụ ôm sát chân IC</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
<tr>
<td style="text-align: center;">6</td>
<td><b>Khoảng cách mép bo (<code>Edge.Cuts</code>)</b></td>
<td>Khoảng cách đường đồng &ge; 0.50 mm</td>
<td style="text-align: center;">1.0 mm &ndash; 2.5 mm</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
<tr>
<td style="text-align: center;">7</td>
<td><b>Tối ưu hóa Via xuyên lớp</b></td>
<td>Via 0.8/0.4mm (Nguồn), 0.6/0.3mm (Tín hiệu)</td>
<td style="text-align: center;">Số lượng tối thiểu</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
<tr>
<td style="text-align: center;">8</td>
<td><b>Dọn dẹp mạch in (Cleanup)</b></td>
<td>Không stub thừa, không via cụt 1 đầu</td>
<td style="text-align: center;">Đã tối ưu hoàn toàn</td>
<td style="text-align: center; font-weight: bold; color: #16a34a;">ĐẠT (Passed)</td>
</tr>
</tbody>
</table>

#### 4.2. Chiến lược Tối ưu hóa và Bài học Kinh nghiệm

* **Quy hoạch phân tầng (Layer Stackup Strategy):**
  * Lớp trên `F.Cu`: Định tuyến các đường tín hiệu ngắn, kết nối trực tiếp các chân linh kiện dán SMD (AMS1117, CP2102, NE555).
  * Lớp dưới `B.Cu`: Phân phối các trục nguồn chính liên kết giữa các cọc Jumpers và Header, tạo hành lang thông thoáng để chuẩn bị cho việc phủ đồng mặt phẳng mass (*Ground Plane*) ở Lab 07.
* **Kỹ thuật chống nhiễu cho khối tạo xung NE555:** Tụ lọc phân cực 10 &mu;F và tụ bypass 100 nF đặt sát chân 8 (VCC) và chân 5 (CV) của NE555. Đường xung ngõ ra `CLK_555` được cách ly với các đường truyền dữ liệu vi sai USB để tránh gây nhiễu chéo (*Crosstalk*).
* **Tối ưu hóa phân tán nhiệt và dòng tải cho IC nguồn:** Đường mạch ngõ ra `+3.3V` của AMS1117-3.3V (U1) được mở rộng lên 0.80 mm, tạo vùng đệm đồng tản nhiệt tại Pad số 2 (Tab) nhằm nâng cao độ bền và ổn định nhiệt.
* **Quy trình kiểm soát chất lượng:** Luôn ưu tiên đi dây đường nguồn và cặp vi sai USB trước; tận dụng chế độ Shove để tối ưu hóa không gian; chạy Cleanup Tracks & Vias và kiểm tra DRC đạt 0 lỗi trước khi bàn giao thiết kế.
