#!/bin/bash

# 農業知識庫 LINE Bot - NAS 快速部署腳本

set -e

echo "🚀 開始部署農業知識庫 LINE Bot..."

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安裝，請先安裝 Docker"
    exit 1
fi

# 檢查 Docker Compose 是否安裝
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安裝，請先安裝 Docker Compose"
    exit 1
fi

# 檢查 .env 檔案
if [ ! -f .env ]; then
    echo "❌ 找不到 .env 檔案"
    echo "請建立 .env 檔案並設定以下變數："
    echo "  LINE_CHANNEL_ACCESS_TOKEN=..."
    echo "  LINE_CHANNEL_SECRET=..."
    echo "  GROQ_API_KEY=..."
    exit 1
fi

echo "✓ Docker 環境檢查通過"

# 停止舊容器（如果存在）
echo "⏸️  停止舊容器..."
docker-compose down 2>/dev/null || true

# 建置新映像
echo "🔨 建置 Docker 映像..."
docker-compose build

# 啟動服務
echo "🚀 啟動服務..."
docker-compose up -d

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 15

# 檢查服務狀態
echo "🔍 檢查服務狀態..."
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ 服務啟動成功！"
    echo ""
    echo "📊 服務資訊："
    docker-compose ps
    echo ""
    echo "📝 查看日誌："
    echo "  docker-compose logs -f"
    echo ""
    echo "🔗 下一步："
    echo "  1. 設定 ngrok 或反向代理"
    echo "  2. 更新 LINE Webhook URL"
    echo "  3. 測試 LINE Bot 功能"
else
    echo "❌ 服務啟動失敗"
    echo "查看日誌："
    docker-compose logs
    exit 1
fi
