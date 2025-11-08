# 🚀 Setup Dorothy Bot trên GitHub Actions

## 📋 Tổng Quan

Dorothy (DoSecurity) là bot moderation với các tính năng:
- ⚠️ Warning system
- 🔇 Auto-moderation
- 🤖 AI chat với Doro personality
- 📊 Logging và tracking

---

## 🔧 Bước 1: Tạo GitHub Repository

1. **Vào GitHub:** https://github.com/new
2. **Repository name:** `dorothy-bot` (hoặc tên bạn muốn)
3. **Visibility:** Private (khuyến nghị)
4. **Click:** "Create repository"

---

## 🔐 Bước 2: Thêm GitHub Secrets

Vào: `https://github.com/YOUR_USERNAME/dorothy-bot/settings/secrets/actions`

### Thêm các secrets sau:

#### 1. DOROTHY_BOT_TOKEN
- **Name:** `DOROTHY_BOT_TOKEN`
- **Secret:** Token của Dorothy bot từ Discord Developer Portal
- Click "Add secret"

#### 2. DOROTHY_OWNER_ID (Optional)
- **Name:** `DOROTHY_OWNER_ID`
- **Secret:** Discord User ID của bạn
- Click "Add secret"

#### 3. DISCORD_WEBHOOK_URL (Optional - cho notifications)
- **Name:** `DISCORD_WEBHOOK_URL`
- **Secret:** Discord webhook URL để nhận thông báo
- Click "Add secret"

---

## 📤 Bước 3: Push Code Lên GitHub

### Mở PowerShell và chạy:

```bash
cd C:/bot/Dorothy

git init
git add .
git commit -m "Initial commit: Dorothy bot with GitHub Actions"

git remote add origin https://github.com/YOUR_USERNAME/dorothy-bot.git
git branch -M main
git push -u origin main
```

**Thay `YOUR_USERNAME` bằng username GitHub của bạn!**

---

## 🎯 Bước 4: Chạy Workflow

### Tự Động:
- Workflow tự động chạy khi push code

### Thủ Công:
1. Vào: `https://github.com/YOUR_USERNAME/dorothy-bot/actions`
2. Click workflow **"Run Dorothy Bot"**
3. Click **"Run workflow"**
4. Chọn branch: **main**
5. Click **"Run workflow"**

---

## ✅ Kiểm Tra Bot

1. **Vào Actions tab** để xem logs
2. **Kiểm tra Discord** - Dorothy bot sẽ online
3. **Test commands:**
   - `-help` - Xem danh sách lệnh
   - `-ping` - Kiểm tra bot
   - Mention bot để chat với AI

---

## 🔄 Cập Nhật Code

Mỗi khi thay đổi code:

```bash
cd C:/bot/Dorothy
git add .
git commit -m "Update features"
git push
```

Workflow sẽ tự động chạy lại!

---

## 📊 So Sánh Doro vs Dorothy

| Feature | Doro | Dorothy |
|---------|------|---------|
| **Type** | Entertainment/Music | Moderation/Security |
| **FFmpeg** | ✅ Required | ❌ Not needed |
| **AI** | OpenRouter/NVIDIA | NVIDIA only |
| **Commands** | Music, Economy, Profile | Warnings, Moderation |
| **Workflow** | `Run Doro Bot` | `Run Dorothy Bot` |

---

## 🔔 Discord Notifications

Nếu đã setup `DISCORD_WEBHOOK_URL`, bạn sẽ nhận:
- 🚀 Thông báo khi workflow bắt đầu
- ✅ Thông báo khi Dorothy online
- 🎉 Thông báo khi hoàn thành
- ❌ Thông báo khi có lỗi

---

## ⚙️ Tùy Chỉnh

### Thay đổi schedule:
Edit file `.github/workflows/run-dorothy.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Chạy mỗi 6 giờ
```

### Thay đổi timeout:
```yaml
timeout-minutes: 360  # 6 hours (max)
```

---

## 🆘 Xử Lý Lỗi

### Bot không start:
- Kiểm tra `DOROTHY_BOT_TOKEN` đã đúng chưa
- Xem logs trong Actions tab

### Import error:
- Kiểm tra `requirements.txt` có đầy đủ dependencies
- Push lại code nếu thiếu

### Encoding error:
- Dorothy đã được config UTF-8 tự động
- Nếu vẫn lỗi, check logs

---

## 📝 Lưu Ý

- ⏰ GitHub Actions giới hạn 6 giờ/run
- 💰 Free tier: 2,000 minutes/tháng (private repo)
- 🔄 Workflow tự động restart mỗi 6 giờ
- 🔒 Luôn dùng Secrets cho tokens

---

**Dorothy bot giờ đã sẵn sàng chạy trên GitHub Actions!** 🎉
