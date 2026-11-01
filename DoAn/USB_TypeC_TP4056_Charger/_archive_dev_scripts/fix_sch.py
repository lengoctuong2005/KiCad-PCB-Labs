import sys, uuid

def get_uuid(): return str(uuid.uuid4())

# Ta xây dựng lại sơ đồ nguyên lý với:
# 1. Các chân symbol định nghĩa trực quan chuẩn KiCad:
#    - Tọa độ chân, hướng (0: sang phải, 90: lên trên, 180: sang trái, 270: xuống dưới)
# 2. Không xoay linh kiện 270 gây đảo dấu âm dương tọa độ pin
# 3. Sử dụng Net Labels rõ ràng, sạch sẽ, chuẩn xác cho từng chân kết nối
