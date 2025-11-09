# Security Check Script - Ensure sensitive information is not committed to Git
# UTF-8 with BOM encoding

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Security Check" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$issues = @()

# 1. Check if .env is ignored
Write-Host "1. Checking if .env is in .gitignore..." -ForegroundColor Yellow
$gitignoreCheck = git check-ignore -v .env 2>&1
if ($gitignoreCheck -match ".gitignore") {
    Write-Host "   [OK] .env is properly ignored" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] .env is NOT ignored!" -ForegroundColor Red
    $issues += ".env not in .gitignore"
}

# 2. Check if .env is tracked by Git
Write-Host "`n2. Checking if .env is tracked by Git..." -ForegroundColor Yellow
$trackedEnv = git ls-files .env 2>&1
if ($trackedEnv) {
    Write-Host "   [DANGER] .env is being tracked by Git!" -ForegroundColor Red
    $issues += ".env is tracked"
} else {
    Write-Host "   [OK] .env is not tracked" -ForegroundColor Green
}

# 3. Check if .env exists in Git history
Write-Host "`n3. Checking Git history for .env..." -ForegroundColor Yellow
$historyCheck = git log --all --full-history -- .env 2>&1
if ($historyCheck) {
    Write-Host "   [WARNING] .env was committed before! Need cleanup" -ForegroundColor Yellow
    $issues += ".env in Git history"
} else {
    Write-Host "   [OK] .env never committed" -ForegroundColor Green
}

# 4. Check for other sensitive files
Write-Host "`n4. Checking for other sensitive files..." -ForegroundColor Yellow
$sensitivePatterns = @("*.key", "*.pem", "secrets/*", "credentials/*", ".env.local")
$foundSensitive = $false
foreach ($pattern in $sensitivePatterns) {
    $found = git ls-files $pattern 2>&1
    if ($found) {
        Write-Host "   [FAIL] Found sensitive file: $found" -ForegroundColor Red
        $issues += "Sensitive file tracked: $found"
        $foundSensitive = $true
    }
}
if (-not $foundSensitive) {
    Write-Host "   [OK] No other sensitive files found" -ForegroundColor Green
}

# 5. Check DEBUG mode
Write-Host "`n5. Checking DEBUG setting in .env..." -ForegroundColor Yellow
if (Test-Path .env) {
    $envContent = Get-Content .env
    $debugLine = $envContent | Select-String "DEBUG=True"
    if ($debugLine) {
        Write-Host "   [WARNING] DEBUG mode is enabled" -ForegroundColor Yellow
        Write-Host "   Recommendation: Set DEBUG=False in production" -ForegroundColor Gray
    } else {
        Write-Host "   [OK] DEBUG setting is safe" -ForegroundColor Green
    }
} else {
    Write-Host "   [WARNING] .env file not found" -ForegroundColor Yellow
}

# 6. Check Git staging area
Write-Host "`n6. Checking Git staging area..." -ForegroundColor Yellow
$staged = git diff --cached --name-only 2>&1
if ($staged -match ".env") {
    Write-Host "   [DANGER] .env is in staging area!" -ForegroundColor Red
    Write-Host "   Run: git reset HEAD .env" -ForegroundColor Gray
    $issues += ".env in staging"
} else {
    Write-Host "   [OK] Staging area is safe" -ForegroundColor Green
}

# 7. Check environment variables configuration
Write-Host "`n7. Checking environment variables..." -ForegroundColor Yellow
if (Test-Path .env) {
    $envContent = Get-Content .env -Raw
    $requiredVars = @("LINE_CHANNEL_ACCESS_TOKEN", "LINE_CHANNEL_SECRET", "GROQ_API_KEY")
    $missingVars = @()
    
    foreach ($var in $requiredVars) {
        if ($envContent -match "$var=your_" -or $envContent -notmatch $var) {
            $missingVars += $var
        }
    }
    
    if ($missingVars.Count -gt 0) {
        Write-Host "   [WARNING] Missing environment variables:" -ForegroundColor Yellow
        foreach ($var in $missingVars) {
            Write-Host "     - $var" -ForegroundColor Gray
        }
    } else {
        Write-Host "   [OK] All required variables are set" -ForegroundColor Green
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Summary" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($issues.Count -eq 0) {
    Write-Host "[PASS] Security check passed!" -ForegroundColor Green
    Write-Host "No security issues found`n" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Found $($issues.Count) security issues:`n" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  - $issue" -ForegroundColor Red
    }
    Write-Host ""
    
    # Provide solutions
    Write-Host "Recommended fixes:" -ForegroundColor Yellow
    if ($issues -contains ".env is tracked") {
        Write-Host "  1. Remove .env from Git:" -ForegroundColor Gray
        Write-Host "     git rm --cached .env" -ForegroundColor White
        Write-Host "     git commit -m 'Remove .env from tracking'" -ForegroundColor White
    }
    
    if ($issues -match ".env in Git history") {
        Write-Host "  2. Clean Git history (advanced):" -ForegroundColor Gray
        Write-Host "     git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all" -ForegroundColor White
        Write-Host "     Or use BFG Repo-Cleaner" -ForegroundColor White
    }
    
    if ($issues -contains ".env in staging") {
        Write-Host "  3. Remove from staging:" -ForegroundColor Gray
        Write-Host "     git reset HEAD .env" -ForegroundColor White
    }
    
    Write-Host ""
}

Write-Host "========================================`n" -ForegroundColor Cyan

# Best practices
Write-Host "Security Best Practices:" -ForegroundColor Cyan
Write-Host "  1. Never commit .env to Git" -ForegroundColor Gray
Write-Host "  2. Use different API keys for dev/production" -ForegroundColor Gray
Write-Host "  3. Rotate API keys regularly" -ForegroundColor Gray
Write-Host "  4. Use secret management services (Azure Key Vault)" -ForegroundColor Gray
Write-Host "  5. Set DEBUG=False in production" -ForegroundColor Gray
Write-Host ""
