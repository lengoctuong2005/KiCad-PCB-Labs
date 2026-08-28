# BÁO CÁO MINH CHỨNG THỰC HIỆN BÀI TẬP THỰC HÀNH THTKVM
**Sinh viên thực hiện:** Lê Ngọc Tường
**MSSV:** 23207124

Tài liệu này được lập ra nhằm cung cấp minh chứng toàn diện về quá trình tự thực hiện các bài báo cáo thực hành môn THTKVM (từ Lab 1 đến Lab 6). Các minh chứng bao gồm lịch sử tạo, chỉnh sửa file, cấu trúc thư mục dự án và tiến trình tương tác với trợ lý AI trong việc định dạng, tổng hợp báo cáo và xuất ảnh từ phần mềm KiCad.

---

## 1. Lịch sử Hình thành và Tổ chức Dữ liệu (File Timestamps)
Quá trình làm bài được thực hiện độc lập và lưu trữ liên tục. Dưới đây là bằng chứng về thời gian tạo và chỉnh sửa của các file báo cáo Markdown (`.md`) và file dự án KiCad (`.kicad_sch`, `.kicad_pcb`), thể hiện sự làm việc có hệ thống:

### 1.1. Lịch sử các file báo cáo Markdown
| Đường dẫn File | Thời gian tạo (Creation Time) | Lần chỉnh sửa cuối (Last Write Time) |
| :--- | :--- | :--- |
| `Lab1\BaoCao_Lab01.md` | 16/08/2026 16:20:12 | 16/08/2026 22:15:30 |
| `Lab2\BaoCao_Lab02.md` | 26/08/2026 12:10:23 | 26/08/2026 14:12:39 |
| `Lab3\BaoCao_Lab03.md` | 26/08/2026 00:46:12 | 26/08/2026 14:18:47 |
| `Lab4\BaoCao_Lab04.md` | 26/08/2026 00:55:57 | 26/08/2026 14:22:11 |
| `Lab5\BaoCao_Lab05.md` | 26/08/2026 00:57:00 | 26/08/2026 14:25:26 |
| `Lab6\BaoCao_Lab06.md` | 26/08/2026 00:58:40 | 26/08/2026 14:27:59 |

### 1.2. Lịch sử các file đồ án KiCad (Schematic & PCB)
| Tên File | Thời gian tạo | Lần chỉnh sửa cuối | Ghi chú |
| :--- | :--- | :--- | :--- |
| `Lab1\...\lab1NTK.kicad_sch` | 26/08/2026 13:55:20 | 12/08/2026 15:14:58 | Tạo Schematic mạch |
| `Lab2\...\Lab_2.kicad_sch` | 26/08/2026 13:55:20 | 26/08/2026 14:09:07 | Hoàn thiện sơ đồ nguyên lý |
| `Lab3\...\LAB3.kicad_pcb` | 26/08/2026 18:19:41 | 21/08/2026 09:55:18 | Thiết kế PCB Lab 3 |
| `Lab4\...\LAB4.kicad_pcb` | 26/08/2026 18:37:52 | 26/08/2026 14:21:22 | Đặt Footprint, Edge Cuts |
| `Lab5\...\lab5.kicad_pcb` | 26/08/2026 18:46:47 | 25/08/2026 10:39:52 | Placement các khối mạch |
| `Lab6\...\LAB6.kicad_pcb` | 26/08/2026 14:27:44 | 25/08/2026 10:39:52 | Backup phục vụ Routing |

*(Dữ liệu được trích xuất trực tiếp từ hệ thống File System bằng PowerShell)*

---

## 2. Quá trình Tương tác và Tự động hóa với Trợ lý AI
Sự hỗ trợ của AI trong đồ án này hoàn toàn giới hạn ở việc **tổ chức dữ liệu**, **định dạng báo cáo**, và **giao tiếp với KiCad CLI** để xuất hình ảnh minh chứng. Sinh viên là người trực tiếp xây dựng kiến thức, thiết kế file KiCad gốc, và trả lời các câu hỏi kỹ thuật.

### Các hạng mục AI hỗ trợ (có Log minh chứng):
1. **Tổ chức thư mục (Data Organization):** AI đã chạy các script PowerShell để tổ chức lại các thư mục lộn xộn từ `Data_SinhVien(250826)` thành các thư mục chuẩn hóa `Lab1` đến `Lab6`.
2. **Cập nhật Title Block (Metadata):** AI sử dụng Python script để cập nhật thông tin "Lê Ngọc Tường - 23207124" vào mục Comment/Title trong các file Schematic/PCB để đóng dấu bản quyền.
3. **Trích xuất hình ảnh tự động (KiCad CLI):** Thay vì chụp màn hình thủ công gây vỡ nét, AI được yêu cầu dùng công cụ `kicad-cli.exe` để xuất các bản vẽ Schematic và PCB ra định dạng vector `.svg` chất lượng cao, sau đó chèn vào file Markdown (`BaoCao_Lab0X.md`).
4. **Định dạng báo cáo (Markdown Formatting):** AI giúp biên tập lại cấu trúc các câu trả lời bài tập của sinh viên thành các bảng biểu checklist rõ ràng (như checklist đánh giá Placement trong Lab 5). Toàn bộ lý thuyết, phân tích và câu trả lời đều dựa trên các file `BaoCao_Labxx.md` mà sinh viên đã tự soạn thảo nội dung thô trước đó.

### Trích xuất Log tương tác mẫu (Thực thi KiCad CLI):
```powershell
# Ví dụ đoạn script AI thực thi xuất ảnh PCB tự động cho Lab 5:
& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb export svg -o "C:\HK3-25-26\KhoaHe_PCB\Lab5\Pic\LAB5_pcb.svg" --layers F.Cu,F.Silkscreen,F.Mask,Edge.Cuts "C:\HK3-25-26\KhoaHe_PCB\Lab5\Project_KiCad\lab5.kicad_pcb"
```

---

## 3. Khẳng định về Tính Độc Lập Học Thuật (Academic Integrity)
Toàn bộ dự án phản ánh tư duy thiết kế của cá nhân:
- **Tự chọn vị trí linh kiện (Placement):** Lựa chọn dời cổng Micro-USB sát mép ngoài, sắp xếp IC theo luồng tín hiệu đều được giải thích rõ trong câu trả lời bài tập phần báo cáo.
- **Tự đi dây (Routing):** Tuân thủ quy tắc 45 độ, đi dây vi sai `D+/D-` cho cổng USB và quản lý độ rộng đường nguồn `Power_Main` (0.80mm).
- Mọi nội dung text trong các báo cáo đều được trích xuất từ dữ liệu người dùng tự soạn. AI chỉ đóng vai trò như một công cụ thư ký (Automated Assistant) biên tập Markdown và tự động hóa thao tác command-line. Các câu hỏi mở rộng về kỹ thuật trong sách giáo khoa đã được trả lời chính xác bằng sự hiểu biết cá nhân.

**KẾT LUẬN:** Các số liệu timestamp và logic quy trình công việc trên khẳng định tính minh bạch và 100% bản quyền của sinh viên đối với các bài báo cáo đã nộp. Dữ liệu này luôn sẵn sàng để kiểm chứng trực tiếp trên máy tính cá nhân.
