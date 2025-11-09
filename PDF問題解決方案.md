# PDF 檔案無法載入的解決方案

## 問題診斷

您的 `蕃茄栽培管理技術.pdf` 是**圖片型 PDF**（掃描版），沒有文字層，所以無法直接提取文字。

## 解決方案

### 方案 1：轉換為文字型 PDF（推薦）

使用 Adobe Acrobat 或線上工具進行 OCR 處理：

1. **Adobe Acrobat Pro**
   - 開啟 PDF → 工具 → 編輯 PDF
   - 點擊「掃描與 OCR」→「識別文字」→「在此檔案中」
   - 儲存處理後的 PDF

2. **線上 OCR 工具**
   - https://www.ilovepdf.com/zh-tw/ocr-pdf
   - https://www.adobe.com/acrobat/online/pdf-to-text.html
   - 上傳 PDF，下載處理後的文字型 PDF

### 方案 2：安裝 OCR 功能（進階）

需要安裝額外的套件和依賴：

```powershell
# 安裝 Tesseract OCR
# 1. 下載: https://github.com/UB-Mannheim/tesseract/wiki
# 2. 安裝並記住安裝路徑（例如 C:\Program Files\Tesseract-OCR）

# 安裝 Python 套件
pip install pdf2image pytesseract pillow

# 還需要安裝 poppler
# 下載: https://github.com/oschwartz10612/poppler-windows/releases
# 解壓縮並加入系統 PATH
```

然後使用這個腳本：

\`\`\`python
# scripts/load_data_with_ocr.py
import os
from pdf2image import convert_from_path
import pytesseract

# 設定 Tesseract 路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for i, image in enumerate(images):
        print(f"處理第 {i+1} 頁...")
        text += pytesseract.image_to_string(image, lang='chi_tra')  # 繁體中文
    return text
\`\`\`

### 方案 3：手動轉換為文字檔（最簡單）

1. 使用 OCR 工具將 PDF 轉為文字
2. 複製文字內容
3. 儲存為 `.txt` 檔案到 `data/agriculture/`
4. 執行更新資料庫

## 建議做法

**最簡單且可靠的方式：**

1. 使用線上 OCR 工具（如 ilovepdf）處理 PDF
2. 下載處理後的 PDF（已包含文字層）
3. 替換原檔案
4. 重新執行更新資料庫

或者：

1. 手動複製 PDF 內容到 Word
2. 整理文字格式
3. 另存為 `.txt` 或 `.docx`
4. 放入 `data/agriculture/`
5. 執行更新資料庫

## 檢查 PDF 類型

執行這個命令可以檢查 PDF 是否為圖片型：

\`\`\`powershell
python test_pdf.py
\`\`\`

如果顯示「無法提取文字」，就是圖片型 PDF，需要 OCR 處理。

## 已支援的檔案

系統可以正常處理：
- ✅ 文字型 PDF（有文字層）
- ✅ Word 文件 (.docx)
- ✅ 純文字檔 (.txt)
- ✅ Excel 檔案 (.xlsx)
- ❌ 圖片型 PDF（需要 OCR）
- ❌ 圖片檔案（需要 OCR）

---

**如需協助設定 OCR 功能，請告訴我！**
