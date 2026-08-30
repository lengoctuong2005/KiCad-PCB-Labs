# HƯỚNG DẪN QUY CHUẨN THỰC HIỆN VÀ BIÊN SOẠN BÁO CÁO THỰC HÀNH PCB KICAD (LAB 1 - LAB 6)

Tài liệu này tổng hợp toàn bộ quy chuẩn kỹ thuật, thiết kế giao diện (CSS/HTML), nguyên tắc biên soạn nội dung, kiểm soát văn phong và kinh nghiệm thực tế để chuẩn hóa toàn diện bộ báo cáo môn **Thiết kế mạch in PCB với KiCad** (Khoa Điện tử - Viễn thông, Trường Đại học Khoa học Tự nhiên - ĐHQG TP.HCM).

---

## I. THÔNG TIN QUY CHUẨN CHUNG

* **Đơn vị:** TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM
* **Khoa:** KHOA ĐIỆN TỬ - VIỄN THÔNG
* **Học phần:** Thiết kế mạch in PCB với KiCad
* **Sinh viên thực hiện:** Lê Ngọc Tường
* **Mã số sinh viên:** 23207124
* **Lớp:** 23DTV_CLC3
* **Ca thực hành:** Ca 2 (Mã quy chuẩn nhóm/thư viện: `CA2_14`, ví dụ `LAB2_CA2_14`, `LAB3_CA2_14`)
* **Học kỳ / Năm học:** HK3 / 2025 - 2026

---

## II. CẤU TRÚC THƯ MỤC VÀ TẬP TIN CHUẨN MỖI LAB

Mỗi thư mục Lab (`Lab1` đến `Lab6`) tuân thủ cấu trúc đồng bộ, tinh gọn:

```text
LabX/
├── LAB_0X_PCB_KiCad.pdf        # File đề bài gốc từ giảng viên
├── BaoCao_Lab0X.md             # File nguồn Markdown chứa nội dung và mã HTML bìa
├── BaoCao_Lab0X.html           # File HTML trung gian sinh tự động
├── BaoCao_Lab0X_KiCad.pdf      # File PDF kết quả xuất bản chuẩn in A4
├── render_report_pdf.py        # Script Python chuyển đổi Markdown sang HTML
├── print_pdf.js                # Script Node.js (Puppeteer) in PDF chuẩn xác
├── Project_KiCad/              # Toàn bộ project KiCad (.kicad_pro, .kicad_sch, .kicad_pcb, .kicad_sym, .pretty)
└── Pic/                        # Thư mục chứa hình ảnh minh chứng kỹ thuật thật
    ├── pdf_preview/            # Ảnh preview từng trang trích xuất từ PDF để kiểm tra bố cục
    └── ...                     # Các ảnh chụp GUI KiCad và render CLI độ phân giải cao
```

---

## III. NGUYÊN TẮC BỐ CỤC VÀ HÌNH ẢNH MINH CHỨNG

### 1. Bố cục tinh gọn, đi thẳng vào bài tập (Tránh phần thừa)
* **Trang bìa (Trang 1):** Đúng chuẩn mẫu bìa (khung viền đôi trang nhã, bảng thông tin sinh viên 4 dòng có nền dịu, phân bố đều theo chiều dọc trang A4).
* **Các trang nội dung (Từ trang 2 trở đi):** Bắt đầu ngay bằng `## BÀI TẬP 1: ...`, `## BÀI TẬP 2: ...`.
* **Tuyệt đối không chèn phần thừa:** Không thêm các mục "Mục tiêu bài thực hành", "Lời mở đầu", "Giới thiệu tổng quan", hay "Kết luận / Đánh giá chung" vì các phần này làm loãng báo cáo và không đúng trọng tâm kỹ thuật.

### 2. Nguyên tắc "Zero-Placeholder" & Hình ảnh minh chứng thật (Bắt buộc)
* **100% hình ảnh phải là kết quả thao tác thực tế:** Không dùng ảnh mẫu giáo trình, không dùng ảnh vẽ đồ họa vector giả lập.
* **Minh chứng qua giao diện KiCad (GUI):**
  - Cửa sổ **Electrical Rules Checker (ERC)** hiển thị trạng thái **0 Errors** và **Title Block** mang tên sinh viên *Lê Ngọc Tường - MSSV: 23207124*.
  - Giao diện **PCB Editor** sau khi gán footprint và cập nhật mạng nối (`Update PCB from Schematic - F8`).
  - Giao diện **3D Viewer** hiển thị trực quan các linh kiện SMD/THT trên bo mạch.
* **Minh chứng qua KiCad CLI:**
  - Xuất Schematic vector độ phân giải cao có Title Block chuẩn.
  - Render mô hình 3D góc phối cảnh Isometric toàn bo mạch (`kicad-cli pcb render`).
  - Render ma trận footprint tùy chỉnh trong thư viện `.pretty`.
* **Quy chuẩn thẻ ảnh trong Markdown:**
  Mỗi hình phải được bọc trong thẻ `<div class="figure-container">` với giới hạn chiều cao `max-height` (từ `70mm` đến `105mm` tùy nội dung) để kiểm soát ngắt trang chính xác:
  ```html
  <div class="figure-container">
      <img class="report-img" src="Pic/ten_anh.png" alt="Mô tả" style="max-height: 82mm;">
      <div class="figure-caption">Hình X. Chú thích ngắn gọn, rõ ràng</div>
  </div>
  ```

---

## IV. BỘ MÃ NGUỒN VÀ BẢNG MÀU THIẾT KẾ CSS CHUẨN IN A4

### 1. Bảng màu chủ đạo (Color Palette)
* **Màu chủ đạo (Primary Blue):** `#1e3a8a` - Dùng cho khung viền bìa, tên trường khoa, tiêu đề H2, tiêu đề bảng (`<th>`).
* **Màu điểm nhấn (Accent Red):** `#b91c1c` - Dùng cho tiêu đề lớn báo cáo (`.report-title`) và thanh gạch chân badge (`.report-badge`).
* **Màu tiêu đề phụ (Secondary Slate):** `#0f172a` / `#1e293b` - Dùng cho tên bài Lab, tiêu đề H3, H4.
* **Màu nền phụ (Light Slate / Tint):** `#f8fafc` - Dùng cho khung thông tin sinh viên bìa, hàng chẵn trong bảng, khung code (`code`).
* **Màu viền & đường kẻ (Border / Divider):** `#cbd5e1` / `#e2e8f0` - Dùng cho khung ảnh, bảng biểu.
* **Font chữ:** `Times New Roman`, serif (11pt cho nội dung; 18pt cho tiêu đề chính).

### 2. Cấu hình CSS mẫu nhúng trong file Markdown

```css
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
        content: "Báo cáo Thực hành Thiết kế Mạch in PCB - Lab 0X";
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
    font-size: 11pt;
    line-height: 1.4;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
    background-color: #fff;
}

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

.page-break {
    page-break-before: always;
    break-before: page;
}

h2 {
    font-size: 12.5pt;
    color: #1e3a8a;
    border-bottom: 1.5px solid #1e3a8a;
    padding-bottom: 3px;
    margin-top: 10px;
    margin-bottom: 8px;
    text-transform: uppercase;
    page-break-after: avoid;
    break-after: avoid;
}
h3 {
    font-size: 11pt;
    color: #0f172a;
    margin-top: 8px;
    margin-bottom: 4px;
    page-break-after: avoid;
    break-after: avoid;
}
p { margin: 3px 0 6px 0; text-align: justify; }
ul, ol { margin: 3px 0 6px 0; padding-left: 20px; }
li { margin-bottom: 3px; text-align: justify; }

table.bom-table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8.5pt;
    table-layout: fixed;
}
table.bom-table th, table.bom-table td {
    border: 1px solid #334155;
    padding: 3.5px 5px;
    line-height: 1.25;
    word-wrap: break-word;
}
table.bom-table th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
}
table.bom-table tbody tr:nth-child(even) { background-color: #f8fafc; }

.figure-container {
    text-align: center;
    margin: 6px 0;
    page-break-inside: avoid;
}
.report-img {
    max-width: 92%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.figure-caption {
    font-size: 9.5pt;
    font-style: italic;
    color: #334155;
    margin-top: 4px;
}
```

---

## V. BỘ LỌC KIỂM TRA NỘI DUNG VÀ VĂN PHONG (ANTI-AI WRITING QUALITY GATE)

Trước khi xuất file PDF chính thức, **bắt buộc chạy quy trình rà soát văn bản** đối chiếu với các dấu hiệu văn phong máy theo hướng dẫn [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing):

| STT | Dấu hiệu văn phong AI cần loại bỏ | Quy tắc chuẩn hóa kỹ thuật |
| :--- | :--- | :--- |
| **1** | **Mỹ từ thổi phồng & Cụm từ sáo rỗng (Inflated Language & Clichés)**<br>*Ví dụ:* toàn diện, triệt để, chính xác tuyệt đối, minh chứng sống động, đóng vai trò then chốt, hoàn hảo. | Thay bằng câu trần thuật kỹ thuật gãy gọn, khách quan:<br>*"được kiểm tra bằng công cụ", "kết quả 0 lỗi (0 Errors)", "dựa theo datasheet".* |
| **2** | **Né tránh động từ đơn giản (Copula Avoidance & Fancy Verbs)**<br>*Ví dụ:* đóng vai trò là, mang tính chất, thể hiện một cách trực quan, biểu thị cấu trúc. | Dùng các động từ kỹ thuật trực diện:<br>*"gồm", "là", "chọn từ", "đặt cờ", "chuyển sang".* |
| **3** | **Đuôi phân từ suy diễn lê thê (*-ing* trails)**<br>*Ví dụ:* "...nhằm đảm bảo tính chính xác cao, tạo tiền đề vững chắc cho các bước sau". | Cắt bỏ vế câu thừa. Đi thẳng vào hành động và thông số: công cụ, phím tắt (`P`, `W`, `J`, `Q`, `F8`), thông số footprint. |
| **4** | **Dấu gạch ngang dài (Em dash / En dash)**<br>*Ví dụ:* sử dụng `—` hoặc `–` tràn lan giữa câu. | Thay toàn bộ bằng dấu phẩy, dấu gạch nối tiêu chuẩn `-` hoặc mở đóng ngoặc đơn `()`. |
| **5** | **Liệt kê máy móc & Tiêu đề lặp lại (Mechanical Boldface / Rule of Three)**<br>*Ví dụ:* Cố ép 3 ý đối xứng hoặc lặp lại cấu trúc máy móc. | Trình bày tự nhiên theo dạng bảng dữ liệu BOM đối chiếu hoặc danh sách các bước thao tác kỹ thuật cụ thể. |
| **6** | **Rối chữ do chèn path thư viện quá dài trong ngoặc**<br>*Ví dụ:* `Jumper_3 (từ thư viện Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical)`. | Trình bày rõ ràng trong bảng hoặc ghi ngắn gọn: `Header 1x03 P2.54mm (KiCad Standard)`. |

---

## VI. QUY TRÌNH BIÊN DỊCH VÀ KIỂM ĐỊNH TRANG IN (PIPELINE TỰ ĐỘNG)

Mỗi lần chỉnh sửa nội dung, thực thi chuỗi lệnh sau để sinh PDF và kiểm tra trực quan số trang:

```bash
# 1. Chuyển đổi Markdown sang HTML
python3 render_report_pdf.py BaoCao_Lab0X.md

# 2. In file PDF qua Puppeteer (Chính xác 100% CSS Paged Media)
node print_pdf.js

# 3. Trích xuất ảnh preview từng trang để kiểm tra ngắt trang (Trang 1 đến trang N)
rm -rf Pic/pdf_preview/*
pdftoppm -png -r 150 BaoCao_Lab0X_KiCad.pdf Pic/pdf_preview/page

# 4. Kiểm tra danh sách trang sinh ra (Đảm bảo số trang đúng theo barem yêu cầu, không tràn thêm trang trắng thừa)
ls -la Pic/pdf_preview/
```

---

## VII. BẢNG TIÊU CHUẨN TRIỂN KHAI TỪNG LAB (LAB 1 - LAB 6)

| Lab | Tên bài thực hành | Trọng tâm kỹ thuật | Hình ảnh minh chứng bắt buộc |
| :--- | :--- | :--- | :--- |
| **Lab 01** | Làm quen KiCad & Mạch nguồn | Cài đặt KiCad, phân tích nguyên lý nguồn đa năng, làm quen giao diện | Sơ đồ khối nguyên lý, bảng linh kiện BOM phân loại |
| **Lab 02** | Schematic & Symbol Library | Tạo Symbol LM2776, Jumper 3 chân, vẽ hoàn chỉnh sơ đồ, chạy ERC 0 lỗi | Sơ đồ hoàn chỉnh có Title Block, Symbol LM2776 & Jumper_3, ảnh ERC GUI 0 lỗi |
| **Lab 03** | Schematic phức hợp & Gán Footprint | Hoàn thiện sơ đồ nguồn, gán footprint SMD/THT chính xác, xuất 3D | Sơ đồ nguyên lý, bảng BOM đối chiếu Footprint, ảnh ERC GUI, ảnh PCB Editor sau gán chân, ảnh 3D Viewer & 3D Isometric |
| **Lab 04** | Thiết lập PCB & Design Rules | Vẽ viền bo Edge.Cuts $50\times 50\text{ mm}$, cấu hình Stackup 2 lớp FR4, Net Classes | Cấu hình Stackup, bảng Design Rules, bảng Net Classes |
| **Lab 05** | Bố trí linh kiện (Placement) | Sắp xếp linh kiện tối ưu, tụ lọc sát chân IC, phân chia khối nguồn | Bản vẽ PCB 2D sau placement, ảnh 3D linh kiện đã sắp xếp |
| **Lab 06** | Đi dây (Routing), Phủ đồng & Xuất Gerber | Routing lớp Top/Bottom, đổ đồng GND, chạy DRC 0 lỗi, xuất Gerber/BOM | Bản vẽ Routing hoàn chỉnh, bản vẽ phủ đồng, báo cáo DRC 0 lỗi |

---

## VIII. KINH NGHIỆM VÀ QUY CHUẨN KỸ THUẬT NÂNG CAO (ĐÃ ĐƯỢC THỰC NGHIỆM)

### 1. Quy chuẩn căn chỉnh mô hình 3D (3D Model Alignment & Offsets)
* **Quy tắc đảo dấu trục Y giữa PCB và 3D STEP:**
  - Hệ toạ độ mặt phẳng 2D trong KiCad PCB quy định trục $+Y$ hướng xuống dưới (downward).
  - Hệ toạ độ không gian 3D OpenGL / STEP quy định trục $+Y$ hướng lên trên (upward).
  - Khi gán offset 3D `(offset (xyz ox oy oz))` trong tệp `.kicad_pcb`: toạ độ $Y_{\text{3D\_offset}} = - Y_{\text{PCB\_offset}}$.
* **Kiểm tra khớp chân linh kiện (Pads vs 3D Pins):**
  - **Headers 2x3 (J5, J6, J7, J8):** Đảm bảo dùng đúng tệp `PinHeader_2x03_P2.54mm_Vertical.step` (không dùng nhầm 1x03), kiểm tra vị trí chân số 1 và góc xoay footprint để 6 chân cắm lọt 100% vào 6 lỗ pad.
  - **IC QFN-28 (CP2102 - U3):** Đảm bảo dấu chấm Pin 1 trên thân IC trùng với ký hiệu Pin 1 trên lớp Silkscreen và pad đồng góc dưới bên trái; cân chỉnh offset và xoay góc `(xyz 0 0 90)`.
  - **Cổng Micro USB (USB1) & Công tắc trượt (SW2):** Cân chỉnh chính xác vị trí các pad gá vỏ kim loại chịu lực và các chân tín hiệu tiếp xúc.
* **Lệnh render 3D kiểm tra qua CLI:**
  ```bash
  # Render nhìn thẳng từ trên xuống (Top View)
  kicad-cli pcb render --side top --quality high -o Pic/3d_placement_top.png Project_KiCad/LAB5.kicad_pcb

  # Render góc phối cảnh 3D Isometric chuẩn
  kicad-cli pcb render --rotate '-45,0,45' --perspective --quality high -o Pic/3d_placement_isometric.png Project_KiCad/LAB5.kicad_pcb
  ```

### 2. Quy chuẩn tạo ảnh đồ họa chú thích bo mạch (PCB Image Annotations)
* **Tỉ lệ ánh xạ tọa độ vật lý sang pixel:**
  - Với bo mạch $50 \times 50\text{ mm}$ xuất ảnh kích thước $1927 \times 1927\text{ px}$, hệ số chuyển đổi là $\approx 38.54\text{ px/mm}$.
* **Quy tắc đóng khung bao (Bounding Boxes):**
  - Khung bao khối chức năng hoặc linh kiện bắt buộc phải bao trọn: toàn bộ diện tích thân linh kiện (Body), toàn bộ các chân pad hàn (Pads), và nhãn định danh (Silkscreen Reference).
  - Tuyệt đối không để khung chỉ bao quanh phần chữ định danh mà bỏ sót cụm pad mạch in.

### 3. Quy chuẩn an toàn trước khi Commit và Push GitHub
* **Dọn dẹp tệp tin rác:** Xóa toàn bộ ảnh cắt tạm thời (`crop_*.png`, `test_3d_render_*.png`), thư mục preview trung gian (`Pic/pdf_preview/`), và cache `__pycache__`.
* **Quét bảo mật bí mật (Secret Scan):** Chạy kiểm tra qua công cụ `safety_guard.py` để đảm bảo không rò rỉ token, khóa riêng tư hoặc thông tin cá nhân ngoài quy chuẩn.
* **Đồng bộ định danh tác giả Git:** Đảm bảo `git config user.name` và `git config user.email` thể hiện đúng tên sinh viên *Lê Ngọc Tường*.

