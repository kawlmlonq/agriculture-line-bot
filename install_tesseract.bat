@echo off
chcp 65001 >nul
echo ========================================
echo    Tesseract OCR Manual Setup Guide
echo ========================================
echo.
echo Step 1: Download Tesseract
echo ----------------------------------------
echo.
echo Visit: https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Or use direct link:
echo https://github.com/UB-Mannheim/tesseract/releases
echo.
echo Download: tesseract-ocr-w64-setup-5.X.X.XXXXXXXX.exe
echo.
pause
echo.
echo Step 2: Install Tesseract
echo ----------------------------------------
echo.
echo 1. Run the downloaded .exe file
echo 2. During installation, make sure to:
echo    - Check "Additional language data"
echo    - Select "Traditional Chinese" (chi_tra)
echo 3. Note the installation path (default: C:\Program Files\Tesseract-OCR)
echo 4. Add to PATH when prompted (recommended)
echo.
pause
echo.
echo Step 3: Verify Installation
echo ----------------------------------------
echo.
tesseract --version 2>nul
if errorlevel 1 (
    echo Tesseract NOT found!
    echo.
    echo Please add Tesseract to your system PATH:
    echo 1. Press Win + X, select "System"
    echo 2. Click "Advanced system settings"
    echo 3. Click "Environment Variables"
    echo 4. In "System variables", find "Path", click "Edit"
    echo 5. Click "New" and add: C:\Program Files\Tesseract-OCR
    echo 6. Click OK and restart this terminal
) else (
    echo.
    echo Tesseract installed successfully!
    echo.
    echo ========================================
    echo    Setup Complete!
    echo ========================================
    echo.
    echo You can now use the OCR tools:
    echo - Run: OCR處理.bat
    echo - Or: python scripts\simple_ocr.py
)
echo.
pause
