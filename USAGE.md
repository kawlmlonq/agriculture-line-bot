# 使用說明

## 🚀 快速開始

### Windows PowerShell 一鍵設定

```powershell
.\setup.ps1
```

這個腳本會自動：
- 建立虛擬環境
- 安裝所有必要套件
- 建立設定檔範本

### 手動設定步驟

如果自動設定失敗，可以手動執行：

```powershell
# 1. 建立虛擬環境
python -m venv venv

# 2. 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 3. 安裝套件
pip install -r requirements.txt

# 4. 複製環境變數範本
copy .env.example .env

# 5. 編輯 .env 填入設定
notepad .env
```

## 📋 系統檢查

在開始之前，執行系統檢查確認一切正常：

```powershell
python scripts\check_system.py
```

## 📚 載入農業知識

### 準備資料

將你的農業知識文件放入 `data/agriculture/` 資料夾：

支援的格式：
- `.txt` - 純文字檔
- `.pdf` - PDF 文件
- `.docx` - Word 文件

範例資料結構：
```
data/agriculture/
├── 水稻栽培手冊.pdf
├── 有機農業指南.docx
├── 病蟲害防治.txt
└── ...
```

### 載入到向量資料庫

```powershell
python scripts\load_data.py
```

這個過程會：
1. 讀取所有文件
2. 切分成適當大小的區塊
3. 轉換為向量
4. 儲存到 ChromaDB

**注意**：首次執行會下載嵌入模型（約 500MB），需要一些時間。

## 🧪 測試問答功能

在啟動 LINE Bot 之前，建議先測試問答功能：

```powershell
python scripts\test_qa.py
```

選擇測試模式：
1. **自動測試** - 使用預設問題測試
2. **互動測試** - 自己輸入問題測試

## 🤖 啟動 LINE Bot

### 本地開發

1. **啟動服務**
   ```powershell
   python app.py
   ```

2. **使用 ngrok 建立公開 URL**（在另一個終端機）
   ```powershell
   ngrok http 5000
   ```

3. **設定 LINE Webhook**
   - 複製 ngrok 提供的 HTTPS URL
   - 前往 LINE Developers Console
   - 設定 Webhook URL: `https://xxxx.ngrok.io/callback`
   - 啟用 Webhook

4. **測試**
   - 用手機加入 Bot 為好友
   - 開始提問！

## 💬 使用 LINE Bot

### 基本使用

直接輸入問題即可：
```
你: 水稻什麼時候種植？
Bot: 水稻是台灣最重要的糧食作物之一...
```

### 指令列表

- `/help` 或 `/說明` - 顯示幫助訊息
- `/about` 或 `/關於` - 關於系統資訊
- `/topics` 或 `/主題` - 顯示可查詢的主題

### 範例問題

**作物栽培**
- 水稻的種植季節是什麼時候？
- 番茄如何整枝修剪？
- 如何育苗？

**病蟲害管理**
- 如何防治水稻病蟲害？
- 番茄常見病害有哪些？
- 有機栽培如何防治病蟲害？

**施肥管理**
- 有機肥料有哪些種類？
- 如何使用有機肥料？
- 植物缺氮有什麼症狀？

**設施栽培**
- 溫室要如何控制環境？
- 適合溫室栽培的作物有哪些？

## 🔧 進階功能

### API 測試端點

系統提供測試端點供開發使用：

```powershell
# 使用 curl 或 Postman 測試
curl -X POST http://localhost:5000/test `
  -H "Content-Type: application/json" `
  -d '{"question": "水稻如何種植？"}'
```

回應格式：
```json
{
  "question": "水稻如何種植？",
  "answer": "...",
  "sources": [
    {
      "source": "data/agriculture/sample_data.txt",
      "snippet": "..."
    }
  ]
}
```

### 健康檢查

```powershell
curl http://localhost:5000/health
```

## 🔄 更新資料

當你新增或修改農業知識文件時：

1. **將新文件放入** `data/agriculture/`
2. **重新載入資料**
   ```powershell
   python scripts\load_data.py
   ```
3. **重啟服務**（如果正在運行）
   - Ctrl+C 停止
   - `python app.py` 重新啟動

## ⚙️ 自訂設定

### 修改模型參數

編輯 `config.py`：

```python
# RAG 設定
TOP_K_RESULTS = 3      # 檢索文件數量（增加可能提高答案品質）
MAX_TOKENS = 500       # 回答長度（增加會更詳細但耗費更多 token）
TEMPERATURE = 0.7      # 創造性（0.0-1.0，越高越有創意）
```

### 更換嵌入模型

```python
# 使用不同的嵌入模型
EMBEDDING_MODEL = 'sentence-transformers/distiluse-base-multilingual-cased-v2'
```

### 使用本地 LLM

如果不想使用 OpenAI，可以整合本地 LLM：

1. 安裝 `llama-cpp-python` 或 `transformers`
2. 修改 `src/qa_engine.py` 中的 `generate_answer` 方法
3. 使用本地模型生成回答

## 📊 監控與維護

### 查看日誌

服務運行時會在終端機顯示日誌：
- 收到的使用者問題
- 搜尋和生成過程
- 錯誤訊息

### 常見問題

**Q: Bot 沒有回應**
- 檢查 ngrok 是否正常運行
- 確認 Webhook URL 設定正確
- 查看終端機日誌

**Q: 回答不準確**
- 增加更多相關文件
- 調整 `TOP_K_RESULTS` 參數
- 優化提示詞

**Q: OpenAI API 錯誤**
- 檢查 API Key 是否有效
- 確認帳戶有額度
- 檢查網路連線

**Q: 嵌入模型下載失敗**
- 使用 VPN
- 手動下載模型
- 選擇較小的模型

## 🚀 部署到生產環境

詳細部署指南請參閱 [DEPLOYMENT.md](DEPLOYMENT.md)

支援的部署平台：
- Heroku
- Google Cloud Run
- AWS EC2
- Railway.app

## 📖 更多資源

- [README.md](README.md) - 專案完整說明
- [QUICKSTART.md](QUICKSTART.md) - 快速開始指南
- [DEPLOYMENT.md](DEPLOYMENT.md) - 詳細部署說明
- [LINE Developers](https://developers.line.biz/) - LINE Bot 文件

## 💡 技術支援

遇到問題？
1. 執行 `python scripts\check_system.py` 檢查系統
2. 查看終端機日誌訊息
3. 閱讀文件中的疑難排解章節
4. 檢查 .env 設定是否正確

祝你使用愉快！🌾
