@echo off
chcp 65001 >nul
title 系統診斷工具
cls

echo ============================================================
echo 🔍 系統診斷工具
echo ============================================================
echo.
echo 正在檢查系統狀態...
echo.

REM 創建日誌檔案
set LOG_FILE=診斷報告_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
set LOG_FILE=%LOG_FILE: =0%

echo 診斷報告 - %date% %time% > %LOG_FILE%
echo ============================================================ >> %LOG_FILE%
echo. >> %LOG_FILE%

REM 1. 檢查 Python
echo [1/10] 檢查 Python 版本...
python --version >> %LOG_FILE% 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Python 已安裝
    python --version
) else (
    echo ❌ Python 未安裝或不在 PATH 中
    echo ❌ Python 未安裝或不在 PATH 中 >> %LOG_FILE%
)
echo. >> %LOG_FILE%

REM 2. 檢查虛擬環境
echo [2/10] 檢查虛擬環境...
if exist ".venv\Scripts\activate.bat" (
    echo ✅ 虛擬環境存在
    echo ✅ 虛擬環境存在 >> %LOG_FILE%
    
    REM 檢查虛擬環境中的 Python
    .\.venv\Scripts\python.exe --version >> %LOG_FILE% 2>&1
) else (
    echo ❌ 虛擬環境不存在
    echo ❌ 虛擬環境不存在 >> %LOG_FILE%
)
echo. >> %LOG_FILE%

REM 3. 檢查 .env 檔案
echo [3/10] 檢查環境變數檔案...
if exist ".env" (
    echo ✅ .env 檔案存在
    echo ✅ .env 檔案存在 >> %LOG_FILE%
    
    REM 檢查必要設定（不顯示實際值）
    findstr /C:"LINE_CHANNEL_ACCESS_TOKEN=" .env >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   ✅ LINE_CHANNEL_ACCESS_TOKEN 已設定
    ) else (
        echo   ❌ LINE_CHANNEL_ACCESS_TOKEN 未設定
    )
    
    findstr /C:"LINE_CHANNEL_SECRET=" .env >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   ✅ LINE_CHANNEL_SECRET 已設定
    ) else (
        echo   ❌ LINE_CHANNEL_SECRET 未設定
    )
    
    findstr /C:"GROQ_API_KEY=" .env >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   ✅ GROQ_API_KEY 已設定
    ) else (
        echo   ❌ GROQ_API_KEY 未設定
    )
) else (
    echo ❌ .env 檔案不存在
    echo ❌ .env 檔案不存在 >> %LOG_FILE%
)
echo. >> %LOG_FILE%

REM 4. 檢查必要檔案
echo [4/10] 檢查必要檔案...
set FILES_OK=1
if exist "app.py" (
    echo ✅ app.py
) else (
    echo ❌ app.py 不存在
    set FILES_OK=0
)

if exist "config.py" (
    echo ✅ config.py
) else (
    echo ❌ config.py 不存在
    set FILES_OK=0
)

if exist "requirements.txt" (
    echo ✅ requirements.txt
) else (
    echo ❌ requirements.txt 不存在
    set FILES_OK=0
)

if %FILES_OK% EQU 1 (
    echo ✅ 所有必要檔案存在 >> %LOG_FILE%
) else (
    echo ❌ 部分檔案遺失 >> %LOG_FILE%
)
echo. >> %LOG_FILE%

REM 5. 檢查 Python 套件
echo [5/10] 檢查 Python 套件...
if exist ".venv\Scripts\python.exe" (
    echo 檢查已安裝的套件... >> %LOG_FILE%
    .\.venv\Scripts\python.exe -m pip list >> %LOG_FILE% 2>&1
    
    .\.venv\Scripts\python.exe -c "import flask" 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Flask
    ) else (
        echo ❌ Flask 未安裝
    )
    
    .\.venv\Scripts\python.exe -c "import groq" 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Groq
    ) else (
        echo ❌ Groq 未安裝
    )
    
    .\.venv\Scripts\python.exe -c "import chromadb" 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ ChromaDB
    ) else (
        echo ❌ ChromaDB 未安裝
    )
    
    .\.venv\Scripts\python.exe -c "from linebot.v3 import WebhookHandler" 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ LINE Bot SDK
    ) else (
        echo ❌ LINE Bot SDK 未安裝
    )
)
echo. >> %LOG_FILE%

REM 6. 檢查向量資料庫
echo [6/10] 檢查向量資料庫...
if exist "vector_db" (
    echo ✅ vector_db 資料夾存在
    echo ✅ vector_db 資料夾存在 >> %LOG_FILE%
    
    REM 計算資料夾大小
    for /f "tokens=3" %%a in ('dir /s "vector_db" ^| find "個檔案"') do (
        echo   檔案總數: %%a
    )
) else (
    echo ❌ vector_db 資料夾不存在
    echo ❌ vector_db 資料夾不存在 >> %LOG_FILE%
    echo   請執行: python scripts\load_data.py
)
echo. >> %LOG_FILE%

REM 7. 檢查資料檔案
echo [7/10] 檢查資料檔案...
if exist "data\agriculture" (
    echo ✅ data\agriculture 資料夾存在
    echo ✅ data\agriculture 資料夾存在 >> %LOG_FILE%
    
    REM 列出檔案
    dir /b "data\agriculture\*.pdf" "data\agriculture\*.txt" 2>nul | find /c /v "" > temp_count.txt
    set /p FILE_COUNT=<temp_count.txt
    del temp_count.txt
    
    echo   資料檔案數: %FILE_COUNT%
    echo   資料檔案數: %FILE_COUNT% >> %LOG_FILE%
) else (
    echo ❌ data\agriculture 資料夾不存在
    echo ❌ data\agriculture 資料夾不存在 >> %LOG_FILE%
)
echo. >> %LOG_FILE%

REM 8. 檢查 Port 5000
echo [8/10] 檢查 Port 5000...
netstat -ano | findstr :5000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 5000 已被佔用
    echo ⚠️  Port 5000 已被佔用 >> %LOG_FILE%
    echo.
    echo 佔用 Port 5000 的程式: >> %LOG_FILE%
    netstat -ano | findstr :5000 >> %LOG_FILE%
) else (
    echo ✅ Port 5000 可用
    echo ✅ Port 5000 可用 >> %LOG_FILE%
)
echo. >> %LOG_FILE%

REM 9. 檢查記憶體
echo [9/10] 檢查系統資源...
echo 系統資源: >> %LOG_FILE%
systeminfo | findstr /C:"可用的實體記憶體" >> %LOG_FILE% 2>&1
wmic cpu get loadpercentage >> %LOG_FILE% 2>&1
echo ✅ 系統資源檢查完成
echo. >> %LOG_FILE%

REM 10. 測試啟動
echo [10/10] 測試應用程式啟動...
if exist ".venv\Scripts\python.exe" (
    echo 嘗試載入主程式... >> %LOG_FILE%
    .\.venv\Scripts\python.exe -c "import app; print('✅ app.py 可以載入')" 2>> %LOG_FILE%
    if %ERRORLEVEL% EQU 0 (
        echo ✅ app.py 語法正常
    ) else (
        echo ❌ app.py 載入失敗（請查看日誌）
    )
)
echo. >> %LOG_FILE%

echo.
echo ============================================================
echo 📊 診斷完成
echo ============================================================
echo.
echo 診斷報告已儲存至: %LOG_FILE%
echo.
echo 如果發現問題，請根據以上檢查結果修正。
echo 常見問題修正:
echo   1. Python 套件未安裝: pip install -r requirements.txt
echo   2. .env 未設定: 複製 .env.example 並填入設定
echo   3. 向量資料庫未建立: python scripts\load_data.py
echo   4. Port 被佔用: 修改 .env 中的 PORT 設定
echo.
pause
