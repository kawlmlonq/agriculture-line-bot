# 修正 PowerShell 亂碼問題
# Fix PowerShell encoding issues

# 設定終端機編碼為 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

Write-Host "✅ PowerShell 編碼已設定為 UTF-8" -ForegroundColor Green
Write-Host "   Console Encoding: UTF-8" -ForegroundColor Gray
Write-Host "   Output Encoding: UTF-8" -ForegroundColor Gray
Write-Host "   Code Page: 65001 (UTF-8)" -ForegroundColor Gray
Write-Host ""
Write-Host "現在可以正常顯示中文了！" -ForegroundColor Cyan
Write-Host "測試：🌾 農業知識庫 📊 資料載入完成 ✅" -ForegroundColor Yellow
