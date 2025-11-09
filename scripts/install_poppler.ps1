# PowerShell script: Auto-download and setup Poppler
# For PDF to image conversion

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Poppler Auto-Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set paths
$installDir = "$PSScriptRoot\..\poppler"
$downloadUrl = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
$zipFile = "$env:TEMP\poppler.zip"

# Check if already installed
if (Test-Path "$installDir\Library\bin\pdfinfo.exe") {
    Write-Host "Poppler already installed!" -ForegroundColor Green
    Write-Host "Location: $installDir" -ForegroundColor Gray
    
    $response = Read-Host "Reinstall? (y/n)"
    if ($response -ne "y") {
        Write-Host "Cancelled" -ForegroundColor Yellow
        exit 0
    }
    
    Write-Host "Removing old version..." -ForegroundColor Yellow
    Remove-Item -Path $installDir -Recurse -Force
}

# Create directory
Write-Host "Creating installation directory..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $installDir -Force | Out-Null

# Download Poppler
Write-Host "Downloading Poppler..." -ForegroundColor Cyan
Write-Host "Source: $downloadUrl" -ForegroundColor Gray
try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile -UseBasicParsing
    Write-Host "Download complete!" -ForegroundColor Green
} catch {
    Write-Host "Download failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please download manually:" -ForegroundColor Yellow
    Write-Host $downloadUrl -ForegroundColor Gray
    Write-Host "Extract to: $installDir" -ForegroundColor Gray
    exit 1
}

# Extract
Write-Host "Extracting..." -ForegroundColor Cyan
try {
    Expand-Archive -Path $zipFile -DestinationPath $installDir -Force
    Write-Host "Extraction complete!" -ForegroundColor Green
} catch {
    Write-Host "Extraction failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# Cleanup
Write-Host "Cleaning up temp files..." -ForegroundColor Cyan
Remove-Item -Path $zipFile -Force

# Set environment variable (current session only)
$popplerBin = "$installDir\Library\bin"
$env:PATH = "$popplerBin;$env:PATH"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Poppler location: $popplerBin" -ForegroundColor Gray
Write-Host ""

# Test
Write-Host "Testing Poppler..." -ForegroundColor Cyan
try {
    $version = & "$popplerBin\pdfinfo.exe" -v 2>&1
    Write-Host "Poppler version: $version" -ForegroundColor Green
} catch {
    Write-Host "Test failed, but files are installed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Notes:" -ForegroundColor Yellow
Write-Host "1. Environment variable set (current session only)" -ForegroundColor Gray
Write-Host "2. OCR script will auto-detect Poppler" -ForegroundColor Gray
Write-Host "3. For permanent setup, run install_ocr.bat" -ForegroundColor Gray
Write-Host ""
