# 農業知識庫 LINE Bot - Docker 部署指南

## NAS Docker 部署步驟

### 1. 準備 NAS 環境

確保您的 NAS 已安裝：
- Docker
- Docker Compose（通常隨 Docker 一起安裝）

### 2. 上傳專案到 NAS

將整個專案資料夾上傳到 NAS，例如：
```
/volume1/docker/agriculture-line-bot/
```

### 3. 設定環境變數

在專案根目錄確認 `.env` 檔案包含所有必要的 API 金鑰：
```bash
LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_ACCESS_TOKEN
LINE_CHANNEL_SECRET=你的_LINE_SECRET
GROQ_API_KEY=你的_GROQ_API_KEY
```

### 4. 建置並啟動容器

使用 SSH 連接到 NAS，或在 NAS 的終端機中執行：

```bash
# 進入專案目錄
cd /volume1/docker/agriculture-line-bot

# 建置 Docker 映像
docker-compose build

# 啟動服務（背景執行）
docker-compose up -d
```

### 5. 檢查服務狀態

```bash
# 查看容器狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 檢查健康狀態
curl http://localhost:5000/health
```

### 6. 設定 ngrok 或 反向代理

#### 選項 A：在 NAS 上運行 ngrok

```bash
# 下載 ngrok（Linux ARM/x64 版本）
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz

# 認證
./ngrok config add-authtoken 你的_NGROK_TOKEN

# 啟動隧道
./ngrok http 5000
```

#### 選項 B：使用 NAS 內建反向代理（推薦）

如果您的 NAS 有公開 IP 和網域：

1. 在 NAS 設定反向代理：
   - 來源：`your-domain.com/linebot`
   - 目標：`localhost:5000`

2. 設定 HTTPS 憑證（Let's Encrypt）

3. 更新 LINE Webhook URL：
   ```
   https://your-domain.com/linebot/callback
   ```

### 7. 自動啟動設定

Docker Compose 已設定 `restart: unless-stopped`，容器會在 NAS 重啟後自動啟動。

### 8. 維護指令

```bash
# 停止服務
docker-compose stop

# 重新啟動服務
docker-compose restart

# 停止並移除容器
docker-compose down

# 更新代碼後重新建置
docker-compose up -d --build

# 查看資源使用
docker stats agriculture-line-bot
```

### 9. 資料持久化

以下目錄已掛載到 NAS：
- `./vector_db` - 向量資料庫（自動持久化）
- `./data` - 農業知識文件

即使容器重啟，這些資料也會保留。

### 10. 疑難排解

#### 容器無法啟動
```bash
docker-compose logs agriculture-line-bot
```

#### 記憶體不足
在 `docker-compose.yml` 中添加資源限制：
```yaml
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 1G
```

#### 端口衝突
修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "5001:5000"  # 改用 5001
```

## NAS 特定注意事項

### Synology NAS
- 可透過 Docker 套件中心安裝 Docker
- 使用 Container Manager 管理容器
- 建議使用 Task Scheduler 設定定期備份

### QNAP NAS
- 透過 Container Station 管理 Docker
- 支援 Docker Compose
- 可設定自動快照備份

### 效能優化
- 建議最少 2GB RAM
- SSD 快取可提升向量資料庫效能
- 使用有線網路連接

## 安全建議

1. **不要將 .env 檔案上傳到 GitHub**
2. **定期更新 Docker 映像**
3. **使用 HTTPS 連接**
4. **設定防火牆規則**
5. **啟用 NAS 的自動更新**

## 監控與日誌

建議設定：
- 日誌輪換避免磁碟空間不足
- 使用 Portainer 視覺化管理 Docker
- 設定健康檢查通知

---

有問題隨時在 [GitHub Issues](https://github.com/kawlmlonq/agriculture-line-bot/issues) 回報！
