@echo off
chcp 65001 >nul
title 測試啟動腳本
cls

echo ============================================================
echo 🧪 測試啟動腳本
echo ============================================================
echo.

REM 測試 1: 檢查腳本文件存在
echo [測試 1/8] 檢查腳本文件...
set PASS_COUNT=0
set TOTAL_COUNT=8

if exist "快速啟動.bat" (
    echo ✅ 快速啟動.bat 存在
    set /a PASS_COUNT+=1
) else (
    echo ❌ 快速啟動.bat 不存在
)

if exist "手動啟動.bat" (
    echo ✅ 手動啟動.bat 存在
    set /a PASS_COUNT+=1
) else (
    echo ❌ 手動啟動.bat 不存在
)
echo.

REM 測試 2: 檢查虛擬環境
echo [測試 2/8] 檢查虛擬環境...
if exist ".venv\Scripts\activate.bat" (
    echo ✅ 虛擬環境存在
    set /a PASS_COUNT+=1
) else (
    echo ❌ 虛擬環境不存在
)
echo.

REM 測試 3: 檢查 .env
echo [測試 3/8] 檢查環境變數文件...
if exist ".env" (
    echo ✅ .env 文件存在
    set /a PASS_COUNT+=1
) else (
    echo ❌ .env 文件不存在
)
echo.

REM 測試 4: 檢查必要檔案
echo [測試 4/8] 檢查應用程式文件...
if exist "app.py" (
    echo ✅ app.py 存在
    set /a PASS_COUNT+=1
) else (
    echo ❌ app.py 不存在
)
echo.

REM 測試 5: 測試虛擬環境啟動
echo [測試 5/8] 測試虛擬環境啟動...
call .venv\Scripts\activate.bat >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ 虛擬環境可以啟動
    set /a PASS_COUNT+=1
) else (
    echo ❌ 虛擬環境啟動失敗
)
echo.

REM 測試 6: 測試 Python 套件
echo [測試 6/8] 測試關鍵套件...
python -c "import flask, groq, chromadb; print('✅ 所有關鍵套件可用')" 2>nul
if %ERRORLEVEL% EQU 0 (
    set /a PASS_COUNT+=1
) else (
    echo ❌ 部分套件無法載入
)
echo.

REM 測試 7: 測試 Port 5000
echo [測試 7/8] 檢查 Port 5000...
netstat -ano | findstr :5000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 5000 目前被佔用（這可能是正常的）
    echo    如果您的應用正在運行，這是正常的
) else (
    echo ✅ Port 5000 可用
    set /a PASS_COUNT+=1
)
echo.

REM 測試 8: 模擬啟動（載入模組）
echo [測試 8/8] 測試應用程式模組載入...
python -c "from src.vector_store import VectorStore; print('✅ VectorStore 可以載入')" 2>nul
if %ERRORLEVEL% EQU 0 (
    set /a PASS_COUNT+=1
) else (
    echo ❌ VectorStore 載入失敗
)
echo.

REM 顯示結果
echo ============================================================
echo 📊 測試結果
echo ============================================================
echo.
echo 通過: %PASS_COUNT%/%TOTAL_COUNT%
echo.

if %PASS_COUNT% EQU %TOTAL_COUNT% (
    echo ✅✅✅ 所有測試通過！ ✅✅✅
    echo.
    echo 🎉 快速啟動和手動啟動都應該可以正常使用！
    echo.
    echo 建議操作:
    echo   1. 使用 快速啟動.bat - 自動開啟 Flask 視窗
    echo   2. 使用 手動啟動.bat - 在當前視窗查看日誌
) else if %PASS_COUNT% GEQ 6 (
    echo ✅ 大部分測試通過
    echo.
    echo ⚠️  有少數問題，但應該可以運行
    echo    請查看上方的測試結果
) else (
    echo ❌ 測試未通過
    echo.
    echo 請檢查以下項目:
    echo   1. 虛擬環境是否正確安裝
    echo   2. .env 文件是否存在並設定正確
    echo   3. Python 套件是否完整安裝
    echo.
    echo 建議執行: 重新安裝套件.bat
)

echo.
echo ============================================================
echo 🔧 快速修正指令
echo ============================================================
echo.
echo 如果測試失敗，請依序執行:
echo   1. 重新安裝套件.bat      - 修正套件問題
echo   2. python scripts\load_data.py  - 重建向量資料庫
echo   3. 再次執行本測試
echo.
pause
