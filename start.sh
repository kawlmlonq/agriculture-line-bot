#!/bin/bash
# 雲端啟動腳本 - 自動載入資料並啟動服務

echo "🚀 開始初始化..."

# 載入資料到向量資料庫
echo "📚 載入農業知識資料..."
python scripts/load_data.py

# 啟動 Flask 服務
echo "🌐 啟動 LINE Bot 服務..."
python app.py
