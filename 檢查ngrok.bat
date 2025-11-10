@echo off
chcp 65001 >nul
title ngrok 設定檢查
cls

echo ============================================================
echo 🔍 ngrok 設定檢查
echo ============================================================
echo.

REM 檢查 ngrok 是否安裝
echo [1/3] 檢查 ngrok 安裝狀態...
where ngrok >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ ngrok 已安裝在系統 PATH 中
    ngrok version
) else if exist "C:\ngrok\ngrok.exe" (
    echo ✅ ngrok 已安裝在 C:\ngrok\
    C:\ngrok\ngrok.exe version
) else if exist "ngrok.exe" (
    echo ✅ ngrok 已安裝在專案目錄
    ngrok.exe version
) else (
    echo ❌ 未找到 ngrok
    echo.
    echo 請先安裝 ngrok:
    echo   方式 1: choco install ngrok
    echo   方式 2: https://ngrok.com/download
    echo.
    goto :end
)

echo.
echo [2/3] 檢查 ngrok 設定...

REM 檢查配置文件
set "CONFIG_PATH=%USERPROFILE%\.ngrok2\ngrok.yml"
if exist "%CONFIG_PATH%" (
    echo ✅ 找到設定檔: %CONFIG_PATH%
    
    REM 檢查是否有 authtoken
    findstr /C:"authtoken:" "%CONFIG_PATH%" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ authtoken 已設定
    ) else (
        echo ⚠️  未設定 authtoken
        echo.
        echo 請執行以下命令設定:
        echo   ngrok config add-authtoken YOUR_TOKEN_HERE
        echo.
        echo 從這裡取得 token: https://dashboard.ngrok.com/get-started/your-authtoken
    )
) else (
    echo ⚠️  未找到設定檔
    echo.
    echo 請先執行:
    echo   ngrok config add-authtoken YOUR_TOKEN_HERE
)

echo.
echo [3/3] 檢查本機應用程式...

REM 檢查 Port 5000
netstat -ano | findstr :5000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ 應用程式正在 Port 5000 運行
) else (
    echo ⚠️  Port 5000 未使用
    echo 請先啟動應用程式: 快速啟動.bat
)

echo.
echo ============================================================
echo 📋 總結
echo ============================================================
echo.
echo 如果所有檢查都通過，您可以:
echo 1. 執行 .\啟動ngrok.bat 啟動 tunnel
echo 2. 複製 Forwarding 網址
echo 3. 更新 LINE Developers Console 的 Webhook URL
echo.
echo 需要幫助？參考: 本機執行指南.md
echo.

:end
pause
