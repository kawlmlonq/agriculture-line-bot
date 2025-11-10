@echo off
chcp 65001 >nul
title Agriculture Bot - 快速啟動
cls

echo ============================================================
echo 🌾 農業知識庫 LINE Bot - 快速啟動
echo ============================================================
echo.

REM 檢查虛擬環境
echo [1/4] 檢查虛擬環境...
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ 找不到虛擬環境！
    echo.
    echo 請先執行: python -m venv .venv
    echo 然後: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo ✅ 虛擬環境正常

REM 檢查 .env 檔案
echo [2/4] 檢查環境變數...
if not exist ".env" (
    echo ❌ 找不到 .env 檔案！
    echo.
    echo 請先複製 .env.example 為 .env 並填入設定
    echo.
    pause
    exit /b 1
)
echo ✅ .env 檔案存在

REM 檢查 Port 5000 是否被佔用
echo [3/4] 檢查 Port 5000...
netstat -ano | findstr :5000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 5000 已被使用
    echo.
    echo 請關閉佔用的程式或修改 .env 中的 PORT 設定
    echo.
    echo 查看佔用程式: netstat -ano ^| findstr :5000
    echo.
    choice /C YN /M "是否繼續啟動"
    if errorlevel 2 exit /b 1
)
echo ✅ Port 5000 可用

REM 啟動 Flask 伺服器
echo [4/4] 啟動 Flask 伺服器...
echo.
start "Agriculture Bot - Flask Server" cmd /k "title Agriculture Bot - Flask Server && chcp 65001 >nul && cd /d %~dp0 && call .venv\Scripts\activate.bat && echo 🚀 正在啟動 Flask 伺服器... && echo. && python app.py"

REM 等待伺服器啟動
echo ⏳ 等待伺服器啟動...
timeout /t 8 /nobreak >nul

REM 檢查伺服器是否成功啟動
echo.
echo 🔍 檢查伺服器狀態...
curl -s http://localhost:5000/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Flask 伺服器運行正常！
) else (
    echo ⚠️  伺服器可能還在啟動中...
    echo    請查看 Flask Server 視窗確認
)

echo.
echo ============================================================
echo 📊 系統狀態
echo ============================================================
echo.
echo ✅ Flask 伺服器已啟動
echo 📍 本地網址: http://localhost:5000
echo 📍 健康檢查: http://localhost:5000/health
echo.
echo ============================================================
echo 🌐 下一步: 啟動 ngrok
echo ============================================================
echo.
echo 請執行以下任一操作:
echo   1. 雙擊執行 啟動ngrok.bat
echo   2. 或手動執行: ngrok http 5000
echo.
echo 然後複製 ngrok 提供的 URL 更新到 LINE Console
echo.

pause
