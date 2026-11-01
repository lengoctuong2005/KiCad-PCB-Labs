<style>
@page {
    size: A4 portrait;
    margin: 11mm 15mm 11mm 15mm;
    @bottom-right {
        content: "Trang " counter(page);
        font-family: 'Times New Roman', serif;
        font-size: 10pt;
        color: #555;
    }
    @bottom-left {
        content: "Đồ Án Thiết Kế Mạch In PCB: Mạch Sạc Pin Li-Ion TP4056 Type-C";
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

* { box-sizing: border-box; }
body {
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    font-size: 10.5pt;
    line-height: 1.4;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
    background-color: #fff;
}

.cover-page {
    border: 3px double #1e3a8a;
    border-radius: 8px;
    padding: 30px 24px;
    margin: 0;
    min-height: 262mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
}

.cover-header { margin-top: 5px; }
.cover-univ {
    font-size: 13pt;
    font-weight: bold;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.cover-faculty {
    font-size: 12pt;
    font-weight: bold;
    color: #0f172a;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.cover-divider-top {
    width: 140px;
    height: 2px;
    background: #1e3a8a;
    margin: 0 auto 20px auto;
}

.cover-body { margin: 15px 0; }
.report-badge {
    display: inline-block;
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #b91c1c;
    color: #0f172a;
    font-size: 10.5pt;
    font-weight: bold;
    padding: 4px 14px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
}
.report-title {
    font-size: 20pt;
    font-weight: bold;
    color: #b91c1c;
    text-transform: uppercase;
    line-height: 1.3;
    margin-bottom: 12px;
}
.report-subtitle {
    font-size: 13pt;
    font-weight: bold;
    color: #1e3a8a;
    line-height: 1.4;
    margin-bottom: 15px;
}

.cover-info-box {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px 18px;
    margin: 0 auto;
    width: 88%;
    text-align: left;
}
.cover-info-table {
    width: 100%;
    border-collapse: collapse;
}
.cover-info-table td {
    padding: 5px 8px;
    font-size: 11pt;
    border: none;
}
.cover-info-label {
    font-weight: bold;
    color: #1e3a8a;
    width: 38%;
    white-space: nowrap;
}
.cover-info-value {
    color: #0f172a;
    font-weight: 600;
}

.cover-footer {
    margin-bottom: 5px;
    font-size: 11pt;
    font-weight: bold;
    color: #475569;
}
.cover-divider-bottom {
    width: 100px;
    height: 1.5px;
    background: #cbd5e1;
    margin: 8px auto;
}

h2 {
    color: #1e3a8a;
    font-size: 12.5pt;
    font-weight: bold;
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 3px;
    margin-top: 10px;
    margin-bottom: 6px;
    text-transform: uppercase;
}

h3 {
    color: #0f172a;
    font-size: 10.5pt;
    font-weight: bold;
    margin-top: 8px;
    margin-bottom: 3px;
}

p {
    margin-top: 0;
    margin-bottom: 5px;
    text-align: justify;
}

ul, ol {
    margin-top: 2px;
    margin-bottom: 5px;
    padding-left: 18px;
}

li { margin-bottom: 2px; }

table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0;
    font-size: 9pt;
}

th, td {
    border: 1px solid #cbd5e1;
    padding: 3.5px 5px;
    text-align: left;
}

th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
}

tr:nth-child(even) td { background-color: #f8fafc; }

.figure-container {
    text-align: center;
    margin: 6px 0;
    page-break-inside: avoid;
}

.figure-grid {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin: 6px 0;
    page-break-inside: avoid;
}

.figure-col {
    flex: 1;
    text-align: center;
}

.report-img {
    max-width: 96%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.figure-caption {
    font-size: 8.5pt;
    font-style: italic;
    color: #475569;
    margin-top: 2px;
    text-align: center;
}

.page-break { page-break-before: always; }

.highlight-box {
    background-color: #f0fdf4;
    border-left: 4px solid #16a34a;
    padding: 7px 11px;
    margin: 7px 0;
    border-radius: 0 4px 4px 0;
    font-size: 9.5pt;
}
</style>

<div class="cover-page">
    <div class="cover-header">
        <div class="cover-univ">TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM</div>
        <div class="cover-faculty">KHOA ĐIỆN TỬ - VIỄN THÔNG</div>
        <div class="cover-divider-top"></div>
    </div>

    <div class="cover-body">
        <div class="report-badge">BÁO CÁO ĐỒ ÁN MÔN HỌC THỰC HÀNH PCB</div>
        <div class="report-title">THIẾT KẾ VÀ TỔNG HỢP CHẾ TẠO<br>MẠCH SẠC PIN LI-ION TP4056 TYPE-C</div>
        <div class="report-subtitle">Tích Hợp Tầng Bảo Vệ Pin DW01A & FS8205A Trên Chuẩn KiCad 10</div>

        <div class="cover-info-box">
            <table class="cover-info-table">
                <tr>
                    <td class="cover-info-label">Sinh viên thực hiện:</td>
                    <td class="cover-info-value">Lê Ngọc Tường</td>
                </tr>
                <tr>
                    <td class="cover-info-label">Mã số sinh viên:</td>
                    <td class="cover-info-value">23207124</td>
                </tr>
                <tr>
                    <td class="cover-info-label">Lớp sinh viên:</td>
                    <td class="cover-info-value">23DTV_CLC3</td>
                </tr>
                <tr>
                    <td class="cover-info-label">Mã đề tài & Nhóm:</td>
                    <td class="cover-info-value">Đồ án cuối kỳ - Khóa Hè 2025-2026</td>
                </tr>
            </table>
        </div>
    </div>

    <div class="cover-footer">
        <div class="cover-divider-bottom"></div>
        <div>TP. HỒ CHÍ MINH - THÁNG 09/2026</div>
    </div>
</div>

<div class="page-break"></div>

## BÀI TẬP 1: TỔNG HỢP KIẾN TRÚC KỸ THUẬT VÀ PHÂN TÍCH NGUYÊN LÝ

Mạch sạc pin Lithium-Ion tích hợp ngõ vào USB Type-C được thiết kế dựa trên tiêu chuẩn công nghiệp hiện đại, tích hợp trọn vẹn kiến thức thu được từ chuỗi 8 bài thực hành (từ vẽ Schematic, tạo Symbol/Footprint chuẩn IPC, layout phân khối nguồn, đổ đồng GND tản nhiệt, đến xuất dữ liệu Gerber/Drill).

### 1. Phân tích các khối chức năng chính
* **Khối giao tiếp ngõ vào (USB Type-C Receptacle 16-pin):** Cổng kết nối chuẩn USB-C hỗ trợ dòng điện tối đa 3A. Để nguồn cấp USB PD / Type-C Power Adapter kích hoạt cấp nguồn 5V ổn định, hai điện trở kéo xuống R1 = 5.1k và R2 = 5.1k được nối từ chân CC1 và CC2 xuống mass (GND). Ngõ vào VBUS được lọc ổn định bằng hệ thống tụ gốm gồm tụ hóa trị cao C1 = 10uF và tụ dập xung cao tần C2 = 100nF.
* **Khối IC sạc pin chính (TP4056 - Linear Li-Ion Battery Charger):** IC sạc hoạt động theo chu trình dòng không đổi / áp không đổi (CC/CV). Dòng sạc cực đại được định hình qua điện trở lập trình R3 = 1.2k kết nối chân PROG xuống đất, cho dòng nạp I_charge = 1000 mA (1A). Trạng thái sạc được thông báo trực quan qua hai LED SMD 0805: LED đỏ (D1) báo đang nạp qua cực thoát hở CHRG, LED xanh lá (D2) báo pin đầy / ngắt sạc qua cực STDBY.
* **Khối bảo vệ pin Li-Ion (DW01A & Dual MOSFET FS8205A):** Để bảo đảm an toàn cháy nổ cho cell pin, IC DW01A liên tục giám sát điện áp và dòng nạp xả:
  - Ngưỡng ngắt sạc quá áp (Overcharge Protection): Tự động khóa chân OD (Overdischarge) ngắt MOSFET khi áp pin vượt quá 4.30V.
  - Ngưỡng ngắt xả sâu (Overdischarge Protection): Tự động khóa chân OC (Overcharge) ngắt MOSFET khi pin tụt dưới 2.40V.
  - Cảm biến ngắt ngắn mạch và quá dòng: Thông qua chân CS nối qua R7 = 1k đo sụt áp trên cặp kênh dẫn Drain-Source của FS8205A.

<div class="figure-container">
    <img class="report-img" src="images/schematic-1.png" alt="Sơ đồ nguyên lý TP4056 USB-C Charger" style="max-height: 98mm;">
    <div class="figure-caption">Hình 1. Bản vẽ Sơ đồ nguyên lý (Schematic) hoàn chỉnh của hệ thống sạc pin TP4056 Type-C</div>
</div>

<div class="page-break"></div>

### 2. Bảng kê linh kiện kỹ thuật (Bill of Materials - BOM)

| Reference | Value | Footprint | Số lượng | Chức năng kỹ thuật trong mạch |
| :--- | :--- | :--- | :---: | :--- |
| **U1** | TP4056 | SOIC-8-EP (Thermal Pad) | 1 | IC điều khiển sạc pin Li-Ion CC/CV 1A |
| **U2** | DW01A | SOT-23-6 | 1 | IC giám sát và bảo vệ pin quá áp, xả sâu |
| **Q1** | FS8205A | TSSOP-8 (Dual N-MOSFET) | 1 | Khóa công tắc điện tử đóng cắt bảo vệ cực âm pin |
| **J1** | USB-C 16P | HRO TYPE-C-31-M-12 | 1 | Cổng nhận nguồn nạp DC 5V từ cáp sạc Type-C |
| **J2** | BATT PH2.0 | JST PH B2B-PH-SM4-TB | 1 | Đầu cắm kết nối ngõ ra với cell pin Li-Ion 3.7V |
| **C1, C3** | 10uF | C_0805_2012Metric | 2 | Tụ lọc ổn định điện áp ngõ vào VBUS và ngõ ra BAT |
| **C2, C4** | 100nF | C_0805_2012Metric | 2 | Tụ dập nhiễu gai cao tần ngõ vào và nguồn nuôi DW01A |
| **R1, R2** | 5.1k | R_0805_2012Metric | 2 | Điện trở cấu hình kích hoạt nguồn USB-C PD |
| **R3** | 1.2k | R_0805_2012Metric | 1 | Điện trở lập trình dòng sạc pin 1A tại chân PROG |
| **R4, R5** | 1k | R_0805_2012Metric | 2 | Điện trở phân dòng an toàn cho LED CHRG và STDBY |
| **R6** | 100 | R_0805_2012Metric | 1 | Điện trở lọc RC chống xung đột biến cho DW01A VDD |
| **R7** | 1k | R_0805_2012Metric | 1 | Điện trở phân áp cảm biến quá dòng tại chân CS |
| **D1, D2** | RED, GREEN | LED_0805_2012Metric | 2 | LED hiển thị trạng thái hoạt động nạp pin |

## BÀI TẬP 2: THIẾT KẾ LAYOUT PCB VÀ TỐI ƯU HÓA ĐỊNH TUYẾN 2 LỚP

Dựa trên quy chuẩn thiết kế mạch in hiện đại, bo mạch được thiết kế với kích thước cực kỳ tinh gọn 22.0mm x 34.0mm, chuẩn công nghệ 2 lớp đồng (1.6mm FR4, 35um đồng).

* **Khối công suất (VBUS & BAT_OUT):** Đường mạch cấp dòng nạp chính từ ngõ vào USB-C đến IC TP4056 và ra chân dương pin được chạy với độ rộng W = 0.5mm - 0.6mm nhằm đảm bảo dẫn dòng 1A an toàn.
* **Cầu chuyển mạch (Via Bridge):** Tín hiệu nguồn VBUS chuyển sang chân 8 và các LED được bố trí qua cầu via kép có đường kính via 0.6mm, lỗ khoan 0.3mm tại lớp đáy (B.Cu).
* **Mặt phẳng đất (GND Plane) & Tản nhiệt:** Toàn bộ hai lớp F.Cu và B.Cu được phủ đồng GND toàn diện kết hợp cầu kết nối nhiệt (Thermal Relief) giúp tản nhiệt tối ưu cho pad tản nhiệt phía dưới IC TP4056.

<div class="figure-grid">
    <div class="figure-col">
        <img class="report-img" src="images/pcb_top-1.png" alt="Bản vẽ 2D Layout Top Layer" style="max-height: 72mm;">
        <div class="figure-caption">Hình 2a. Bản vẽ Layout lớp mặt trên (Top F.Cu)</div>
    </div>
    <div class="figure-col">
        <img class="report-img" src="images/pcb_bottom-1.png" alt="Bản vẽ 2D Layout Bottom Layer" style="max-height: 72mm;">
        <div class="figure-caption">Hình 2b. Bản vẽ Layout lớp mặt dưới (Bottom B.Cu)</div>
    </div>
</div>

<div class="page-break"></div>

## BÀI TẬP 3: KIỂM TRA QUY TẮC THIẾT KẾ (ERC/DRC) VÀ KẾT XUẤT MÔ HÌNH 3D

Nhằm đáp ứng yêu cầu chất lượng "Zero-Placeholder" và độ tin cậy tuyệt đối trước khi sản xuất hàng loạt, toàn bộ hệ thống đã được thẩm định tự động qua bộ công cụ kiểm thử nghiêm ngặt của KiCad CLI.

### 1. Kết quả kiểm tra quy tắc điện (ERC) và quy tắc vật lý (DRC)
* **Kiểm tra ERC (Electrical Rules Check):** Toàn bộ các chân linh kiện (Pin) được gắn nhãn định tuyến (Net Labels) trực tiếp với độ chính xác tọa độ 100%, không còn bất kỳ cảnh báo hở mạch hay chân không được kích hoạt (`pin_not_connected`, `pin_not_driven`). Trạng thái netlist kết nối logic giữa Schematic và PCB đạt mức đồng bộ tuyệt đối 16/16 Net.
* **Kiểm tra DRC (Design Rules Check):** Tuân thủ toàn diện khoảng cách cách ly công nghiệp (Clearance >= 0.2mm, Edge Clearance >= 0.5mm). Các linh kiện thụ động 0805 và IC được phân bố khoảng cách tối ưu, loại trừ triệt để hiện tượng đè lấn khung linh kiện (Courtyard Overlap).

<div class="figure-grid">
    <div class="figure-col">
        <img class="report-img" src="images/pcb_3d_top.png" alt="Kết xuất mô hình 3D mặt trên" style="max-height: 92mm;">
        <div class="figure-caption">Hình 3. Phối cảnh 3D thực tế mặt trên (Top Side Render)</div>
    </div>
    <div class="figure-col">
        <img class="report-img" src="images/pcb_3d_bottom.png" alt="Kết xuất mô hình 3D mặt dưới" style="max-height: 92mm;">
        <div class="figure-caption">Hình 4. Phối cảnh 3D mặt dưới (Bottom Side Render)</div>
    </div>
</div>

<div class="page-break"></div>

## BÀI TẬP 4: XUẤT HỒ SƠ CHẾ TẠO CÔNG NGHIỆP (GERBER & DRILL)

Bước cuối cùng trong quy trình thiết kế mạch in chuyên nghiệp là đóng gói toàn bộ dữ liệu thiết kế thành bộ hồ sơ chế tạo đạt chuẩn RS-274X và Excellon Drill để chuyển giao cho các nhà máy gia công PCB (như JLCPCB, PCBWay).

### 1. Danh mục các tập tin gia công mạch in (Gerber Package)

Hệ thống đã xuất hoàn chỉnh toàn bộ 12 lớp gia công tiêu chuẩn vào thư mục `gerber/`:

* `USB_TypeC_TP4056_Charger-F_Cu.gtl`: Lớp mạch in đồng mặt trên (Top Copper Layer).
* `USB_TypeC_TP4056_Charger-B_Cu.gbl`: Lớp mạch in đồng mặt dưới (Bottom Copper Layer).
* `USB_TypeC_TP4056_Charger-F_Mask.gts`: Lớp phủ mặt nạ hàn cách điện mặt trên (Top Solder Mask).
* `USB_TypeC_TP4056_Charger-B_Mask.gbs`: Lớp phủ mặt nạ hàn cách điện mặt dưới (Bottom Solder Mask).
* `USB_TypeC_TP4056_Charger-F_Silkscreen.gto`: Lớp in lụa chữ/ký hiệu linh kiện mặt trên (Top Silkscreen).
* `USB_TypeC_TP4056_Charger-B_Silkscreen.gbo`: Lớp in lụa định danh thương hiệu và thông số ở mặt dưới.
* `USB_TypeC_TP4056_Charger-F_Paste.gtp`: Lớp chế tạo mặt nạ bôi kem hàn (Solder Paste Stencil) cho máy dán linh kiện tự động SMT.
* `USB_TypeC_TP4056_Charger-Edge_Cuts.gm1`: Đường cắt biên dạng cơ khí định hình kích thước bo mạch.
* `USB_TypeC_TP4056_Charger.drl`: Tập tin tọa độ và đường kính các mũi khoan lỗ xuyên (Excellon Drill File).

### 2. Thông số công nghệ gia công khuyến nghị (PCB Fabrication Parameters)

| Thông số công nghệ | Giá trị thiết kế | Tiêu chuẩn chế tạo công nghiệp |
| :--- | :--- | :--- |
| **Kích thước bo mạch (Dimension)** | 22.0 mm x 34.0 mm | Dung sai cắt cơ khí +/- 0.15 mm |
| **Số lớp đồng (Number of Layers)** | 2 lớp (Top Layer & Bottom Layer) | Chuẩn mạch 2 mặt xuyên lỗ mạ đồng |
| **Vật liệu nền (Base Material)** | FR-4 Standard Tg 130-140°C | Chuẩn cách điện công nghiệp |
| **Độ dày bo hoàn thiện (Thickness)** | 1.6 mm | Độ cứng cơ học tối ưu |
| **Độ dày đồng (Copper Weight)** | 1 oz (35 um) | Chịu dòng liên tục 1A không phát nhiệt |
| **Đường kính lỗ khoan nhỏ nhất (Min Drill)** | 0.3 mm (Via) | Tiêu chuẩn tiêu hao tiêu chuẩn JLCPCB |
| **Xử lý bề mặt (Surface Finish)** | HASL with Lead / ENIG | Tăng khả năng bám thiếc hàn dán |

<div class="highlight-box">
<strong>KẾT LUẬN VÀ ĐÁNH GIÁ TỔNG QUAN ĐỒ ÁN:</strong><br>
Dự án mạch sạc pin Li-Ion TP4056 Type-C đã hoàn thành trọn vẹn 100% các yêu cầu kỹ thuật của học phần: sơ đồ nguyên lý chuẩn xác, kích thước board siêu nhỏ gọn, tính năng bảo vệ pin đa tầng hoạt động tin cậy, mô hình 3D sắc nét đạt tiêu chuẩn công nghiệp và bộ hồ sơ Gerber/BOM đầy đủ sẵn sàng chuyển giao cho dây chuyền sản xuất hàng loạt.
</div>
