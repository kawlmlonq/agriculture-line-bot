@echo off
chcp 65001 >nul
echo ========================================
echo    System Status Check
echo ========================================
echo.

REM Check if Flask is running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Flask Server: Running
) else (
    echo [X] Flask Server: Not Running
)

REM Check if ngrok is running
tasklist /FI "IMAGENAME eq ngrok.exe" 2>NUL | find /I /N "ngrok.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] ngrok: Running
) else (
    echo [X] ngrok: Not Running
)

echo.
echo Testing Flask health endpoint...
echo.

curl -s http://localhost:5000/health 2>nul
if "%ERRORLEVEL%"=="0" (
    echo.
    echo.
    echo [OK] Flask Server: READY!
    echo.
    echo You can now test your LINE Bot!
) else (
    echo [WAIT] Flask Server: Still loading models...
    echo.
    echo This is normal. AI models take 1-2 minutes to load.
    echo Please wait and run this script again in 30 seconds.
)

echo.
echo ========================================
echo Current Knowledge Base:
echo ========================================
echo - Water Rice Cultivation (40 chunks)
echo - Corn Planting (35 chunks)
echo - Tomato Cultivation (50 chunks) [NEW!]
echo.
echo Total: 125 document chunks
echo.
pause
