@echo off
chcp 65001 >nul
title Agriculture Bot - ngrok Tunnel
echo ============================================================
echo 🌐 啟動 ngrok - 建立公開 URL
echo ============================================================
echo.
echo 📝 使用說明:
echo 1. ngrok 會建立一個公開的 HTTPS 網址
echo 2. 複製顯示的 Forwarding 網址（https://xxxx.ngrok-free.app）
echo 3. 前往 LINE Developers Console 更新 Webhook URL
echo 4. Webhook URL 格式: https://xxxx.ngrok-free.app/callback
echo.
echo ⚠️  注意: 免費版 ngrok 每次重啟網址會變動
echo    建議升級 ngrok Pro 取得固定網址（$8/月）
echo.
echo ============================================================
echo.

REM 檢查 ngrok 是否安裝
where ngrok >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ ngrok 已安裝在系統 PATH 中
    echo 🚀 正在啟動 ngrok tunnel...
    echo.
    ngrok http 5000
    goto :end
)

if exist "C:\ngrok\ngrok.exe" (
    echo ✅ 找到 ngrok: C:\ngrok\ngrok.exe
    echo 🚀 正在啟動 ngrok tunnel...
    echo.
    C:\ngrok\ngrok.exe http 5000
    goto :end
)

if exist "ngrok.exe" (
    echo ✅ 找到 ngrok: 專案目錄
    echo 🚀 正在啟動 ngrok tunnel...
    echo.
    ngrok.exe http 5000
    goto :end
)

echo ❌ 找不到 ngrok.exe
echo.
echo 📥 請先安裝 ngrok:
echo.
echo 方式 1 (推薦): 使用 Chocolatey
echo    choco install ngrok
echo.
echo 方式 2: 手動下載
echo    1. 前往 https://ngrok.com/download
echo    2. 註冊免費帳號
echo    3. 下載 Windows 版本
echo    4. 解壓縮到 C:\ngrok\ 或專案目錄
echo.
echo 方式 3: 使用 Scoop
echo    scoop install ngrok
echo.
echo 📖 詳細說明請參考: 本機執行指南.md
echo.
pause

:end
