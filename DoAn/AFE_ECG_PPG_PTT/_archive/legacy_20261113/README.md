# Dữ liệu lịch sử, không dùng chế tạo

Các netlist, PCB thử, report và export cũ được chuyển vào đây để không nhầm với nguồn gốc project. Không xóa nội dung. `INDEX.json` ghi đường cũ, đường hiện tại và SHA-256 từng file trước khi chuyển; tất cả hash đã đối chiếu sau di chuyển.

Khôi phục từng mục theo mapping `to` → `from` sau khi xác nhận đường đích không có file cần giữ. Không dùng report cũ để kết luận trạng thái CAD hiện hành.

Các manifest lịch sử khác có thể còn chứa đường tương đối trước di chuyển; dùng INDEX để truy xuất đúng byte, không sửa hash lịch sử để nhận chúng là revision mới.
