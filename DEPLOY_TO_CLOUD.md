# 部署到 Render.com 指南

## 📦 準備工作

### 1. 建立 GitHub Repository

1. 前往 https://github.com/new
2. 建立新的 repository（例如：`agriculture-line-bot`）
3. **不要**勾選 "Add a README file"

### 2. 推送程式碼到 GitHub

在 PowerShell 執行：

```powershell
cd C:\line_ai

# 初始化 Git（如果尚未初始化）
git init

# 加入所有檔案
git add .

# 提交
git commit -m "Initial commit: Agriculture LINE Bot"

# 連接到你的 GitHub repository
git remote add origin https://github.com/[你的用戶名]/[repository名稱].git

# 推送
git branch -M main
git push -u origin main
```

---

## 🚀 部署到 Render

### 1. 註冊 Render

前往 https://render.com 註冊帳號（建議用 GitHub 登入）

### 2. 建立 Web Service

1. 點擊 **New +** → **Web Service**
2. 選擇 **Connect a repository**
3. 找到你的 `agriculture-line-bot` repository 並點擊 **Connect**

### 3. 設定服務

Render 會自動偵測到 `render.yaml`，或手動設定：

- **Name**: `agriculture-line-bot`
- **Region**: `Singapore` (最接近台灣)
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Instance Type**: `Free`

### 4. 設定環境變數

在 **Environment** 區塊新增：

```
LINE_CHANNEL_ACCESS_TOKEN = [你的LINE Access Token]
LINE_CHANNEL_SECRET = [你的LINE Secret]
GROQ_API_KEY = [你的Groq API Key]
PORT = 10000
```

**從 .env 檔案複製這些值**

### 5. 部署

點擊 **Create Web Service**，等待部署完成（約 3-5 分鐘）

部署成功後，你會得到一個網址，例如：
```
https://agriculture-line-bot.onrender.com
```

---

## 🔧 更新 LINE Webhook

1. 前往 LINE Developers Console
2. 更新 Webhook URL 為：
   ```
   https://[你的render網址].onrender.com/callback
   ```
3. 點擊 Verify 測試

---

## ✅ 完成！

現在你的 LINE Bot 會 24/7 運行在雲端，不需要開著電腦！

### 注意事項

- **免費方案限制**：閒置 15 分鐘後會休眠，首次回應需要 30-60 秒喚醒
- **如何避免休眠**：
  1. 使用付費方案（$7/月）
  2. 或使用 cron job 定期 ping 你的服務（例如用 UptimeRobot）

---

## 🔄 更新程式碼

之後要更新程式碼，只需：

```powershell
cd C:\line_ai
git add .
git commit -m "更新說明"
git push
```

Render 會自動重新部署！

---

## 💰 費用說明

- **Render 免費方案**：
  - ✅ 750 小時/月運行時間
  - ✅ 足夠一個服務 24/7 運行
  - ⚠️ 會休眠（閒置 15 分鐘）
  - ⚠️ 每月 100GB 流量

- **付費方案**：$7/月起
  - ✅ 不會休眠
  - ✅ 更好效能
  - ✅ 自動擴展

---

## 🆘 常見問題

### Q: 部署失敗怎麼辦？
查看 Render 的 Logs 頁面，找出錯誤訊息

### Q: 如何查看運行狀態？
在 Render Dashboard 可以看到：
- 部署狀態
- 即時 Logs
- 效能監控

### Q: 可以用其他雲端服務嗎？
可以！其他選擇：
- Railway.app
- Google Cloud Run
- Heroku (已改為付費)
- AWS Elastic Beanstalk
- Azure App Service

---

需要我幫你設定 Git 並推送到 GitHub 嗎？
