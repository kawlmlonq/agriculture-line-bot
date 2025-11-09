@echo off
chcp 65001 >nul
echo ============================================================
echo  農業知識庫 LINE Bot - 快速啟動
echo ============================================================
echo.

echo [1/2] 啟動 Flask 伺服器...
start "Flask Server" cmd /k "chcp 65001 && cd /d %~dp0 && .venv\Scripts\activate.bat && python app.py"

echo [2/2] 等待伺服器啟動...
timeout /t 5 /nobreak >nul

echo 啟動 ngrok...
start "ngrok" cmd /k "chcp 65001 && ngrok http 5000"

echo.
echo ============================================================
echo  啟動完成！
echo ============================================================
echo.
echo  請等待 30 秒讓伺服器完全啟動
echo  然後從 ngrok 視窗複製 URL 設定到 LINE Console
echo.
pause
