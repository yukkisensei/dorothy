# Dorothy Discord Bot 🛡️

Bot bảo mật và kiểm duyệt chuyên nghiệp cho Discord với tính năng AI và hệ thống bảo vệ toàn diện.

## 🌟 Tính năng

### 🤖 Trợ lý AI Dorothy
- Chat với Dorothy sử dụng phân tích cảm xúc AI
- Phản hồi tự nhiên "doro doro" với nhiều cảm xúc
- Phản ứng thông minh dựa trên ngữ cảnh tin nhắn
- Được hỗ trợ bởi NVIDIA API với fallback thông minh

### 🛡️ Hệ thống Bảo mật Nâng cao

#### Chống Phá Server (Anti-Nuke)
- Phát hiện và ngăn chặn các nỗ lực phá hoại server
- Giám sát ban, kick, xóa kênh và xóa role hàng loạt
- Tự động loại bỏ quyền của kẻ tấn công
- Cảnh báo real-time đến chủ server
- Ngưỡng phát hiện có thể điều chỉnh

#### Chống Raid (Anti-Raid)
- Phát hiện mẫu tham gia đáng ngờ
- Giám sát tuổi tài khoản và tần suất tham gia
- Tự động kick những kẻ raid tiềm năng
- Cửa sổ và ngưỡng phát hiện có thể điều chỉnh
- Hệ thống whitelist cho người dùng tin cậy

#### Chống Spam (Anti-Spam)
- Giám sát tần suất tin nhắn
- Phát hiện tin nhắn trùng lặp
- Ngăn chặn spam mention
- Cảnh báo và trừng phạt tự động
- Theo dõi thông minh từng người dùng
- Whitelist kênh cho vùng miễn nhiễm

#### Tự động Kiểm duyệt (Auto-Mod)
- Lọc từ ngữ cấm
- Chặn link invite Discord
- Phát hiện viết hoa quá mức
- Danh sách đen tùy chỉnh theo server
- Hành động tự động dựa trên mức độ nghiêm trọng

### ⚠️ Hệ thống Cảnh báo Nâng cao
- Hệ thống trừng phạt tăng dần (10 cấp độ)
- Tự động xử lý dựa trên số lần cảnh báo:
  - Cấp 1-3: Chỉ cảnh báo
  - Cấp 4: Mute 5 phút
  - Cấp 5: Mute 30 phút
  - Cấp 6: Mute 1 giờ
  - Cấp 7: Mute 3 giờ
  - Cấp 8: Kick khỏi server
  - Cấp 9-10: Ban vĩnh viễn
- Lưu lịch sử cảnh báo kèm lý do
- Xóa cảnh báo để cho cơ hội sửa đổi
- Thông báo DM cho người dùng

### 🔨 Công cụ Kiểm duyệt
- **Timeout/Mute**: Cấm chat tạm thời với thời gian tùy chỉnh (hỗ trợ định dạng 1h, 30m, 1h30m)
- **Kick**: Đuổi thành viên gây rối khỏi server
- **Ban/Unban**: Cấm vĩnh viễn với khả năng gỡ ban
- **Xóa tin nhắn**: Xóa hàng loạt tin nhắn (1-100)
- **Khóa/Mở khóa kênh**: Kiểm soát kênh khẩn cấp
- **Slowmode**: Giới hạn tốc độ gửi tin
- **Lệnh Say**: Bot nói thay với tính năng reply tin nhắn

### 📊 Lệnh Thông tin
- Thống kê server toàn diện
- Hồ sơ người dùng chi tiết kèm trạng thái cảnh báo
- Kiểm tra độ trễ real-time
- Prefix tùy chỉnh theo server
- Tích hợp kênh mod-log và security-log

### 🌐 Hỗ trợ Đa ngôn ngữ
- Hỗ trợ đầy đủ tiếng Anh và tiếng Việt
- Tùy chọn ngôn ngữ theo từng server
- Slash command `/setlanguage` để dễ dàng chuyển đổi
- Chỉ admin mới được đổi ngôn ngữ
- Tất cả lệnh, tin nhắn và embed đều thích ứng theo ngôn ngữ đã chọn

## 🚀 Bắt đầu nhanh

### Yêu cầu
- Python 3.12.x (đã test trên 3.12.10)
- Discord Bot Token
- Quyền Administrator trong server
- (Tùy chọn) NVIDIA API Key cho tính năng AI

### Cài đặt

1. Tải về các file bot
2. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

3. Tạo file `.env` với cấu hình:
```env
DISCORD_BOT_TOKEN=token_bot_của_bạn
OWNER_ID=discord_id_của_bạn
NVIDIA_API_KEY=nvidia_api_key  # Tùy chọn
```

4. Chạy bot:
```bash
python main.py
```

### Cấu trúc File
```
dorothy/
├── main.py              # File khởi động chính
├── config.py            # Cấu hình và hằng số
├── database.py          # Quản lý dữ liệu và lưu trữ
├── localization.py      # Hệ thống hỗ trợ đa ngôn ngữ
├── security.py          # Tính năng bảo mật (anti-nuke, anti-raid, v.v.)
├── moderation.py        # Lệnh kiểm duyệt
├── info_commands.py     # Lệnh thông tin và tiện ích
├── security_commands.py # Lệnh quản lý bảo mật
├── doro_ai.py          # Phân tích cảm xúc AI
├── events.py           # Xử lý sự kiện Discord
└── utils.py            # Hàm trợ giúp
```

## 📝 Danh sách Lệnh

### 🤖 Lệnh AI
- `@Dorothy [tin nhắn]` - Chat với Dorothy AI (phản hồi "doro doro!")

### 🛡️ Lệnh Bảo mật
- `-security` - Xem trạng thái bảo mật và nhật ký gần đây
- `-antinuke [on/off]` - Bật/tắt chống phá server
- `-antiraid [on/off]` - Bật/tắt chống raid
- `-antispam [on/off]` - Bật/tắt chống spam
- `-automod [on/off]` - Bật/tắt tự động kiểm duyệt
- `-whitelist @user [add/remove]` - Quản lý whitelist người dùng
- `-whitelistchannel [#channel] [add/remove]` - Quản lý whitelist kênh (vùng miễn nhiễm)
- `-blacklist [add/remove] <từ>` - Quản lý danh sách từ cấm

### ⚠️ Hệ thống Cảnh báo
- `-warn @user [lý do]` - Cảnh báo thành viên
- `-warnings [@user]` - Kiểm tra số cảnh báo
- `-clearwarns @user` - Xóa toàn bộ cảnh báo

### 🔇 Lệnh Timeout
- `-timeout @user [time] [lý do]` - Cấm chat (vd: 5m, 1h, 2h30m)
- `-to @user [time]` - Viết tắt
- `-untimeout @user` - Gỡ timeout
- `-rto @user` - Viết tắt gỡ timeout

### 🔨 Lệnh Kick/Ban
- `-kick @user [lý do]` - Đuổi thành viên
- `-ban @user [lý do]` - Cấm thành viên
- `-unban <user_id> [lý do]` - Gỡ ban
- `-rban <user_id>` - Viết tắt gỡ ban

### 🛠️ Lệnh Tiện ích
- `-clear [số]` - Xóa tin nhắn (1-100)
- `-lock [#kênh]` - Khóa kênh
- `-unlock [#kênh]` - Mở khóa kênh
- `-slowmode [giây]` - Đặt slowmode (0-21600)
- `-say <nội dung>` - Bot nói thay
- `-say -r <msg_id> <nội dung>` - Bot reply tin nhắn

### 📊 Thông tin
- `-help` - Hiển thị tất cả lệnh
- `-serverinfo` - Chi tiết server
- `-userinfo [@user]` - Thông tin user kèm cảnh báo
- `-ping` - Kiểm tra độ trễ
- `-setprefix <prefix>` - Đặt prefix tùy chỉnh cho server

### 🌐 Ngôn ngữ (Slash Commands)
- `/setlanguage` - Đổi ngôn ngữ bot (Chỉ Admin)
  - 🇬🇧 English
  - 🇻🇳 Tiếng Việt

## ⚙️ Cấu hình

### Biến môi trường
Tạo file `.env` trong thư mục gốc:
```env
DISCORD_BOT_TOKEN=token_của_bạn
OWNER_ID=discord_id_của_bạn
BOT_OWNER_IDS=id1,id2,id3  # Nhiều owner (tùy chọn)
NVIDIA_API_KEY=nvidia_key  # Tùy chọn cho AI
```

### Cài đặt Bảo mật
Tất cả tính năng bảo mật được bật mặc định và có thể bật/tắt theo server:
- Anti-Nuke: Ngăn chặn ban/kick/xóa hàng loạt
- Anti-Raid: Chặn mẫu tham gia đáng ngờ
- Anti-Spam: Giám sát tần suất và trùng lặp tin nhắn
- Auto-Mod: Lọc từ cấm và link

### Tùy chỉnh Ngưỡng Bảo mật
Sửa `config.py` để điều chỉnh ngưỡng phát hiện:
```python
RAID_DETECTION_THRESHOLD = 5  # Số lần join trong cửa sổ thời gian
SPAM_MESSAGE_THRESHOLD = 10   # Tin nhắn trong cửa sổ thời gian
NUKE_BAN_THRESHOLD = 3        # Số ban được phát hiện
```

### Tùy chỉnh Cấp độ Cảnh báo
Sửa `WARNING_LEVELS` trong `config.py`:
```python
WARNING_LEVELS = {
    1: {"action": "none", "duration": 0, "message": "Tin nhắn cảnh báo"},
    # ... tổng 10 cấp độ
}
```

### Kênh Log
Tạo các kênh này để tự động ghi log:
- `mod-log` - Hành động kiểm duyệt (warn, kick, ban)
- `security-log` - Sự kiện bảo mật (raid, spam, nuke)

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

1. **Thiết lập kênh log** - Tạo kênh `mod-log` và `security-log`
2. **Cấu hình thứ tự role** - Role bot phải cao hơn tất cả role được quản lý
3. **Whitelist staff tin cậy** - Thêm mod vào whitelist để tránh false positive
4. **Test tính năng bảo mật** - Test trong server riêng trước khi dùng thực tế
5. **Xem log bảo mật** - Thường xuyên kiểm tra lệnh `-security` để xem cảnh báo
6. **Cấu hình ngưỡng** - Điều chỉnh ngưỡng phát hiện dựa trên kích thước server
7. **Đào tạo staff** - Đảm bảo mod hiểu tất cả hệ thống bảo mật
8. **Bảo trì thường xuyên** - Xóa cảnh báo cũ và xem lại blacklist định kỳ

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

## 🔧 Tính năng Nâng cao

### Kiến trúc Modular
Dorothy sử dụng thiết kế modular để dễ bảo trì và tùy chỉnh:
- **config.py** - Tất cả hằng số cấu hình
- **database.py** - Lưu trữ dữ liệu dựa trên JSON
- **security.py** - Thuật toán bảo mật cốt lõi
- **moderation.py** - Logic lệnh kiểm duyệt
- **doro_ai.py** - Phân tích cảm xúc AI
- **events.py** - Giám sát sự kiện Discord

### Ghi Log Bảo mật
Tất cả sự kiện bảo mật được ghi với timestamp và chi tiết:
- Phát hiện raid kèm tuổi tài khoản
- Mẫu spam và theo dõi người dùng
- Nỗ lực nuke với số lượng hành động
- Kích hoạt auto-mod với mức độ nghiêm trọng

### Lưu trữ Dữ liệu
Tất cả dữ liệu được lưu trong `dorothy_data.json`:
- Lịch sử cảnh báo theo người dùng
- Cài đặt bảo mật theo server
- Prefix tùy chỉnh
- Người dùng trong whitelist
- Từ trong blacklist
- Log sự kiện bảo mật

---

> **Ghi chú:** Dorothy được xây dựng với kiến trúc modular để dễ dàng tùy chỉnh. Nếu bạn cần giúp đỡ chỉnh sửa tính năng, trợ lý AI có thể giúp bạn điều hướng codebase một cách hiệu quả!

## 📄 Giấy phép

Bot được cung cấp để sử dụng cá nhân và thương mại. Thoải mái chỉnh sửa và phân phối.

---
*Dorothy - Bot Bảo mật & Kiểm duyệt Discord Nâng cao v3.1*
