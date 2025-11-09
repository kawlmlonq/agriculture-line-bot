@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    OCR System Installation
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment!
    echo Please run setup.ps1 first
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM Install Python packages
echo ========================================
echo Installing Python packages...
echo ========================================
echo.

echo Installing pytesseract...
pip install pytesseract
if errorlevel 1 (
    echo Failed to install pytesseract!
    pause
    exit /b 1
)

echo Installing pdf2image...
pip install pdf2image
if errorlevel 1 (
    echo Failed to install pdf2image!
    pause
    exit /b 1
)

echo Installing Pillow...
pip install Pillow
if errorlevel 1 (
    echo Failed to install Pillow!
    pause
    exit /b 1
)

echo Installing reportlab...
pip install reportlab
if errorlevel 1 (
    echo Failed to install reportlab!
    pause
    exit /b 1
)

echo.
echo Python packages installed!
echo.

REM Install Poppler
echo ========================================
echo Installing Poppler...
echo ========================================
echo.

powershell -ExecutionPolicy Bypass -File scripts\install_poppler.ps1
if errorlevel 1 (
    echo Poppler installation failed!
    echo You may need to install manually
)

echo.

REM Install Tesseract
echo ========================================
echo Installing Tesseract OCR...
echo ========================================
echo.

REM Check if Tesseract is already installed
where tesseract >nul 2>&1
if %errorlevel% equ 0 (
    echo Tesseract is already installed!
    tesseract --version
    echo.
) else (
    echo Tesseract not found. Installing...
    echo.
    
    REM Check if Chocolatey is available
    where choco >nul 2>&1
    if %errorlevel% equ 0 (
        echo Installing Tesseract via Chocolatey...
        choco install tesseract -y
        if errorlevel 1 (
            echo Chocolatey installation failed!
            goto manual_tesseract
        )
        echo Tesseract installed via Chocolatey!
    ) else (
        :manual_tesseract
        echo.
        echo Chocolatey not found. Please install Tesseract manually:
        echo.
        echo 1. Visit: https://github.com/UB-Mannheim/tesseract/wiki
        echo 2. Download: tesseract-ocr-w64-setup-vX.X.X.exe
        echo 3. Install and select Traditional Chinese language pack
        echo 4. Add Tesseract to system PATH
        echo.
        echo After installation, re-run this script.
        pause
        exit /b 1
    )
)

REM Download Traditional Chinese language data
echo ========================================
echo Downloading Traditional Chinese data...
echo ========================================
echo.

set TESSDATA_DIR=%LOCALAPPDATA%\Tesseract-OCR\tessdata
if not exist "%TESSDATA_DIR%" (
    mkdir "%TESSDATA_DIR%"
)

echo Downloading chi_tra.traineddata...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tessdata_best/raw/main/chi_tra.traineddata' -OutFile '%TESSDATA_DIR%\chi_tra.traineddata'"
if errorlevel 1 (
    echo Failed to download chi_tra.traineddata
    echo Please download manually from:
    echo https://github.com/tesseract-ocr/tessdata_best/raw/main/chi_tra.traineddata
    echo And save to: %TESSDATA_DIR%
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Close and reopen your terminal
echo 2. Run: python scripts\ocr_pdf.py
echo.
pause
