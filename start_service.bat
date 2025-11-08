@echo off
chcp 65001 > nul
echo ============================================================
echo 🌾 農業知識庫 LINE Bot - 啟動服務
echo ============================================================
echo.

echo 正在啟動服務...
cd /d "%~dp0"
start "LINE Bot Service" python app.py

echo.
echo ✅ 服務已在背景啟動
echo.
echo 請等待 10 秒讓服務完全啟動...
timeout /t 10 /nobreak > nul
echo.
echo 測試服務健康狀態...
powershell -Command "try { $result = Invoke-RestMethod -Uri 'http://localhost:5000/health'; Write-Host '✓ 服務運行正常' -ForegroundColor Green; Write-Host '  文件數量:' $result.vector_db.documents -ForegroundColor Cyan } catch { Write-Host '✗ 服務啟動失敗' -ForegroundColor Red }"
echo.
echo ============================================================
echo 接下來的步驟：
echo ============================================================
echo.
echo 1. 安裝 ngrok (如果尚未安裝)
echo    - 下載: https://ngrok.com/download
echo    - 解壓到: C:\ngrok\
echo    - 設定 authtoken
echo.
echo 2. 啟動 ngrok:
echo    開啟新的 PowerShell 視窗，執行：
echo    cd C:\ngrok
echo    .\ngrok.exe http 5000
echo.
echo 3. 複製 ngrok 顯示的 HTTPS URL
echo.
echo 4. 設定 LINE Webhook:
echo    - 登入: https://developers.line.biz/console/
echo    - 選擇你的 Channel
echo    - Messaging API 頁籤 -^> Webhook settings
echo    - 輸入: https://[你的ngrok網址]/callback
echo    - 點擊 Update 和 Verify
echo    - 啟用 "Use webhook"
echo.
echo 5. 測試 Bot:
echo    - 掃描 QR code 加入好友
echo    - 傳送訊息測試，例如:
echo      • 水稻什麼時候種植？
echo      • 有機肥料有哪些種類？
echo      • /help
echo.
echo ============================================================
pause
