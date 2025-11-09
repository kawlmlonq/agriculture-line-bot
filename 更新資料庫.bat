@echo off
chcp 65001 >nul
cls
echo.
echo ============================================================
echo   Smart Update - Agriculture Knowledge Base
echo ============================================================
echo.
echo   Features:
echo      - Auto detect new/modified files
echo      - Skip unchanged files
echo      - Track file processing status
echo.
echo ============================================================
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat

python scripts\smart_load_data.py

echo.
echo ============================================================
echo  更新完成！
echo ============================================================
echo.
echo 💡 下一步：重啟伺服器讓更新生效
echo    執行：.\RUN.bat
echo.
echo 💡 舊版載入方式（不使用智能判斷）：
echo    python scripts\load_data.py
echo.
pause
