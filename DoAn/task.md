# Kế hoạch & Tiến độ Triển khai Đồ án Phần cứng DoAn

## 1. Đồ án AFE ECG PPG PTT - Quản lý Danh mục Linh kiện & Mua sắm (BOM & Sourcing)
- [x] Rà soát và đối chiếu toàn diện linh kiện từ sơ đồ nguyên lý `AFE_ECG_PPG_PTT.kicad_sch`, `outputs/print_preflight_20261114/BOM.csv` và `BOM_Orderable_LCSC.csv`:
  - [x] 3 Vi mạch tích hợp & ổn áp nguồn: AD8232 (LFCSP-20), ADS1115 (VSSOP-10), MCP1700-2802E (SOT-23)
  - [x] 2 Module cắm ngoài: ESP32-DevKitC V4 38 chân, Module quang MAX30102
  - [x] 6 Đầu nối jack & cơ khí: Jack audio 3.5mm SJ1-3533N, Cáp điện tim ECG 3 nút, Miếng dán điện cực Ag/AgCl, Header cái 1x20P (cắt 1x19P), Header đực 1x7P, Trụ đồng M3 + Vít
  - [x] 6 Trị số tụ điện gốm ceramic SMD 0603 (11 vị trí): 0.33uF (C1, C2), 1nF (C3), 0.1uF (C4, C8, C11), 1.5nF (C5), 10nF (C6, C7), 1uF 50V (C9, C10)
  - [x] 8 Trị số điện trở dán SMD 0603 1% (18 vị trí): 360k (R1..R3), 10M (R4..R6, R8..R10), 1M (R11, R12, R14), 100k (R13), 1k (R15), 4.7k (R16, R17), 1.4M (R18), 10k (R19)
- [x] Tra cứu Google / khảo sát nguồn hàng thực tế và cập nhật báo giá trực tiếp tại thị trường Việt Nam:
  - [x] Kênh Thế Giới IC (thegioiic.com): IC ADS1115IDGSR, LDO MCP1700, dải trở/tụ SMD 0603, jack 3.5mm, cáp ECG
  - [x] Kênh Hshop.vn: ESP32-DevKitC V4 38 chân, Module cảm biến MAX30102, Header cái 1x20, Trụ đồng M3
  - [x] Kênh Shopee Việt Nam: Chip dán AD8232ACPZ, tép trở tụ 0603, miếng dán điện cực tim ECG Ag/AgCl bịch 50 cái
  - [x] Kênh nhà máy LCSC (lcsc.com): Đầy đủ mã đặt hàng C-part chính xác 100%
- [x] Xây dựng file HTML và biên dịch tài liệu PDF chuẩn in ấn A4 (3 trang chuyên nghiệp):
  - [x] Trang 1: Tổng quan quy mô, dự toán kinh phí, Bảng linh kiện IC chính (AD8232, ADS1115, MCP1700) và Module vi điều khiển (ESP32, MAX30102)
  - [x] Trang 2: Bảng đầu nối jack & phụ kiện cơ khí (Jack 3.5mm, cáp, điện cực, header, trụ M3) và Bảng tụ điện SMD 0603 (C1..C11)
  - [x] Trang 3: Bảng điện trở dán SMD 0603 (R1..R19), Danh bạ các cửa hàng uy tín tại Việt Nam, Chiến lược gom đơn 2 giỏ hàng tiết kiệm, Cẩm nang kỹ thuật hàn khò QFN LFCSP-20, quy trình rửa sạch flux bằng cồn IPA 99% chống rò nút 10M và cảnh báo an toàn điện y sinh
- [x] Xuất bản tài liệu thành công:
  - [x] `DoAn/DANH_SACH_LINH_KIEN_AFE_ECG_PPG_PTT.pdf` (366 KB, đúng 3 trang cân đối)
  - [x] `DoAn/AFE_ECG_PPG_PTT/DANH_SACH_LINH_KIEN_MUA_AFE_ECG_PPG_PTT.pdf`
  - [x] `DoAn/DANH_SACH_LINH_KIEN_AFE_ECG_PPG_PTT.html` (Mở trực tiếp trên trình duyệt để click link nhanh)

## 2. Các đồ án phần cứng hoàn tất trước đó
- [x] Đồ án Sạc USB Type-C TP4056 (`DoAn/USB_TypeC_TP4056_Charger`): Khắc phục triệt để 83 lỗi DRC, DFM và xuất trọn bộ Gerber sản xuất
- [x] Đồ án Cảm biến Điện cơ EMG (`DoAn/EMG_Sensor`): Tối ưu vát góc 45 độ, thermal relief 0.25mm / 0.40mm
- [x] Đồ án Hệ thống ECG + PPG (`DoAn/ECG_PPG_System`): Cập nhật R hạn dòng LED quang 120R và chuẩn hóa thuật toán PTT
- [x] Tài liệu kiểm toán công nghiệp: `KIEM_TOAN_VA_CHUAN_HOA_DOANH_NGHIEP_PCB.md`, `TONG_KET_KINH_NGHIEM_THIET_KE_PCB.md`

## 3. Xuất file PDF in ủi mạch thủ công (Toner Transfer 1:1)
- [x] Xuất mặt trên `F.Cu` lật gương, đen trắng 1:1: `AFE_ECG_PPG_PTT/outputs/toner_transfer_1to1/F_Cu_Top_MIRRORED_1to1.pdf`
- [x] Xuất mặt dưới `B.Cu` thuận chiều, đen trắng 1:1: `AFE_ECG_PPG_PTT/outputs/toner_transfer_1to1/B_Cu_Bottom_UNMIRRORED_1to1.pdf`
- [x] Xuất lớp chữ `F.Silkscreen` lật gương 1:1: `AFE_ECG_PPG_PTT/outputs/toner_transfer_1to1/F_Silkscreen_Top_MIRRORED_1to1.pdf`
- [x] Kiểm tra trực quan bằng `pdftoppm` xác nhận đúng chiều lật gương, phủ đồng GND, vùng cấm anten và lỗ định tâm khoan
