# 快速開始指南

## 第一次使用

### 1. 建立虛擬環境並安裝套件

```powershell
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 安裝所需套件
pip install -r requirements.txt
```

### 2. 設定環境變數

```powershell
# 複製範例檔案
copy .env.example .env

# 編輯 .env 檔案，填入你的設定
notepad .env
```

需要填入的資訊：
- `LINE_CHANNEL_ACCESS_TOKEN` - 從 LINE Developers Console 取得
- `LINE_CHANNEL_SECRET` - 從 LINE Developers Console 取得
- `OPENAI_API_KEY` - 從 OpenAI 取得（如果使用 OpenAI）

### 3. 準備農業資料

將你的農業知識文件放入 `data/agriculture/` 資料夾：
- 支援格式：TXT, PDF, DOCX
- 系統已包含範例資料供測試

### 4. 載入資料到向量資料庫

```powershell
python scripts\load_data.py
```

這個步驟會：
- 讀取 `data/agriculture/` 中的所有文件
- 將文件轉換為向量並儲存到資料庫
- 第一次執行會下載嵌入模型（約 500MB）

### 5. 測試問答功能（選擇性）

在啟動 LINE Bot 之前，可以先測試問答功能：

```powershell
python scripts\test_qa.py
```

### 6. 啟動 LINE Bot 服務

```powershell
python app.py
```

服務啟動後會顯示：
```
🌾 農業知識庫 LINE Bot 伺服器
============================================================
伺服器位址: http://localhost:5000
Webhook URL: http://localhost:5000/callback
健康檢查: http://localhost:5000/health
============================================================
```

### 7. 設定公開網址（本地開發）

本地開發需要使用 ngrok 或類似工具建立公開 URL：

```powershell
# 在另一個終端機執行
ngrok http 5000
```

複製 ngrok 提供的 HTTPS URL（例如 `https://xxxx.ngrok.io`）

### 8. 設定 LINE Webhook

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 選擇你的 Channel
3. 在「Messaging API」分頁中：
   - Webhook URL: `https://xxxx.ngrok.io/callback`
   - 啟用「Use webhook」
   - 點擊「Verify」測試連線

### 9. 開始使用

1. 用手機掃描 LINE Bot 的 QR Code
2. 加入 Bot 為好友
3. 開始提問！

## 範例對話

```
你: 水稻的種植季節是什麼時候？
Bot: 水稻是台灣最重要的糧食作物之一...

你: /help
Bot: 🌾 農業知識庫 LINE Bot 使用說明...
```

## 常用指令

### 問答測試
```powershell
python scripts\test_qa.py
```

### 重新載入資料
```powershell
python scripts\load_data.py
```

### 啟動服務
```powershell
python app.py
```

### 檢查健康狀態
開啟瀏覽器訪問：http://localhost:5000/health

## 專案結構

```
line_ai/
├── app.py                    # Flask 主應用
├── config.py                 # 設定檔
├── requirements.txt          # Python 套件
├── .env                      # 環境變數（需自行建立）
├── README.md                 # 專案說明
├── QUICKSTART.md            # 本檔案
├── DEPLOYMENT.md            # 部署指南
│
├── src/                      # 原始碼
│   ├── __init__.py
│   ├── document_loader.py   # 文件載入
│   ├── vector_store.py      # 向量資料庫
│   ├── qa_engine.py         # 問答引擎
│   └── line_bot.py          # LINE Bot 處理
│
├── scripts/                  # 工具腳本
│   ├── load_data.py         # 載入資料
│   └── test_qa.py           # 測試問答
│
├── data/                     # 資料檔案
│   └── agriculture/         # 農業文件
│       └── sample_data.txt  # 範例資料
│
└── vector_db/               # 向量資料庫（自動建立）
```

## 疑難排解

### 問題：找不到模組
```powershell
# 確認虛擬環境已啟動
.\venv\Scripts\Activate.ps1

# 重新安裝套件
pip install -r requirements.txt
```

### 問題：向量資料庫是空的
```powershell
# 執行資料載入
python scripts\load_data.py
```

### 問題：LINE Bot 沒有回應
1. 檢查 ngrok 是否正常運行
2. 確認 Webhook URL 設定正確
3. 查看終端機的日誌訊息
4. 確認 .env 中的 Token 和 Secret 正確

### 問題：OpenAI API 錯誤
1. 檢查 API Key 是否有效
2. 確認帳戶有足夠額度
3. 檢查網路連線

### 問題：嵌入模型下載緩慢
模型會自動下載並快取，首次使用需要時間。如果網路不穩定：
1. 使用 VPN 或代理
2. 手動下載模型
3. 或選擇較小的模型（修改 config.py）

## 下一步

- 📖 閱讀 [README.md](README.md) 了解更多功能
- 🚀 閱讀 [DEPLOYMENT.md](DEPLOYMENT.md) 學習如何部署到雲端
- 📝 新增更多農業知識文件到 `data/agriculture/`
- 🎨 自訂 Bot 的回答風格（編輯 `src/qa_engine.py`）
- 🔧 調整參數優化效能（編輯 `config.py`）

有問題或建議歡迎回饋！
