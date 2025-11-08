# ngrok 快速設定指南

## 📥 步驟 1：下載 ngrok

1. 前往：https://ngrok.com/download
2. 點擊 "Download For Windows"
3. 下載完成後解壓縮到 C:\ngrok\

## 🔑 步驟 2：設定 authtoken（第一次使用）

1. 前往：https://dashboard.ngrok.com/get-started/your-authtoken
2. 複製你的 authtoken
3. 在 PowerShell 執行：

```powershell
cd C:\ngrok
.\ngrok.exe config add-authtoken 你的authtoken
```

## 🚀 步驟 3：啟動 ngrok

**在新的 PowerShell 視窗執行：**

```powershell
cd C:\ngrok
.\ngrok.exe http 5000
```

## 📋 步驟 4：複製 ngrok URL

啟動後你會看到：

```
Forwarding    https://xxxx-xxxx-xxxx.ngrok-free.app -> http://localhost:5000
```

**複製 `https://xxxx-xxxx-xxxx.ngrok-free.app` 這個網址！**

---

## ✅ 完成後需要你手動做的事：

### 到 LINE Developers Console 設定：

1. 登入：https://developers.line.biz/console/
2. 選擇你的 Channel → Messaging API 分頁
3. 找到 "Webhook settings" 區塊
4. 在 "Webhook URL" 填入：
   ```
   https://你的ngrok網址/callback
   ```
   例如：`https://1234-5678-9abc.ngrok-free.app/callback`
   
5. 點擊 "Update" 按鈕
6. 啟用 "Use webhook" 開關
7. 點擊 "Verify" 按鈕（應該顯示 Success）

### 加入 Bot 為好友：

1. 在 Messaging API 分頁找到 QR Code
2. 用手機 LINE 掃描加入

### 測試：

發送訊息給 Bot：
- "水稻什麼時候種植？"
- "/help"
- "有機肥料有哪些種類？"

---

## 🎯 目前系統狀態

✅ LINE Bot 服務已啟動（正在運行）
✅ 向量資料庫已建立（35個農業知識文件）
✅ Groq AI 已連接
⏳ 需要：安裝並啟動 ngrok
⏳ 需要：在 LINE Console 設定 Webhook

---

## 💡 提示

- 保持兩個 PowerShell 視窗開啟：
  1. 執行 `python app.py`（已在運行）
  2. 執行 `ngrok http 5000`（需要啟動）
  
- 每次重啟 ngrok，URL 都會改變，需要重新到 LINE 更新 Webhook URL
