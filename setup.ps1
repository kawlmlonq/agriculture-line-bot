# 快速啟動腳本
# 自動設定虛擬環境並安裝套件

Write-Host "================================" -ForegroundColor Green
Write-Host "農業知識庫 LINE Bot - 快速設定" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# 檢查 Python 是否安裝
Write-Host "檢查 Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ 找到 Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 找不到 Python，請先安裝 Python 3.8 或更新版本" -ForegroundColor Red
    exit 1
}

# 建立虛擬環境
if (!(Test-Path "venv")) {
    Write-Host ""
    Write-Host "建立虛擬環境..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ 虛擬環境建立完成" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✓ 虛擬環境已存在" -ForegroundColor Green
}

# 啟動虛擬環境
Write-Host ""
Write-Host "啟動虛擬環境..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# 升級 pip
Write-Host ""
Write-Host "升級 pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# 安裝套件
Write-Host ""
Write-Host "安裝套件（這可能需要幾分鐘）..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 套件安裝完成" -ForegroundColor Green
} else {
    Write-Host "✗ 套件安裝失敗" -ForegroundColor Red
    exit 1
}

# 檢查 .env 檔案
Write-Host ""
if (!(Test-Path ".env")) {
    Write-Host "建立 .env 檔案..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ 已建立 .env 檔案，請編輯此檔案填入你的設定" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "需要填入的資訊：" -ForegroundColor Cyan
    Write-Host "  - LINE_CHANNEL_ACCESS_TOKEN" -ForegroundColor Cyan
    Write-Host "  - LINE_CHANNEL_SECRET" -ForegroundColor Cyan
    Write-Host "  - OPENAI_API_KEY" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "✓ .env 檔案已存在" -ForegroundColor Green
}

# 檢查資料資料夾
Write-Host ""
if (!(Test-Path "data\agriculture")) {
    Write-Host "建立資料資料夾..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "data\agriculture" -Force | Out-Null
    Write-Host "✓ 已建立資料資料夾" -ForegroundColor Green
} else {
    Write-Host "✓ 資料資料夾已存在" -ForegroundColor Green
}

# 完成
Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "設定完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步：" -ForegroundColor Cyan
Write-Host "1. 編輯 .env 檔案填入你的設定" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 將農業文件放入 data\agriculture 資料夾" -ForegroundColor White
Write-Host ""
Write-Host "3. 載入資料到向量資料庫" -ForegroundColor White
Write-Host "   python scripts\load_data.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 啟動服務" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "詳細說明請參閱 QUICKSTART.md" -ForegroundColor Yellow
Write-Host ""
