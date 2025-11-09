# OCR 功能安裝指南

## 方案 A：線上 OCR（最簡單）⭐

**完全免費，3分鐘搞定：**

1. 前往 https://www.ilovepdf.com/zh-tw/ocr-pdf
2. 上傳您的 PDF
3. 選擇語言：繁體中文
4. 點擊「辨識文字」
5. 下載處理後的 PDF
6. 替換原檔案
7. 執行 `更新資料庫.bat`

**優點：**
- ✅ 不需安裝任何軟體
- ✅ 支援繁體中文
- ✅ 免費（每天有使用次數限制）
- ✅ 品質好

---

## 方案 B：本地 OCR（需要安裝）

**如果您需要經常處理大量 PDF，可以使用本地 OCR。**

### 步驟 1：安裝 Tesseract OCR

```powershell
# 使用 Chocolatey 安裝（推薦）
choco install tesseract

# 或手動下載安裝
# https://github.com/UB-Mannheim/tesseract/wiki
# 下載 tesseract-ocr-w64-setup-v5.x.x.exe
# 安裝時記得勾選「繁體中文」語言包
```

### 步驟 2：安裝 Python 套件

```powershell
pip install pdf2image pytesseract pillow
pip install poppler-utils  # 或手動安裝 poppler
```

### 步驟 3：下載 Poppler

```powershell
# 下載 Poppler for Windows
# https://github.com/oschwartz10612/poppler-windows/releases
# 解壓縮到 C:\poppler
# 將 C:\poppler\Library\bin 加入系統 PATH
```

### 步驟 4：使用 OCR 腳本

我已經為您準備好了！執行：

```powershell
python scripts/ocr_pdf.py
```

---

## 方案 C：使用 Adobe Acrobat（如果您有）

1. 開啟 PDF
2. 工具 → 編輯 PDF
3. 掃描與 OCR → 識別文字 → 在此檔案中
4. 儲存

---

## 建議

**對於偶爾使用：** 
→ 使用**線上 OCR**（方案 A）最簡單！

**對於經常使用：**
→ 安裝**本地 OCR**（方案 B）一勞永逸

**時間對比：**
- 線上 OCR：3分鐘搞定一個檔案
- 安裝本地 OCR：首次設定 15-20 分鐘，之後秒處理

---

需要我幫您設定本地 OCR 嗎？
