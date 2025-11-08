# LINE Bot 部署指南

## 本地開發測試

### 使用 ngrok 建立公開 URL

1. **下載並安裝 ngrok**
   - 前往 https://ngrok.com/ 下載
   - 註冊帳號並取得 authtoken

2. **啟動 ngrok**
   ```powershell
   ngrok http 5000
   ```

3. **複製 HTTPS URL**
   - ngrok 會顯示類似 `https://xxxx.ngrok.io` 的網址
   - 這就是你的公開 Webhook URL

4. **設定 LINE Webhook**
   - 到 LINE Developers Console
   - 設定 Webhook URL: `https://xxxx.ngrok.io/callback`
   - 啟用 Webhook

## 雲端部署選項

### 選項 1: Heroku

1. **安裝 Heroku CLI**
   ```powershell
   # 從 https://devcenter.heroku.com/articles/heroku-cli 下載安裝
   ```

2. **建立 Procfile**
   ```
   web: python app.py
   ```

3. **部署**
   ```powershell
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. **設定環境變數**
   ```powershell
   heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token
   heroku config:set LINE_CHANNEL_SECRET=your_secret
   heroku config:set OPENAI_API_KEY=your_key
   ```

### 選項 2: Google Cloud Run

1. **建立 Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "app.py"]
   ```

2. **部署**
   ```powershell
   gcloud run deploy agriculture-bot --source .
   ```

### 選項 3: AWS EC2

1. **啟動 EC2 執行個體**
   - 選擇 Ubuntu Server
   - 開放 Port 5000 或 80/443

2. **安裝相依套件**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements.txt
   ```

3. **使用 Supervisor 或 systemd 保持服務運行**

### 選項 4: Railway.app

1. **連接 GitHub 儲存庫**
2. **自動偵測並部署**
3. **設定環境變數**

## 環境變數設定

無論使用哪種部署方式，都需要設定以下環境變數：

```
LINE_CHANNEL_ACCESS_TOKEN=你的LINE Channel Access Token
LINE_CHANNEL_SECRET=你的LINE Channel Secret
OPENAI_API_KEY=你的OpenAI API Key
VECTOR_DB_PATH=./vector_db
COLLECTION_NAME=agriculture_qa
PORT=5000
```

## LINE Developers 設定步驟

### 1. 建立 Provider
1. 登入 [LINE Developers Console](https://developers.line.biz/)
2. 點選「Create a new provider」
3. 輸入 Provider 名稱

### 2. 建立 Messaging API Channel
1. 點選「Create a channel」
2. 選擇「Messaging API」
3. 填寫必要資訊：
   - Channel name: 農業知識庫 Bot
   - Channel description: 農業問答助手
   - Category: 選擇適當類別
   - Subcategory: 選擇適當子類別

### 3. 取得憑證
1. 進入 Channel 設定頁面
2. 在「Basic settings」找到 **Channel Secret**
3. 在「Messaging API」找到 **Channel Access Token**（需要先 Issue）

### 4. 設定 Webhook
1. 在「Messaging API」分頁
2. 設定 Webhook URL: `https://your-domain.com/callback`
3. 啟用「Use webhook」
4. 停用「Auto-reply messages」（可選）

### 5. 加入好友
1. 使用 QR Code 加入 Bot 為好友
2. 開始測試！

## 監控與維護

### 查看日誌
```powershell
# 本地開發
# 直接在終端機查看

# Heroku
heroku logs --tail

# Google Cloud
gcloud logging read

# AWS EC2
sudo journalctl -u your-service-name -f
```

### 健康檢查
訪問 `https://your-domain.com/health` 查看系統狀態

### 更新資料
1. 新增或修改 `data/agriculture/` 中的文件
2. 執行 `python scripts/load_data.py`
3. 重啟服務

## 常見問題

### Q: Webhook 驗證失敗
A: 檢查 Channel Secret 是否正確設定

### Q: Bot 沒有回應
A: 
1. 確認 Webhook URL 可以從外部訪問
2. 檢查伺服器日誌
3. 確認向量資料庫已正確載入資料

### Q: 回答品質不佳
A:
1. 增加更多高品質的農業知識文件
2. 調整 RAG 參數（TOP_K_RESULTS）
3. 優化提示詞

### Q: OpenAI API 費用
A:
1. 考慮使用本地 LLM（如 Llama 2, Mistral）
2. 設定每日使用限額
3. 快取常見問題的答案
