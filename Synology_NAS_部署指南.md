# Synology NAS 部署指南 (DSM 7.x)

## 📋 目標 NAS 規格
- **型號：** Synology N220J (DS220j 升級版)
- **系統：** DSM 7.x
- **部署方式：** Docker Container

---

## 🎯 部署概述

### 部署架構
```
Internet → Synology NAS → Docker Container → Agriculture LINE Bot
          ↓
      ngrok / DDNS → LINE Webhook
```

### 優勢
- ✅ 24/7 運行，無需電腦開機
- ✅ Docker 隔離環境，安全穩定
- ✅ 自動重啟，容錯能力強
- ✅ 資源占用低（~200MB RAM）

---

## 📦 部署前準備

### 1. 檢查 NAS 系統
- DSM 版本 ≥ 7.0
- 可用空間 ≥ 2GB
- RAM 建議 ≥ 1GB 可用

### 2. 安裝必要套件
登入 DSM → 套件中心 → 安裝以下套件：
- **Container Manager** (或舊版 Docker 套件)
- **File Station**
- **Text Editor** (可選)

### 3. 準備部署檔案
需要上傳到 NAS 的檔案：
```
agriculture-line-bot/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
├── config.py
├── prompts.py
├── .env                    # 重要！包含 API Keys
├── src/                    # 所有原始碼
├── scripts/               # 腳本檔案
└── vector_db/             # 向量資料庫（已建立的）
```

---

## 🚀 部署步驟

### 步驟 1：建立共享資料夾

**DSM 介面操作：**
1. 控制台 → 共享資料夾 → 新增
2. 名稱：`docker`
3. 位置：volume1
4. 不需要啟用資源回收筒

**SSH 操作（進階）：**
```bash
# 連接 NAS
ssh admin@nas-ip-address

# 建立專案資料夾
sudo mkdir -p /volume1/docker/agriculture-line-bot
cd /volume1/docker/agriculture-line-bot
```

---

### 步驟 2：上傳專案檔案

#### 方法 A：使用 File Station（推薦新手）

1. **開啟 File Station**
2. 進入 `docker` 資料夾
3. 建立 `agriculture-line-bot` 資料夾
4. 上傳所有檔案（拖曳上傳）

**重要提醒：**
- ✅ 確認上傳 `.env` 檔案（包含 API Keys）
- ✅ 確認上傳 `vector_db/` 整個資料夾
- ✅ 保持目錄結構不變

#### 方法 B：使用 SCP/SFTP（進階）

**Windows PowerShell：**
```powershell
# 從專案目錄執行
scp -r * admin@nas-ip:/volume1/docker/agriculture-line-bot/
```

**或使用 WinSCP / FileZilla：**
- 協定：SFTP
- 主機：NAS IP
- 帳號：admin
- 上傳路徑：`/volume1/docker/agriculture-line-bot/`

---

### 步驟 3：建立 Docker 映像

#### 方法 A：使用 Container Manager GUI

1. **開啟 Container Manager**
2. 專案 → 新增
3. 選擇來源：「從本機匯入」
4. docker-compose.yml 路徑：`/volume1/docker/agriculture-line-bot/docker-compose.yml`
5. 建立專案

#### 方法 B：使用 SSH（推薦）

```bash
# SSH 連接 NAS
ssh admin@nas-ip-address

# 進入專案目錄
cd /volume1/docker/agriculture-line-bot

# 確認 .env 存在且有內容
cat .env

# 建立並啟動容器
sudo docker-compose up -d --build
```

**預期輸出：**
```
Building agriculture-bot...
Step 1/10 : FROM python:3.12-slim
...
Creating agriculture-line-bot ... done
```

---

### 步驟 4：驗證部署

#### 檢查容器狀態

**GUI 方式：**
1. Container Manager → 容器
2. 找到 `agriculture-line-bot`
3. 狀態應顯示「執行中」🟢

**SSH 方式：**
```bash
# 查看容器狀態
sudo docker ps

# 應該看到：
# CONTAINER ID   IMAGE                  STATUS         PORTS
# xxxx           agriculture-bot:latest Up 2 minutes   0.0.0.0:5000->5000/tcp

# 查看日誌
sudo docker logs agriculture-line-bot

# 應該看到：
# 🚀 初始化系統...
# ✓ 向量資料庫已載入: 234 個文件
# ✓ LINE Bot 已就緒
# 🌾 農業知識庫 LINE Bot 伺服器
```

#### 測試健康檢查

```bash
# 在 NAS 內測試
curl http://localhost:5000/health

# 預期回應：
# {"status":"healthy","vector_db":{"collection":"agriculture_qa","documents":234}}
```

---

### 步驟 5：設定外部連線

#### 選項 A：使用 ngrok（最簡單）

**1. 在 NAS 上安裝 ngrok：**
```bash
# SSH 連接 NAS
cd /volume1/docker

# 下載 ngrok
sudo wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz

# 解壓縮
sudo tar xvzf ngrok-v3-stable-linux-arm64.tgz

# 設定 authtoken
./ngrok config add-authtoken YOUR_NGROK_TOKEN
```

**2. 啟動 ngrok：**
```bash
# 背景執行 ngrok
nohup ./ngrok http 5000 > ngrok.log 2>&1 &

# 查看 ngrok URL
curl http://localhost:4040/api/tunnels | grep public_url

# 或查看日誌
cat ngrok.log
```

**3. 設定 LINE Webhook：**
- 複製 ngrok URL（如 `https://abc123.ngrok.io`）
- LINE Developers Console → Webhook URL → 設定為 `https://abc123.ngrok.io/callback`

#### 選項 B：使用 Synology DDNS（免費）

**1. 啟用 DDNS：**
```
控制台 → 外部存取 → DDNS
→ 新增 → Synology
→ 主機名稱：yourname.synology.me
```

**2. 設定路由器端口轉發：**
```
路由器設定
→ 端口轉發 / Port Forwarding
→ 外部端口：5000 → 內部 IP：NAS IP → 內部端口：5000
```

**3. 設定反向代理（可選，使用 HTTPS）：**
```
控制台 → 登入入口 → 進階 → 反向代理伺服器
→ 來源：yourname.synology.me:443
→ 目的地：localhost:5000
```

**4. LINE Webhook 設定：**
- URL：`https://yourname.synology.me/callback`

#### 選項 C：使用 Cloudflare Tunnel（最安全）

**1. 安裝 cloudflared：**
```bash
# SSH 連接 NAS
cd /volume1/docker
sudo wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
sudo chmod +x cloudflared-linux-arm64
```

**2. 建立 Tunnel：**
```bash
./cloudflared-linux-arm64 tunnel login
./cloudflared-linux-arm64 tunnel create agriculture-bot
./cloudflared-linux-arm64 tunnel route dns agriculture-bot yourbot.yourdomain.com
```

**3. 設定 config：**
```yaml
# ~/.cloudflared/config.yml
tunnel: agriculture-bot
credentials-file: /root/.cloudflared/tunnel-id.json

ingress:
  - hostname: yourbot.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404
```

**4. 啟動 Tunnel：**
```bash
nohup ./cloudflared-linux-arm64 tunnel run > cloudflared.log 2>&1 &
```

---

## 🔧 管理與維護

### 查看容器日誌

**GUI：**
```
Container Manager → 容器 → agriculture-line-bot → 詳細資料 → 日誌
```

**SSH：**
```bash
# 即時查看日誌
sudo docker logs -f agriculture-line-bot

# 查看最近 100 行
sudo docker logs --tail 100 agriculture-line-bot
```

### 重啟容器

**GUI：**
```
Container Manager → 容器 → agriculture-line-bot → 動作 → 重新啟動
```

**SSH：**
```bash
sudo docker restart agriculture-line-bot
```

### 更新應用程式

**方式 1：修改後重新建置**
```bash
cd /volume1/docker/agriculture-line-bot

# 停止容器
sudo docker-compose down

# 修改檔案（如更新 prompts.py）
# 使用 File Station 或 vi/nano 編輯

# 重新建置並啟動
sudo docker-compose up -d --build
```

**方式 2：更新資料不重建**
```bash
# 如果只是更新 prompts.py 或 .env
# 直接重啟即可
sudo docker restart agriculture-line-bot
```

### 更新向量資料庫

**方式 1：在容器內執行**
```bash
# 進入容器
sudo docker exec -it agriculture-line-bot bash

# 執行資料載入
python scripts/load_data.py

# 退出容器
exit

# 重啟容器
sudo docker restart agriculture-line-bot
```

**方式 2：從本機更新**
```bash
# 1. 在 Windows 執行載入
python scripts\load_data.py

# 2. 上傳更新後的 vector_db 資料夾到 NAS
scp -r vector_db/* admin@nas-ip:/volume1/docker/agriculture-line-bot/vector_db/

# 3. 重啟容器
ssh admin@nas-ip "sudo docker restart agriculture-line-bot"
```

### 備份

**自動備份腳本：**
```bash
#!/bin/bash
# /volume1/docker/backup_agriculture_bot.sh

BACKUP_DIR="/volume1/backups/agriculture-bot"
DATE=$(date +%Y%m%d_%H%M%S)

# 建立備份目錄
mkdir -p $BACKUP_DIR

# 備份向量資料庫
tar -czf $BACKUP_DIR/vector_db_$DATE.tar.gz \
  /volume1/docker/agriculture-line-bot/vector_db

# 備份環境變數
cp /volume1/docker/agriculture-line-bot/.env \
  $BACKUP_DIR/env_$DATE.backup

# 保留最近 7 天的備份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

**設定排程備份：**
```
控制台 → 工作排程器 → 新增 → 排程的工作 → 使用者定義的指令碼
→ 每日凌晨 3:00 執行
→ bash /volume1/docker/backup_agriculture_bot.sh
```

---

## 📊 監控與診斷

### 資源使用監控

**GUI：**
```
Container Manager → 容器 → agriculture-line-bot → 詳細資料 → 終端機
```

**SSH：**
```bash
# 查看資源使用
sudo docker stats agriculture-line-bot

# 預期占用：
# CPU: 1-5%
# MEM: 150-300MB
# NET I/O: 視使用量
```

### 健康檢查

```bash
# 定期檢查腳本
#!/bin/bash
# /volume1/docker/health_check.sh

HEALTH=$(curl -s http://localhost:5000/health)

if echo "$HEALTH" | grep -q "healthy"; then
    echo "✅ Bot is healthy"
else
    echo "❌ Bot is unhealthy, restarting..."
    docker restart agriculture-line-bot
fi
```

### 常見問題診斷

**問題 1：容器無法啟動**
```bash
# 檢查日誌
sudo docker logs agriculture-line-bot

# 常見原因：
# - .env 檔案遺失或格式錯誤
# - Port 5000 被占用
# - 向量資料庫檔案損壞
```

**問題 2：LINE Bot 無回應**
```bash
# 1. 檢查容器狀態
sudo docker ps | grep agriculture

# 2. 測試健康端點
curl http://localhost:5000/health

# 3. 檢查 ngrok 是否運行
ps aux | grep ngrok

# 4. 檢查 LINE Webhook URL 設定
```

**問題 3：記憶體不足**
```bash
# 限制容器記憶體
sudo docker update --memory=512m agriculture-line-bot

# 或在 docker-compose.yml 加入：
services:
  agriculture-bot:
    deploy:
      resources:
        limits:
          memory: 512M
```

---

## 🔒 安全建議

### NAS 安全設定

1. **啟用防火牆：**
```
控制台 → 安全性 → 防火牆 → 啟用
→ 只開放必要端口（SSH: 22, HTTP: 80, HTTPS: 443）
```

2. **啟用自動封鎖：**
```
控制台 → 安全性 → 帳號 → 自動封鎖
→ 登入嘗試失敗 5 次封鎖 10 分鐘
```

3. **啟用 2FA：**
```
控制台 → 使用者與群組 → 進階 → 啟用雙重驗證
```

### Docker 安全

1. **使用非 root 使用者（進階）：**
```dockerfile
# Dockerfile 加入
RUN useradd -m -u 1000 botuser
USER botuser
```

2. **定期更新映像：**
```bash
# 每月執行
cd /volume1/docker/agriculture-line-bot
sudo docker-compose pull
sudo docker-compose up -d --build
```

---

## 📱 快速指令參考

### 常用 SSH 指令

```bash
# 連接 NAS
ssh admin@your-nas-ip

# 進入專案目錄
cd /volume1/docker/agriculture-line-bot

# 查看容器狀態
sudo docker ps

# 查看日誌
sudo docker logs -f agriculture-line-bot

# 重啟容器
sudo docker restart agriculture-line-bot

# 停止容器
sudo docker stop agriculture-line-bot

# 啟動容器
sudo docker start agriculture-line-bot

# 完全重建
sudo docker-compose down
sudo docker-compose up -d --build

# 進入容器執行指令
sudo docker exec -it agriculture-line-bot bash
```

---

## 📋 部署檢查清單

### 部署前
- [ ] NAS 已安裝 Container Manager
- [ ] 已建立 `/volume1/docker/agriculture-line-bot` 資料夾
- [ ] 所有檔案已上傳（包含 .env）
- [ ] vector_db 資料夾已上傳（234 文件）
- [ ] .env 中的 API Keys 已設定

### 部署時
- [ ] Docker 映像建置成功
- [ ] 容器啟動成功（狀態：執行中）
- [ ] 健康檢查通過（/health 返回 healthy）
- [ ] 日誌顯示「向量資料庫已載入: 234 個文件」

### 部署後
- [ ] ngrok 或 DDNS 已設定
- [ ] LINE Webhook URL 已更新
- [ ] LINE Bot 回應測試成功
- [ ] 圖片分析功能正常
- [ ] 設定自動備份排程
- [ ] 文件已更新（記錄 NAS IP、ngrok URL 等）

---

## 🆘 故障排除

### 緊急恢復

**如果容器完全無法啟動：**
```bash
# 1. 完全清除
sudo docker-compose down -v
sudo docker system prune -a

# 2. 檢查檔案
ls -la /volume1/docker/agriculture-line-bot/

# 3. 重新建置
sudo docker-compose up -d --build
```

**如果向量資料庫損壞：**
```bash
# 1. 從備份恢復
cd /volume1/backups/agriculture-bot
tar -xzf vector_db_YYYYMMDD_HHMMSS.tar.gz -C /volume1/docker/agriculture-line-bot/

# 2. 或重新載入
sudo docker exec -it agriculture-line-bot bash
python scripts/load_data.py
exit
```

---

## 📞 支援資源

- **Synology 官方文件：** https://kb.synology.com
- **Docker 官方文件：** https://docs.docker.com
- **ngrok 文件：** https://ngrok.com/docs
- **專案 SECURITY.md：** 安全相關問題
- **專案 README.md：** 基本使用說明

---

**部署時間預估：** 30-60 分鐘  
**難度：** ⭐⭐⭐ (中等)  
**建議：** 先在本機測試成功再部署到 NAS

祝您部署順利！ 🎉
