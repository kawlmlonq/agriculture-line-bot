@echo off
echo ========================================
echo 農業知識庫 LINE Bot - 快速啟動
echo ========================================
echo.

REM 檢查 Python 服務是否運行
echo [1/2] 檢查 Python 服務...
powershell -Command "$process = Get-Process python -ErrorAction SilentlyContinue; if ($process) { Write-Host '   ✓ Python 服務正在運行' -ForegroundColor Green } else { Write-Host '   ✗ Python 服務未運行，正在啟動...' -ForegroundColor Yellow; Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd C:\line_ai; python app.py' }"

echo.
echo [2/2] 檢查 ngrok...

REM 檢查 ngrok 是否存在
if exist "C:\ngrok\ngrok.exe" (
    echo    ✓ 找到 ngrok
    echo.
    echo 是否要啟動 ngrok? (Y/N)
    set /p start_ngrok=
    if /i "%start_ngrok%"=="Y" (
        echo    正在啟動 ngrok...
        start powershell -NoExit -Command "cd C:\ngrok; .\ngrok.exe http 5000"
        echo    ✓ ngrok 已在新視窗啟動
    )
) else (
    echo    ✗ 找不到 ngrok
    echo.
    echo 請依照以下步驟安裝 ngrok:
    echo 1. 前往: https://ngrok.com/download
    echo 2. 下載 Windows 版本
    echo 3. 解壓縮到 C:\ngrok\
    echo 4. 重新執行此腳本
)

echo.
echo ========================================
echo 下一步:
echo ========================================
echo 1. 複製 ngrok 顯示的 HTTPS 網址
echo 2. 前往 LINE Developers Console
echo 3. 設定 Webhook URL (網址/callback)
echo 4. 加入 Bot 為好友並測試
echo.
echo 詳細說明請參考: NGROK_SETUP.md
echo ========================================
pause
