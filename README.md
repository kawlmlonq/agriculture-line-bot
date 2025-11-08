# 農業向量資料庫 LINE Bot

這是一個結合 LINE Messaging API 和向量資料庫的農業知識問答系統。使用者可以透過 LINE 對話介面查詢農業相關知識，系統會從向量資料庫中檢索相關資料並使用 LLM 生成回答。

## 功能特色

- 🌾 **農業知識庫**：儲存和檢索農業相關文件資料
- 💬 **LINE 對話介面**：透過 LINE 進行自然對話問答
- 🔍 **向量搜尋**：使用 ChromaDB 進行高效的語義搜尋
- 🤖 **AI 問答**：整合 LLM 提供智能回答
- 📄 **多格式支援**：支援 PDF、Word、Excel 等多種文件格式

## 系統架構

```
line_ai/
├── app.py                  # Flask 主應用程式
├── config.py              # 設定檔
├── requirements.txt       # Python 套件依賴
├── .env                   # 環境變數 (需自行建立)
├── .env.example          # 環境變數範例
├── vector_db/            # 向量資料庫儲存位置
├── data/                 # 原始資料檔案
│   └── agriculture/      # 農業相關文件
├── src/
│   ├── vector_store.py   # 向量資料庫管理
│   ├── line_bot.py       # LINE Bot 處理
│   ├── qa_engine.py      # 問答引擎
│   └── document_loader.py # 文件載入器
└── scripts/
    └── load_data.py      # 資料載入腳本
```

## 安裝步驟

### 1. 環境準備

```powershell
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 安裝套件
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 為 `.env` 並填入你的設定：

```powershell
copy .env.example .env
```

編輯 `.env` 檔案，填入：
- LINE Channel Access Token
- LINE Channel Secret
- OpenAI API Key (如果使用 OpenAI)

### 3. 準備農業資料

將你的農業相關文件放入 `data/agriculture/` 資料夾中。

### 4. 載入資料到向量資料庫

```powershell
python scripts\load_data.py
```

### 5. 啟動服務

```powershell
python app.py
```

## LINE Bot 設定

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 建立新的 Messaging API Channel
3. 取得 Channel Secret 和 Channel Access Token
4. 設定 Webhook URL: `https://your-domain.com/callback`
5. 啟用 Webhook

## 使用方式

1. 將 LINE Bot 加入好友
2. 直接傳送農業相關問題
3. Bot 會從向量資料庫搜尋相關資料並回答

### 範例問題

- "水稻的最佳種植季節是什麼時候？"
- "如何防治番茄的病蟲害？"
- "有機肥料的使用方法"
- "葡萄的修剪技巧"

## 注意事項

- 確保網路連線正常（需連接 OpenAI API）
- 建議使用 ngrok 或部署到雲端以接收 LINE Webhook
- 向量資料庫會在第一次載入資料時建立
- 資料更新後需重新執行 `load_data.py`

## 技術棧

- **Backend**: Python, Flask
- **Vector DB**: ChromaDB
- **LLM**: OpenAI GPT / 可替換為其他模型
- **Embeddings**: Sentence Transformers
- **Messaging**: LINE Messaging API

## License

MIT License
