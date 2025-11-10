@echo off
chcp 65001 >nul
title 手動啟動 - Agriculture Bot
cls

echo ============================================================
echo 🌾 農業知識庫 LINE Bot - 手動啟動
echo ============================================================
echo.
echo 此腳本會在當前視窗啟動，方便查看錯誤訊息
echo.

REM 切換到專案目錄
cd /d %~dp0

REM 啟動虛擬環境
echo [1/3] 啟動虛擬環境...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 虛擬環境啟動失敗
    pause
    exit /b 1
)
echo ✅ 虛擬環境已啟動
echo.

REM 檢查環境變數
echo [2/3] 檢查環境變數...
if not exist ".env" (
    echo ❌ 找不到 .env 檔案
    pause
    exit /b 1
)
echo ✅ .env 檔案存在
echo.

REM 啟動應用
echo [3/3] 啟動 Flask 應用...
echo.
echo ============================================================
echo 📊 應用程式日誌
echo ============================================================
echo.

python app.py

echo.
echo ============================================================
echo ⚠️ 應用程式已停止
echo ============================================================
echo.
pause
