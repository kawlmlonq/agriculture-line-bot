@echo off
echo ============================================================
echo 啟動 ngrok - 建立公開 URL
echo ============================================================
echo.

if exist "C:\ngrok\ngrok.exe" (
    echo 正在啟動 ngrok...
    echo.
    C:\ngrok\ngrok.exe http 5000
) else if exist "ngrok.exe" (
    echo 正在啟動 ngrok...
    echo.
    ngrok.exe http 5000
) else (
    echo ❌ 找不到 ngrok.exe
    echo.
    echo 請先安裝 ngrok:
    echo 1. 前往 https://ngrok.com/download
    echo 2. 下載 Windows 版本
    echo 3. 解壓縮到專案目錄或 C:\ngrok\
    echo.
    pause
)
