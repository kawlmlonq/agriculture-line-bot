# 農業知識庫 LINE Bot - 最終部署指南

## ✅ 已完成的項目

1. ✅ **系統架構建立** - 24 個專案檔案已建立
2. ✅ **套件安裝** - 所有 Python 套件已安裝並測試
3. ✅ **API 金鑰設定** - LINE 和 Groq API 金鑰已配置
4. ✅ **向量資料庫** - 35 個農業知識文件已載入
5. ✅ **服務測試** - Flask 服務運行正常，問答功能已驗證

## 🎯 系統運行狀態

### 服務資訊
- **Flask 服務**: http://localhost:5000 ✅ 運行中
- **LAN 網址**: http://192.168.1.202:5000
- **向量資料庫**: 35 個文件已載入
- **AI 模型**: Groq llama-3.3-70b-versatile

### 測試結果
```
問題: 有機肥料有哪些種類？
回答: 根據提供的參考資料，有機肥料主要分為四種類：
1. 堆肥：將農業廢棄物經發酵腐熟製成。
2. 廄肥：家畜糞便與墊料混合發酵。
3. 綠肥：種植豆科等植物後翻耕入土。
4. 液肥：動植物質經發酵製成的液態肥料。
```

## 🚀 接下來需要你手動完成的步驟

### 步驟 1: 安裝 ngrok

1. 前往 https://ngrok.com/download 下載 Windows 版本
2. 解壓縮到 `C:\ngrok\`
3. 註冊 ngrok 帳號 (https://dashboard.ngrok.com/signup)
4. 複製你的 authtoken (在 https://dashboard.ngrok.com/get-started/your-authtoken)
5. 在 PowerShell 中執行:
   ```powershell
   cd C:\ngrok
   .\ngrok.exe config add-authtoken [你的authtoken]
   ```

### 步驟 2: 啟動 ngrok

1. 開啟**新的 PowerShell 視窗**
2. 執行:
   ```powershell
   cd C:\ngrok
   .\ngrok.exe http 5000
   ```
3. 你會看到類似這樣的畫面:
   ```
   Session Status                online
   Account                       你的帳號 (Plan: Free)
   Forwarding                    https://1234-5678-9abc.ngrok-free.app -> http://localhost:5000
   ```
4. **複製** `https://` 開頭的網址 (每次啟動都會不同)

### 步驟 3: 設定 LINE Webhook

1. 登入 LINE Developers Console: https://developers.line.biz/console/
2. 選擇你的 Messaging API Channel
3. 找到 **Messaging API** 頁籤
4. 找到 **Webhook settings** 區塊
5. 在 **Webhook URL** 欄位輸入:
   ```
   https://[你的ngrok網址]/callback
   ```
   例如: `https://1234-5678-9abc.ngrok-free.app/callback`
6. 點擊 **Update** 按鈕
7. 點擊 **Verify** 按鈕 (應該會顯示 Success)
8. 確保 **Use webhook** 開關是**開啟**狀態 (綠色)

### 步驟 4: 測試 LINE Bot

1. 在 LINE Developers Console 找到你的 Bot 的 **QR code**
2. 用手機 LINE 掃描 QR code 加入好友
3. 傳送測試訊息:
   - `水稻什麼時候種植？`
   - `番茄要怎麼種？`
   - `有機肥料有哪些種類？`
   - `/help` (查看指令列表)
   - `/topics` (查看可查詢主題)

## 📝 快速啟動指令

### 啟動主服務
```bash
# 方法 1: 使用批次檔 (推薦)
cd C:\line_ai
start_service.bat

# 方法 2: 手動啟動
cd C:\line_ai
python app.py
```

### 啟動 ngrok (在另一個視窗)
```bash
cd C:\ngrok
.\ngrok.exe http 5000
```

### 測試服務健康狀態
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

### 測試問答功能
```powershell
$body = @{question='水稻什麼時候種植？'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/test" -Method POST -Body $body -ContentType "application/json; charset=utf-8"
```

## 🔧 常見問題排除

### Q: ngrok 啟動失敗
**A:** 確保:
1. 已執行 `ngrok config add-authtoken [你的token]`
2. 沒有其他程式佔用 5000 port
3. ngrok.exe 有執行權限

### Q: LINE Webhook 驗證失敗
**A:** 檢查:
1. ngrok 是否正在運行
2. Python 服務是否正在運行
3. Webhook URL 格式: `https://[ngrok網址]/callback`
4. 防火牆是否阻擋連線

### Q: Bot 沒有回應
**A:** 查看:
1. PowerShell 視窗中的錯誤訊息
2. LINE Console 的 Webhook 設定是否正確
3. "Use webhook" 是否已啟用
4. Bot 是否已加為好友

### Q: 回答品質不佳
**A:** 可以:
1. 在 `data/agriculture/` 新增更多資料檔案
2. 執行 `python scripts/load_data.py` 重新載入
3. 調整 `config.py` 中的 `TOP_K_RESULTS` 和 `TEMPERATURE` 參數

## 📁 重要檔案位置

```
C:\line_ai\
├── app.py                    # Flask 主程式
├── config.py                 # 設定檔 (可調整模型參數)
├── .env                      # API 金鑰 (已設定完成)
├── start_service.bat         # 快速啟動腳本
├── data\agriculture\         # 農業知識資料夾 (可新增檔案)
├── vector_db\                # 向量資料庫 (35 個文件)
├── scripts\
│   ├── load_data.py         # 重新載入資料
│   └── check_system.py      # 系統檢查
└── NGROK_SETUP.md           # ngrok 詳細設定指南
```

## 🎓 新增知識資料

1. 在 `data/agriculture/` 資料夾新增文字檔、PDF、DOCX 或 XLSX
2. 執行載入程式:
   ```bash
   cd C:\line_ai
   python scripts/load_data.py
   ```
3. 重啟服務即可

## 📞 支援資源

- **LINE Developers**: https://developers.line.biz/console/
- **Groq Console**: https://console.groq.com/
- **ngrok Dashboard**: https://dashboard.ngrok.com/
- **專案說明**: README.md

---

## ✨ 恭喜！

你的農業知識庫 LINE Bot 已經準備就緒！
只需要完成上述的 ngrok 設定和 LINE Webhook 配置，就可以開始使用了。

**祝你使用愉快！** 🌾🤖
