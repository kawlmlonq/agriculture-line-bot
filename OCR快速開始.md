# 🚀 OCR 快速開始指南

## ✅ 目前進度

### 已完成：
- ✅ Python 套件已安裝（pytesseract, pdf2image, Pillow, reportlab）
- ✅ Poppler 已安裝並設定

### 待完成：
- ⏳ 安裝 Tesseract OCR

---

## 📝 接下來只需 2 步驟：

### 步驟 1️⃣：安裝 Tesseract OCR（5 分鐘）

#### 方法 A：自動下載（推薦）
```batch
.\install_tesseract.bat
```
會打開瀏覽器到下載頁面，並提供安裝指引。

#### 方法 B：手動下載
1. 訪問：https://github.com/UB-Mannheim/tesseract/releases
2. 下載：`tesseract-ocr-w64-setup-5.X.X.XXXXXXXX.exe`
3. 執行安裝程式
4. **重要**：安裝時勾選「Traditional Chinese」語言包
5. 安裝完成後，確認已加入 PATH

#### 驗證安裝：
```powershell
tesseract --version
```
如果看到版本號，就成功了！✅

---

### 步驟 2️⃣：執行 OCR 處理

安裝完 Tesseract 後，雙擊執行：
```batch
OCR處理.bat
```

這會：
1. 🔍 找到掃描版 PDF（`蕃茄栽培管理技術.pdf`）
2. 📄 轉換為圖片
3. 🔤 執行 OCR 識別
4. 💾 產生文字檔（`data/agriculture_ocr/蕃茄栽培管理技術.txt`）

---

## 🎯 預期結果

OCR 處理後，您會在 `data/agriculture_ocr/` 看到：
```
蕃茄栽培管理技術.txt  (包含識別出的文字)
```

檢查文字檔內容，如果正確，執行：
```batch
更新資料庫.bat
```

系統會自動載入新的文字檔！✨

---

## 🔧 故障排除

### 問題 1: `tesseract: command not found`
**解決：**
1. 確認 Tesseract 已安裝
2. 手動加入 PATH：
   - Win + X → 系統 → 進階系統設定
   - 環境變數 → 系統變數 → Path → 編輯
   - 新增：`C:\Program Files\Tesseract-OCR`
3. 重新開啟 PowerShell

### 問題 2: OCR 結果是亂碼
**解決：**
- 確認已安裝繁體中文語言包（chi_tra）
- 重新安裝 Tesseract，勾選 Traditional Chinese

### 問題 3: 處理速度很慢
**正常現象：**
- OCR 處理需要時間
- 4 頁 PDF 約需 2-3 分鐘
- 可以調低 DPI 加速（但會降低品質）

---

## 📊 狀態總結

| 組件 | 狀態 | 說明 |
|------|------|------|
| Python 套件 | ✅ 已安裝 | pytesseract, pdf2image, Pillow |
| Poppler | ✅ 已安裝 | PDF 轉圖片工具 |
| Tesseract | ⏳ 待安裝 | OCR 引擎 |
| 繁體中文包 | ⏳ 待安裝 | chi_tra 語言資料 |

---

## 💡 小提示

安裝 Tesseract 時：
- ✅ 勾選「Additional language data」
- ✅ 選擇「Traditional Chinese (chi_tra)」
- ✅ 允許加入系統 PATH
- ✅ 記住安裝路徑

完成後就可以開始處理 PDF 了！🎉
