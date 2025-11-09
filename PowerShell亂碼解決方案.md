# PowerShell 亂碼問題解決方案

## 🐛 問題描述

在 Windows PowerShell 中執行腳本時，中文和 Emoji 符號顯示為亂碼：
```
?湔摰?嚗?
? 銝?甇伐???隡箸??刻??湔??
```

應該顯示為：
```
✅ 資料載入完成！
🌾 農業知識庫 LINE Bot
📊 向量資料庫：234 個文件
```

---

## 🔍 問題原因

Windows PowerShell 預設使用 **Big5** 或 **系統預設編碼**，而非 **UTF-8**。

當 Python 腳本輸出 UTF-8 編碼的中文或 Emoji 時，PowerShell 無法正確解析。

---

## ✅ 解決方案

### 方案 1：執行修正腳本（推薦）

**當前終端立即生效：**
```powershell
.\修正編碼.ps1
```

這會設定：
- Console 編碼：UTF-8
- Output 編碼：UTF-8  
- Code Page：65001 (UTF-8)

### 方案 2：手動設定編碼

**在 PowerShell 中執行：**
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

### 方案 3：使用更新後的 .bat 檔案

所有啟動腳本已自動加入 `chcp 65001`：
- ✅ `快速啟動.bat`
- ✅ `更新資料庫.bat`
- ✅ `檢查狀態.bat`

直接執行即可，會自動設定正確編碼。

---

## 🔧 永久解決方案

### 設定 PowerShell Profile

**1. 檢查是否有 Profile：**
```powershell
Test-Path $PROFILE
```

**2. 如果不存在，建立它：**
```powershell
New-Item -Path $PROFILE -Type File -Force
```

**3. 編輯 Profile：**
```powershell
notepad $PROFILE
```

**4. 加入以下內容：**
```powershell
# 設定 UTF-8 編碼
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null
```

**5. 重新載入 Profile：**
```powershell
. $PROFILE
```

之後每次開啟 PowerShell 都會自動設定 UTF-8！

---

## 🧪 測試編碼是否正確

### 測試腳本：
```powershell
python -c "print('✅ 測試中文顯示'); print('🌾 農業知識庫'); print('📊 向量資料庫')"
```

### 預期輸出：
```
✅ 測試中文顯示
🌾 農業知識庫
📊 向量資料庫
```

如果看到亂碼，重新執行 `.\修正編碼.ps1`

---

## 📋 各種終端的解決方案

### Windows PowerShell（傳統）
```powershell
.\修正編碼.ps1
```

### Windows Terminal（推薦）
Windows Terminal 預設支援 UTF-8，通常不需要特別設定。

如果還是有問題：
1. 設定 → 配置文件 → Windows PowerShell
2. 命令列：加入 `-NoExit -Command "chcp 65001"`

### PowerShell Core (pwsh)
PowerShell 7+ 預設使用 UTF-8，不需要額外設定。

### CMD (命令提示字元)
在 .bat 檔案開頭加入：
```bat
@echo off
chcp 65001 >nul
```

---

## 🔍 檢查當前編碼

### PowerShell 指令：
```powershell
# 檢查 Console 編碼
[Console]::OutputEncoding

# 檢查 Output 編碼
$OutputEncoding

# 檢查 Code Page
chcp
```

### 正確的輸出應該是：
```
BodyName          : utf-8
EncodingName      : Unicode (UTF-8)
...
Active code page: 65001
```

---

## 🆘 常見問題

### Q1: 執行 `.\修正編碼.ps1` 後還是亂碼？

**A:** 可能需要重啟終端。關閉 PowerShell 重新開啟，再執行一次。

### Q2: Python 程式本身輸出亂碼？

**A:** 檢查 Python 檔案的編碼：
```python
# 在 .py 檔案開頭加入
# -*- coding: utf-8 -*-
```

### Q3: 使用 VSCode 終端還是亂碼？

**A:** VSCode 設定：
1. 檔案 → 喜好設定 → 設定
2. 搜尋 "terminal integrated encoding"
3. 設定為 "utf8"

或在 settings.json 加入：
```json
{
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "args": ["-NoExit", "-Command", "chcp 65001 | Out-Null"]
        }
    }
}
```

### Q4: 其他程式（如 Git）也有亂碼？

**A:** Git 編碼設定：
```bash
git config --global core.quotepath false
git config --global gui.encoding utf-8
git config --global i18n.commit.encoding utf-8
git config --global i18n.logoutputencoding utf-8
```

---

## 📊 編碼對照表

| Code Page | 編碼名稱 | 說明 |
|-----------|---------|------|
| 65001 | UTF-8 | 通用 Unicode（推薦）|
| 950 | Big5 | 繁體中文（舊式）|
| 936 | GBK | 簡體中文 |
| 437 | ASCII | 英文 |

---

## 🎯 最佳實踐

1. **開發環境：** 使用 Windows Terminal + PowerShell 7
2. **啟動腳本：** 在 .bat 檔案開頭加入 `chcp 65001`
3. **Python 檔案：** 使用 UTF-8 編碼儲存
4. **永久設定：** 修改 PowerShell Profile

---

## 📚 相關資源

- [Microsoft Docs - Console Code Pages](https://docs.microsoft.com/en-us/windows/console/console-code-pages)
- [PowerShell 編碼設定](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)
- [UTF-8 Everywhere](https://utf8everywhere.org/)

---

## ✅ 檢查清單

完成以下設定，確保不再出現亂碼：

- [ ] 執行 `.\修正編碼.ps1` 測試
- [ ] 設定 PowerShell Profile（永久）
- [ ] 更新所有 .bat 檔案加入 `chcp 65001`
- [ ] 確認 Python 檔案使用 UTF-8 編碼
- [ ] 測試中文和 Emoji 顯示正常

---

**最後更新：** 2025/11/09  
**狀態：** ✅ 已解決，所有啟動腳本已更新
