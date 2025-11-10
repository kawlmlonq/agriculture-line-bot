@echo off
chcp 65001 >nul
title 重新安裝套件
cls

echo ============================================================
echo 🔧 重新安裝 Python 套件
echo ============================================================
echo.
echo 這將重新安裝所有必要的 Python 套件
echo 以修正可能的版本衝突或安裝問題
echo.
pause
echo.

REM 啟動虛擬環境
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 無法啟動虛擬環境
    echo.
    echo 請先創建虛擬環境:
    echo   python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo ✅ 虛擬環境已啟動
echo.

echo [1/3] 更新 pip...
python -m pip install --upgrade pip
echo.

echo [2/3] 安裝/更新套件...
pip install --upgrade -r requirements.txt
echo.

echo [3/3] 驗證關鍵套件...
echo.
python -c "import flask; print(f'✅ Flask {flask.__version__}')"
python -c "import groq; print('✅ Groq OK')"
python -c "import chromadb; print(f'✅ ChromaDB {chromadb.__version__}')"
python -c "from linebot.v3 import WebhookHandler; print('✅ LINE Bot SDK OK')"
python -c "from sentence_transformers import SentenceTransformer; print('✅ Sentence Transformers OK')"

echo.
echo ============================================================
echo ✅ 套件安裝完成
echo ============================================================
echo.
echo 現在可以執行 快速啟動.bat 或 手動啟動.bat
echo.
pause
