# 🌾 農業向量資料庫 LINE Bot - 專案總覽

## 📁 專案結構

```
line_ai/
│
├── 📄 app.py                      # Flask 主應用程式（LINE Bot 伺服器）
├── 📄 config.py                   # 設定檔（管理所有環境變數和參數）
├── 📄 requirements.txt            # Python 套件依賴清單
├── 📄 .env                        # 環境變數（需自行建立，包含 API Keys）
├── 📄 .env.example               # 環境變數範本
├── 📄 .gitignore                 # Git 忽略清單
│
├── 📚 README.md                   # 專案完整說明文件
├── 📚 QUICKSTART.md              # 快速開始指南
├── 📚 USAGE.md                   # 詳細使用說明
├── 📚 DEPLOYMENT.md              # 部署指南
├── 📚 PROJECT_OVERVIEW.md        # 本檔案（專案總覽）
│
├── 🔧 setup.ps1                  # Windows PowerShell 自動設定腳本
│
├── 📂 src/                        # 原始碼資料夾
│   ├── __init__.py               # 套件初始化
│   ├── 📄 document_loader.py     # 文件載入器（處理 PDF, DOCX, TXT）
│   ├── 📄 vector_store.py        # 向量資料庫管理（ChromaDB）
│   ├── 📄 qa_engine.py           # 問答引擎（RAG 實作）
│   └── 📄 line_bot.py            # LINE Bot 處理器
│
├── 📂 scripts/                    # 工具腳本資料夾
│   ├── 📄 load_data.py           # 資料載入腳本
│   ├── 📄 test_qa.py             # 問答功能測試
│   └── 📄 check_system.py        # 系統環境檢查
│
├── 📂 data/                       # 資料檔案資料夾
│   └── 📂 agriculture/           # 農業知識文件
│       └── 📄 sample_data.txt    # 範例農業資料
│
├── 📂 vector_db/                  # 向量資料庫（自動建立）
│   └── (ChromaDB 檔案)
│
└── 📂 venv/                       # Python 虛擬環境（自動建立）
    └── (Python 套件)
```

## 🔄 系統架構流程

```
使用者 (LINE App)
        ↓
        ↓ 發送訊息
        ↓
┌───────────────────────────────────────┐
│   LINE Messaging API                  │
│   (LINE 官方伺服器)                   │
└───────────────────────────────────────┘
        ↓
        ↓ Webhook
        ↓
┌───────────────────────────────────────┐
│   Flask Web Server (app.py)          │
│   - 接收 LINE Webhook                │
│   - 路由處理                          │
└───────────────────────────────────────┘
        ↓
        ↓ 處理訊息
        ↓
┌───────────────────────────────────────┐
│   LINE Bot Handler                    │
│   (src/line_bot.py)                   │
│   - 解析使用者訊息                    │
│   - 處理指令                          │
└───────────────────────────────────────┘
        ↓
        ↓ 提問
        ↓
┌───────────────────────────────────────┐
│   QA Engine (src/qa_engine.py)       │
│   - RAG 問答引擎                      │
└───────────────────────────────────────┘
        ↓
        ↓ 檢索
        ↓
┌───────────────────────────────────────┐
│   Vector Store                        │
│   (src/vector_store.py)               │
│   - 將問題轉為向量                    │
│   - 搜尋相似文件                      │
└───────────────────────────────────────┘
        ↓
        ↓ 相關文件
        ↓
┌───────────────────────────────────────┐
│   ChromaDB (向量資料庫)               │
│   - 儲存文件向量                      │
│   - 語義搜尋                          │
└───────────────────────────────────────┘
        ↓
        ↓ 取得上下文
        ↓
┌───────────────────────────────────────┐
│   LLM (OpenAI GPT)                    │
│   - 根據上下文生成回答                │
└───────────────────────────────────────┘
        ↓
        ↓ 生成回答
        ↓
┌───────────────────────────────────────┐
│   回傳給使用者                        │
└───────────────────────────────────────┘
```

## 🧩 核心元件說明

### 1. Flask Web Server (`app.py`)
- **職責**：HTTP 伺服器，接收 LINE Webhook
- **端點**：
  - `/` - 首頁
  - `/callback` - LINE Webhook 回調
  - `/health` - 健康檢查
  - `/test` - API 測試（開發用）

### 2. LINE Bot Handler (`src/line_bot.py`)
- **職責**：處理 LINE 訊息事件
- **功能**：
  - 接收使用者訊息
  - 處理特殊指令（/help, /about, /topics）
  - 呼叫 QA Engine 生成回答
  - 傳送訊息給使用者

### 3. QA Engine (`src/qa_engine.py`)
- **職責**：實作 RAG（檢索增強生成）
- **流程**：
  1. 接收使用者問題
  2. 從向量資料庫檢索相關文件
  3. 組合上下文和問題
  4. 呼叫 LLM 生成回答
  5. 回傳答案和來源

### 4. Vector Store (`src/vector_store.py`)
- **職責**：管理向量資料庫
- **功能**：
  - 將文字轉換為向量（Embedding）
  - 儲存向量到 ChromaDB
  - 語義搜尋（找出最相關的文件）
  - 資料庫管理

### 5. Document Loader (`src/document_loader.py`)
- **職責**：載入和處理文件
- **支援格式**：
  - TXT - 純文字檔
  - PDF - PDF 文件
  - DOCX - Word 文件
- **功能**：
  - 讀取文件內容
  - 分割成適當大小的區塊
  - 附加元資料（來源、頁碼等）

## 🔑 關鍵技術

### RAG (Retrieval-Augmented Generation)
```
問題 → 向量化 → 搜尋相似文件 → 組合上下文 → LLM 生成回答
```

**優勢**：
- ✅ 回答基於實際資料，不會憑空捏造
- ✅ 可以追溯資料來源
- ✅ 容易更新知識（只需更新文件）
- ✅ 支援專業領域知識

### 向量資料庫 (ChromaDB)
- **作用**：儲存文件的語義向量
- **搜尋方式**：語義搜尋（不是關鍵字匹配）
- **範例**：
  - 問「如何種水稻」能找到「水稻栽培方法」
  - 問「番茄病害」能找到「番茄疾病防治」

### 嵌入模型 (Sentence Transformers)
- **模型**：`paraphrase-multilingual-MiniLM-L12-v2`
- **作用**：將文字轉換為向量
- **特點**：支援繁體中文、多語言

### LLM (Large Language Model)
- **預設**：OpenAI GPT-3.5-turbo
- **作用**：根據檢索到的上下文生成自然的回答
- **可替換**：可改用其他 LLM（如本地模型）

## 📊 資料流程

### 資料載入階段
```
農業文件 (PDF/DOCX/TXT)
    ↓
Document Loader 讀取
    ↓
分割成小區塊
    ↓
Embedding Model 轉向量
    ↓
存入 ChromaDB
```

### 問答階段
```
使用者問題
    ↓
Embedding Model 轉向量
    ↓
ChromaDB 搜尋相似向量
    ↓
取得相關文件
    ↓
組合提示詞
    ↓
OpenAI GPT 生成回答
    ↓
回傳給使用者
```

## 🎯 使用場景

### 1. 農民/種植者
- 查詢作物種植方法
- 了解病蟲害防治
- 學習施肥技巧

### 2. 農業顧問
- 快速查找專業知識
- 提供客戶諮詢依據
- 教育訓練輔助

### 3. 農業教育
- 學生學習輔助
- 教材參考
- 快速問答

### 4. 研究人員
- 快速查找文獻
- 知識整理
- 資料檢索

## 🔒 安全性考量

### API Keys 保護
- 使用 `.env` 檔案儲存敏感資訊
- `.gitignore` 防止提交到版本控制
- 不在程式碼中硬編碼

### LINE Webhook 驗證
- 驗證 `X-Line-Signature`
- 防止偽造請求

### 錯誤處理
- 所有 API 呼叫都有錯誤處理
- 避免洩漏系統資訊
- 友善的錯誤訊息

## 📈 效能優化建議

### 向量資料庫
- 定期清理不需要的文件
- 適當的區塊大小（500-1000 字）
- 使用較小的嵌入模型（如需要）

### LLM 呼叫
- 限制回答長度（MAX_TOKENS）
- 快取常見問題（可選）
- 使用較便宜的模型（如 gpt-3.5-turbo）

### 文件處理
- 批次載入文件
- 異步處理大量文件
- 增量更新（只載入新文件）

## 🚀 擴展可能性

### 功能擴展
- [ ] 多使用者對話記憶
- [ ] 圖片識別（病蟲害照片辨識）
- [ ] 語音問答
- [ ] 推薦系統（主動推送資訊）
- [ ] 多語言支援

### 技術升級
- [ ] 使用本地 LLM（降低成本）
- [ ] 加入圖資料庫（知識圖譜）
- [ ] 實作向量資料庫分片
- [ ] WebSocket 即時互動
- [ ] 機器學習模型微調

### 平台擴展
- [ ] Facebook Messenger
- [ ] Telegram Bot
- [ ] Discord Bot
- [ ] Web Chat Widget
- [ ] 行動 App

## 📚 相關資源

### 文件
- [ChromaDB 文件](https://docs.trychroma.com/)
- [LangChain 文件](https://python.langchain.com/)
- [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/)
- [OpenAI API](https://platform.openai.com/docs/)

### 教學
- RAG 實作教學
- 向量資料庫原理
- LINE Bot 開發指南

## 🤝 貢獻指南

歡迎改進這個專案！可以：
- 新增更多農業知識
- 優化問答品質
- 增加新功能
- 修復 Bug
- 改善文件

## 📝 授權

MIT License - 可自由使用、修改、分發

---

**最後更新**: 2025年11月8日
**版本**: 1.0.0
