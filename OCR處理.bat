@echo off
chcp 65001 >nul
echo ========================================
echo    OCR PDF Tool
echo ========================================
echo.

REM Set Tesseract path
set "PATH=C:\Program Files\Tesseract-OCR;%PATH%"

REM Set Poppler path (check multiple possible locations)
if exist "%~dp0poppler\poppler-24.08.0\Library\bin" (
    set "PATH=%~dp0poppler\poppler-24.08.0\Library\bin;%PATH%"
) else if exist "%~dp0poppler\Library\bin" (
    set "PATH=%~dp0poppler\Library\bin;%PATH%"
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting OCR...
echo.

python scripts\simple_ocr.py

echo.
pause
