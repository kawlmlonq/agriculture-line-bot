# Synology NAS 快速部署步驟

## 🚀 10 分鐘快速部署

### 前置作業（5 分鐘）

1. **在 NAS 上安裝套件**
   - 套件中心 → 搜尋「Container Manager」→ 安裝
   - 或搜尋「Docker」（舊版 DSM）

2. **啟用 SSH**
   - 控制台 → 終端機與 SNMP → 啟用 SSH 服務

3. **準備檔案**
   - 確保專案已在本機測試成功
   - 確保 `vector_db/` 資料夾已建立（234 文件）
   - 確保 `.env` 已設定所有 API Keys

---

### 部署步驟（5 分鐘）

#### 步驟 1: 上傳檔案

**方法 A - 使用 PowerShell（推薦）**
```powershell
# 在專案目錄執行
$NAS_IP = "192.168.1.100"  # 改成你的 NAS IP

# 壓縮專案（排除不必要檔案）
$exclude = @("*.bat", ".git", ".venv", "__pycache__", "*.pyc")
Compress-Archive -Path * -DestinationPath agriculture-bot.zip

# 上傳到 NAS
scp agriculture-bot.zip admin@${NAS_IP}:/volume1/docker/

# SSH 連接並解壓縮
ssh admin@$NAS_IP
cd /volume1/docker
unzip agriculture-bot.zip -d agriculture-line-bot
cd agriculture-line-bot
```

**方法 B - 使用 File Station**
1. 開啟 File Station
2. 進入 `docker` 資料夾（沒有則建立）
3. 建立 `agriculture-line-bot` 資料夾
4. 上傳所有專案檔案

---

#### 步驟 2: 執行部署腳本

```bash
# SSH 連接 NAS
ssh admin@your-nas-ip

# 進入專案目錄
cd /volume1/docker/agriculture-line-bot

# 賦予執行權限
sudo chmod +x deploy_nas.sh

# 執行部署
sudo bash deploy_nas.sh
```

腳本會自動：
- ✅ 檢查 Docker
- ✅ 建立目錄
- ✅ 驗證檔案
- ✅ 檢查環境變數
- ✅ 建置映像
- ✅ 啟動容器
- ✅ 執行健康檢查

---

#### 步驟 3: 設定外部連線

**選項 A - ngrok（最簡單）**
```bash
# 下載 ngrok
cd /volume1/docker
sudo wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz
sudo tar xvzf ngrok-v3-stable-linux-arm.tgz

# 設定 authtoken（從 ngrok.com 取得）
./ngrok config add-authtoken YOUR_TOKEN

# 啟動 ngrok
nohup ./ngrok http 5000 > ngrok.log 2>&1 &

# 查看 URL
cat ngrok.log | grep "Forwarding"
# 或訪問 http://localhost:4040
```

**選項 B - Synology DDNS（免費永久）**
1. 控制台 → 外部存取 → DDNS
2. 新增 → Synology
3. 主機名稱：`yourname.synology.me`
4. 路由器設定端口轉發：5000 → NAS IP:5000
5. LINE Webhook: `http://yourname.synology.me:5000/callback`

---

#### 步驟 4: 更新 LINE Webhook

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 選擇你的 Channel
3. Messaging API → Webhook URL
4. 填入：`https://your-ngrok-url.ngrok.io/callback`
5. 點擊「Verify」測試
6. 啟用「Use webhook」

---

### 驗證部署

**1. 檢查容器狀態**
```bash
sudo docker ps | grep agriculture
# 應顯示 "Up X minutes"
```

**2. 測試健康端點**
```bash
curl http://localhost:5000/health
# 應返回 {"status":"healthy",...}
```

**3. 查看日誌**
```bash
sudo docker logs agriculture-line-bot
# 應看到：
# ✓ 向量資料庫已載入: 234 個文件
# ✓ LINE Bot 已就緒
```

**4. 測試 LINE Bot**
- 在 LINE 上傳送訊息給 Bot
- 應收到回應

---

## 🔧 日常管理

### 查看日誌
```bash
# 即時查看
sudo docker logs -f agriculture-line-bot

# 最近 100 行
sudo docker logs --tail 100 agriculture-line-bot
```

### 重啟服務
```bash
# 重啟容器
sudo docker restart agriculture-line-bot

# 完全重建
cd /volume1/docker/agriculture-line-bot
sudo docker-compose down
sudo docker-compose up -d --build
```

### 更新提示詞
```bash
# 方法 1: File Station 編輯 prompts.py 後重啟
sudo docker restart agriculture-line-bot

# 方法 2: SSH 編輯
cd /volume1/docker/agriculture-line-bot
sudo nano prompts.py
# 編輯後存檔
sudo docker restart agriculture-line-bot
```

### 更新資料庫
```bash
# 進入容器
sudo docker exec -it agriculture-line-bot bash

# 執行載入腳本
python scripts/load_data.py

# 退出並重啟
exit
sudo docker restart agriculture-line-bot
```

---

## 📊 監控

### 資源使用
```bash
# 即時監控
sudo docker stats agriculture-line-bot

# 預期占用：
# CPU: 1-5%
# MEM: 150-300MB
```

### 自動重啟設定
容器已設定 `restart: unless-stopped`，會在：
- NAS 重啟後自動啟動
- 容器崩潰後自動重啟

---

## 🆘 常見問題

### Q1: 容器無法啟動
```bash
# 查看錯誤
sudo docker logs agriculture-line-bot

# 常見原因：
# - .env 檔案遺失
# - Port 5000 被占用
# - 記憶體不足
```

### Q2: LINE Bot 無回應
```bash
# 檢查順序
1. 容器是否運行：docker ps
2. 健康檢查：curl http://localhost:5000/health
3. ngrok 是否運行：ps aux | grep ngrok
4. LINE Webhook URL 是否正確
```

### Q3: 向量資料庫未載入
```bash
# 檢查 vector_db 資料夾
ls -la /volume1/docker/agriculture-line-bot/vector_db/

# 重新載入
sudo docker exec -it agriculture-line-bot python scripts/load_data.py
```

---

## 📱 快速指令備忘

```bash
# SSH 連接
ssh admin@nas-ip

# 進入專案
cd /volume1/docker/agriculture-line-bot

# 查看狀態
sudo docker ps

# 查看日誌
sudo docker logs -f agriculture-line-bot

# 重啟
sudo docker restart agriculture-line-bot

# 停止
sudo docker stop agriculture-line-bot

# 啟動
sudo docker start agriculture-line-bot

# 進入容器
sudo docker exec -it agriculture-line-bot bash
```

---

## 🎯 檢查清單

**部署前：**
- [ ] Container Manager 已安裝
- [ ] SSH 已啟用
- [ ] 所有檔案已準備（含 .env 和 vector_db）

**部署中：**
- [ ] 檔案已上傳到 NAS
- [ ] deploy_nas.sh 執行成功
- [ ] 容器狀態顯示「執行中」

**部署後：**
- [ ] 健康檢查通過
- [ ] ngrok/DDNS 已設定
- [ ] LINE Webhook 已更新
- [ ] LINE Bot 測試成功

---

**預估時間：** 10-15 分鐘  
**難度：** ⭐⭐（簡單）  

祝您部署順利！有問題請參考 `Synology_NAS_部署指南.md` 完整文件。
