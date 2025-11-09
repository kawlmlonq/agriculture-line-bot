@echo off
chcp 65001 > nul
cls
echo.
echo ============================================================
echo   🌾 農業知識庫 LINE Bot - 啟動中
echo ============================================================
echo.
echo ⚠️  重要提示：
echo    首次啟動需要 1-2 分鐘載入 AI 模型
echo    請耐心等待，不要關閉視窗！
echo.
echo ============================================================
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat

echo 正在啟動伺服器...
echo.
python app.py

pause
