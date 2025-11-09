@echo off
chcp 65001 > nul
echo ============================================================
echo 農業知識庫 LINE Bot - 完整啟動
echo ============================================================
echo.

echo [1/3] 啟動虛擬環境...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 虛擬環境啟動失敗
    pause
    exit /b 1
)
echo ✅ 虛擬環境已啟動
echo.

echo [2/3] 檢查套件...
python -c "import flask, chromadb, groq, sentence_transformers; print('✅ 所有套件已安裝')" 2>nul
if errorlevel 1 (
    echo ⚠️  缺少套件，正在安裝...
    pip install -r requirements.txt
)
echo.

echo [3/3] 啟動應用程式...
echo.
echo ⏳ 首次啟動可能需要 30-60 秒載入 AI 模型，請耐心等待...
echo.
python app.py

pause
