# DoSecurity Discord Bot 🛡️

Bot bảo mật và quản lý chuyên nghiệp cho Discord với đầy đủ tính năng kiểm soát server.

## 🌟 Tính năng

### ⚠️ Hệ thống Cảnh báo Thông minh
- Hệ thống trừng phạt tăng dần (7 cấp độ)
- Tự động xử lý dựa trên số lần cảnh báo:
  - Cấp 1-2: Chỉ cảnh báo
  - Cấp 3: Mute 2 phút
  - Cấp 4: Mute 5 phút
  - Cấp 5: Mute 10 phút
  - Cấp 6: Kick khỏi server
  - Cấp 7: Ban vĩnh viễn
- Lưu lịch sử cảnh báo
- Xóa cảnh báo để cho cơ hội sửa đổi

### 🔨 Công cụ Kiểm duyệt
- **Timeout/Mute**: Cấm chat tạm thời với thời gian tùy chỉnh
- **Kick**: Đuổi thành viên gây rối khỏi server
- **Ban/Unban**: Cấm vĩnh viễn với khả năng gỡ ban
- **Xóa tin nhắn**: Xóa hàng loạt tin nhắn (1-100)
- **Khóa/Mở khóa kênh**: Kiểm soát kênh khẩn cấp
- **Slowmode**: Giới hạn tốc độ gửi tin

### 📊 Lệnh Thông tin
- Thống kê và thông tin server
- Hồ sơ người dùng kèm trạng thái cảnh báo
- Kiểm tra độ trễ real-time
- Tích hợp kênh mod-log

## 🚀 Bắt đầu nhanh

### Yêu cầu
- Python 3.12+
- Discord Bot Token
- Quyền Administrator trong server

### Cài đặt

1. Tải về các file bot
2. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

3. Cấu hình bot token trong file chính hoặc biến môi trường:
```python
TOKEN = 'TOKEN_CỦA_BẠN_Ở_ĐÂY'
```

4. Chạy bot:
```bash
python dosecurity.py
```

## 📝 Danh sách Lệnh

### Hệ thống Cảnh báo
- `-warn @user [lý do]` - Cảnh báo thành viên
- `-warnings [@user]` - Kiểm tra số cảnh báo
- `-clearwarns @user` - Xóa toàn bộ cảnh báo

### Lệnh Timeout
- `-timeout @user [phút] [lý do]` - Cấm chat tạm thời
- `-to @user [phút]` - Viết tắt của timeout
- `-untimeout @user` - Gỡ timeout
- `-rto @user` - Viết tắt gỡ timeout

### Lệnh Kick/Ban
- `-kick @user [lý do]` - Đuổi thành viên
- `-ban @user [lý do]` - Cấm thành viên
- `-unban <user_id> [lý do]` - Gỡ ban
- `-rban <user_id>` - Viết tắt gỡ ban

### Lệnh Tiện ích
- `-clear [số lượng]` - Xóa tin nhắn
- `-lock [#kênh]` - Khóa kênh
- `-unlock [#kênh]` - Mở khóa kênh
- `-slowmode [giây]` - Đặt chế độ chậm

### Thông tin
- `-help` - Hiển thị tất cả lệnh
- `-serverinfo` - Chi tiết server
- `-userinfo [@user]` - Thông tin người dùng
- `-ping` - Kiểm tra độ trễ

## ⚙️ Cấu hình

### Đặt ID Chủ sở hữu
Chỉnh sửa biến `OWNER_ID` trong file chính:
```python
OWNER_ID = 1344312732278591500  # ID Discord của bạn
```

### Tùy chỉnh Cấp độ Cảnh báo
Sửa dictionary `WARNING_LEVELS` để điều chỉnh hình phạt:
```python
WARNING_LEVELS = {
    1: {"action": "none", "duration": 0, "message": "Tin nhắn cảnh báo"},
    # ... thêm cấp độ
}
```

### Thiết lập Kênh Mod Log
Tạo kênh tên `mod-log` để tự động ghi lại mọi hành động kiểm duyệt.

## 🔒 Quyền Yêu cầu

Bot cần các quyền Discord sau:
- Quản lý Tin nhắn
- Quản lý Vai trò
- Kick Thành viên
- Ban Thành viên
- Timeout Thành viên
- Xem Kênh
- Gửi Tin nhắn
- Nhúng Link

## 🎯 Thực hành Tốt nhất

1. **Thiết lập kênh mod-log** để theo dõi hành động
2. **Cấu hình thứ tự role** - Role bot phải cao hơn role được quản lý
3. **Test lệnh** trong kênh riêng trước
4. **Xem xét cảnh báo định kỳ** - Cân nhắc xóa cảnh báo cũ
5. **Đào tạo staff** - Đảm bảo mod hiểu hệ thống cảnh báo

## 🐛 Xử lý Sự cố

### Bot không phản hồi lệnh
- Kiểm tra bot có message content intent
- Xác nhận prefix lệnh đúng (`-`)
- Đảm bảo bot có đủ quyền

### Không thể timeout/kick/ban
- Role bot phải cao hơn role cao nhất của thành viên
- Bot không thể quản lý chủ server hoặc admin

### Lệnh báo lỗi quyền
- Người dùng cần quyền Quản lý Tin nhắn hoặc là owner bot
- Một số lệnh chỉ owner dùng được

## 📚 Hỗ trợ

Khi gặp vấn đề:
1. Kiểm tra cú pháp lệnh với `-help`
2. Xác nhận quyền bot trong cài đặt server
3. Xem lỗi trong console
4. Kiểm tra trạng thái Discord API

## 🎨 Tùy biến

Bot được thiết kế để dễ tùy chỉnh:
- Sửa màu embed trong phản hồi lệnh
- Đổi prefix lệnh khi khởi tạo bot
- Thêm lệnh tùy chỉnh theo mẫu có sẵn
- Điều chỉnh thời gian timeout và tin nhắn cảnh báo

---

> **Ghi chú:** Tôi đã chỉnh sửa bot này để bạn có thể dễ dàng tùy chỉnh thành một bot tùy ý rồi. Nếu bạn không biết làm thì cứ đưa cho AI đi. Thất bại thì... chịu thôi! 😈

## 📄 Giấy phép

Bot được cung cấp để sử dụng cá nhân và thương mại. Thoải mái chỉnh sửa và phân phối.

---
*DoSecurity - Kiểm duyệt Discord Chuyên nghiệp*
