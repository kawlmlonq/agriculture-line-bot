# 🌾 農業向量資料庫 LINE Bot

## 專案已完成！

恭喜！你的農業向量資料庫 LINE Bot 專案已經建立完成。

## 📦 包含的檔案

### 核心程式
✅ `app.py` - Flask 主應用程式
✅ `config.py` - 設定檔
✅ `requirements.txt` - 套件依賴

### 原始碼模組
✅ `src/document_loader.py` - 文件載入器
✅ `src/vector_store.py` - 向量資料庫
✅ `src/qa_engine.py` - 問答引擎
✅ `src/line_bot.py` - LINE Bot 處理器

### 工具腳本
✅ `scripts/load_data.py` - 資料載入
✅ `scripts/test_qa.py` - 問答測試
✅ `scripts/check_system.py` - 系統檢查

### 文件
✅ `README.md` - 專案說明
✅ `QUICKSTART.md` - 快速開始
✅ `USAGE.md` - 使用指南
✅ `DEPLOYMENT.md` - 部署指南
✅ `PROJECT_OVERVIEW.md` - 專案總覽
✅ `CHANGELOG.md` - 更新日誌

### 範例資料
✅ `data/agriculture/sample_data.txt` - 農業知識範例

### 設定檔
✅ `.env.example` - 環境變數範本
✅ `.gitignore` - Git 忽略清單
✅ `setup.ps1` - 自動設定腳本

## 🚀 下一步

### 1. 執行自動設定
```powershell
.\setup.ps1
```

### 2. 設定環境變數
編輯 `.env` 檔案，填入：
- LINE Channel Access Token
- LINE Channel Secret
- OpenAI API Key

### 3. 載入資料
```powershell
python scripts\load_data.py
```

### 4. 測試功能（選擇性）
```powershell
python scripts\test_qa.py
```

### 5. 啟動服務
```powershell
python app.py
```

### 6. 設定 LINE Webhook
使用 ngrok 建立公開 URL，並在 LINE Developers Console 設定 Webhook

## 📚 詳細指南

請參閱以下文件獲取詳細資訊：

1. **快速開始** → `QUICKSTART.md`
2. **使用說明** → `USAGE.md`
3. **部署指南** → `DEPLOYMENT.md`
4. **專案架構** → `PROJECT_OVERVIEW.md`

## ⚡ 快速參考

### 常用指令
```powershell
# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 系統檢查
python scripts\check_system.py

# 載入資料
python scripts\load_data.py

# 測試問答
python scripts\test_qa.py

# 啟動服務
python app.py
```

### LINE Bot 指令
- `/help` - 顯示幫助
- `/about` - 關於系統
- `/topics` - 可查詢主題

## 🎯 功能特色

✨ **智能問答** - 基於 RAG 技術的精準回答
🔍 **語義搜尋** - 理解問題的真正意圖
📚 **知識追溯** - 每個回答都有資料來源
💬 **對話介面** - 透過 LINE 輕鬆使用
🌾 **專業知識** - 專注於農業領域
🔧 **易於擴展** - 只需新增文件即可更新知識

## 🛠️ 技術亮點

- **向量資料庫** (ChromaDB) - 高效語義搜尋
- **嵌入模型** (Sentence Transformers) - 多語言支援
- **大型語言模型** (OpenAI GPT) - 自然語言生成
- **LINE Messaging API** - 即時對話互動
- **Flask Web 框架** - 輕量級高效能

## 📊 系統流程

```
使用者提問 → LINE → Webhook → 向量搜尋 → LLM 生成 → 回答
```

## 💡 使用技巧

1. **問題要具體** - 「如何種植水稻」比「水稻」更好
2. **善用指令** - 使用 /topics 查看可查詢的主題
3. **更新知識** - 定期新增文件並重新載入
4. **測試優先** - 先用 test_qa.py 測試再上線

## 🔒 安全提醒

- ⚠️ 不要將 `.env` 檔案提交到 Git
- ⚠️ 妥善保管 API Keys
- ⚠️ 定期更新套件版本
- ⚠️ 使用 HTTPS（部署時）

## 📞 需要幫助？

1. 執行 `python scripts\check_system.py` 診斷問題
2. 查看終端機日誌訊息
3. 閱讀相關文件
4. 檢查 .env 設定

## 🎉 開始使用

你現在已經擁有一個完整的農業知識庫 LINE Bot 系統！

按照 QUICKSTART.md 的步驟，幾分鐘內就可以啟動你的 Bot。

祝你使用愉快！🌾

---

**專案建立時間**: 2025年11月8日
**版本**: 1.0.0
**授權**: MIT License
