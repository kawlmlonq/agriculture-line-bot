@echo off
chcp 65001 >nul
title LINE Bot 連線診斷
cls

echo ============================================================
echo 🔍 LINE Bot 連線診斷工具
echo ============================================================
echo.
echo 此工具將檢查 LINE Bot 無法回應的所有可能原因
echo.

REM 步驟 1: 檢查本地應用程式
echo [1/6] 檢查本地應用程式...
curl -s http://localhost:5000/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ 本地應用程式運行中
    curl -s http://localhost:5000/health
    echo.
) else (
    echo ❌ 本地應用程式未運行
    echo.
    echo 💡 解決方法:
    echo    請先執行: 快速啟動.bat 或 手動啟動.bat
    echo.
    pause
    exit /b 1
)

REM 步驟 2: 檢查 ngrok
echo [2/6] 檢查 ngrok 狀態...
curl -s http://localhost:4040/api/tunnels >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ ngrok 運行中
    echo.
    echo 📍 ngrok 公開網址:
    curl -s http://localhost:4040/api/tunnels | findstr "public_url"
    echo.
) else (
    echo ❌ ngrok 未運行
    echo.
    echo 💡 解決方法:
    echo    請執行: 啟動ngrok.bat
    echo.
    pause
    exit /b 1
)

REM 步驟 3: 檢查 .env 設定
echo [3/6] 檢查環境變數設定...
findstr /C:"LINE_CHANNEL_ACCESS_TOKEN=" .env >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ LINE_CHANNEL_ACCESS_TOKEN 已設定
) else (
    echo ❌ LINE_CHANNEL_ACCESS_TOKEN 未設定
)

findstr /C:"LINE_CHANNEL_SECRET=" .env >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ LINE_CHANNEL_SECRET 已設定
) else (
    echo ❌ LINE_CHANNEL_SECRET 未設定
)

findstr /C:"GROQ_API_KEY=" .env >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ GROQ_API_KEY 已設定
) else (
    echo ❌ GROQ_API_KEY 未設定
)
echo.

REM 步驟 4: 檢查最近的請求
echo [4/6] 檢查最近的 LINE 請求...
echo.
echo 請查看應用程式視窗是否有以下訊息:
echo   - POST /callback - 表示收到 LINE 訊息
echo   - 200 - 表示成功回應
echo   - 4xx/5xx - 表示有錯誤
echo.

REM 步驟 5: 顯示 ngrok Web Interface
echo [5/6] ngrok 監控面板...
echo.
echo 💡 開啟瀏覽器訪問以下網址查看詳細日誌:
echo    http://localhost:4040
echo.
echo 在這裡可以看到:
echo   • 所有 HTTP 請求
echo   • LINE 傳送的完整資料
echo   • 您的應用回應內容
echo   • 任何錯誤訊息
echo.

REM 步驟 6: LINE Webhook 設定檢查清單
echo [6/6] LINE Developers Console 檢查清單...
echo.
echo 請確認以下設定:
echo.
echo □ 已登入 LINE Developers Console
echo   https://developers.line.biz/console/
echo.
echo □ Webhook URL 已設定
echo   格式: https://xxxx.ngrok-free.app/callback
echo   (必須以 /callback 結尾)
echo.
echo □ 已點擊 "Verify" 按鈕驗證
echo   ✅ Success - 設定正確
echo   ❌ Failed - 請檢查網址或應用程式
echo.
echo □ "Use webhook" 開關已開啟
echo   OFF → ON
echo.
echo □ "Auto-reply messages" 已關閉 (Optional)
echo   ON → OFF (避免重複回應)
echo.

echo ============================================================
echo 🔧 常見問題和解決方案
echo ============================================================
echo.
echo 問題 1: ngrok 網址改變了
echo   原因: 免費版 ngrok 每次重啟網址都會變
echo   解決: 重新複製新的 ngrok 網址到 LINE Console
echo.
echo 問題 2: Webhook 驗證失敗
echo   原因: 本地應用程式未運行或 ngrok 未連接
echo   解決: 確保兩者都在運行，然後重新驗證
echo.
echo 問題 3: 有收到請求但無回應
echo   原因: API Key 錯誤或向量資料庫問題
echo   解決: 檢查應用程式視窗的錯誤訊息
echo.
echo 問題 4: 完全無請求
echo   原因: Webhook URL 設定錯誤或未開啟
echo   解決: 確認 LINE Console 設定正確
echo.

echo ============================================================
echo 📋 快速檢查步驟
echo ============================================================
echo.
echo 1️⃣  本地應用程式運行? → 應用程式視窗應該開著
echo 2️⃣  ngrok 運行? → ngrok 視窗應該開著
echo 3️⃣  取得 ngrok URL → 從 ngrok 視窗複製
echo 4️⃣  更新 LINE Webhook → 加上 /callback
echo 5️⃣  驗證成功? → 點擊 Verify 按鈕
echo 6️⃣  開關開啟? → Use webhook = ON
echo 7️⃣  傳送測試訊息 → 發送 "你好"
echo 8️⃣  查看 ngrok 監控 → http://localhost:4040
echo.

echo ============================================================
echo.
pause

REM 開啟 ngrok web interface
choice /C YN /M "是否開啟 ngrok 監控面板"
if errorlevel 2 goto :end
start http://localhost:4040

:end
