# 🤖 OCR 系統使用指南

## 📋 快速開始（3 步驟）

### 步驟 1️⃣：安裝 OCR 工具

雙擊執行：
```
install_ocr.bat
```

**這會自動安裝：**
- ✅ Python 套件（pytesseract, pdf2image, Pillow, reportlab）
- ✅ Poppler（PDF 轉圖片工具）
- ✅ Tesseract OCR（文字識別引擎）
- ✅ 繁體中文語言包

**預計時間：** 5-10 分鐘

---

### 步驟 2️⃣：執行 OCR 處理

雙擊執行：
```
OCR處理.bat
```

這會：
- 🔍 自動找到掃描版 PDF（蕃茄栽培管理技術.pdf）
- 📄 將 PDF 轉換為圖片
- 🔤 使用 OCR 識別文字
- 💾 儲存為 `.txt` 文字檔（位於 `data/agriculture_ocr/`）

**預計時間：** 2-5 分鐘（取決於頁數）

---

### 步驟 3️⃣：更新資料庫

檢查 OCR 結果後，執行：
```
更新資料庫.bat
```

這會自動載入新的文字檔到向量資料庫！

---

## 🛠️ 進階使用

### 方案 A：簡易版（推薦）

```bash
# 直接轉換為文字檔
python scripts\simple_ocr.py
```

**優點：**
- 簡單快速
- 直接產生 .txt 檔案
- 容易檢查結果

---

### 方案 B：完整版

```bash
# 自動偵測所有掃描版 PDF 並處理
python scripts\ocr_pdf.py
```

**功能：**
- 自動掃描 `data/agriculture/` 目錄
- 識別哪些 PDF 需要 OCR
- 批次處理多個檔案
- 產生可搜尋的 PDF 檔案

---

## 📁 檔案位置

```
agriculture-line-bot/
├── data/
│   ├── agriculture/          # 原始 PDF 位置
│   │   └── 蕃茄栽培管理技術.pdf
│   └── agriculture_ocr/      # OCR 結果輸出
│       └── 蕃茄栽培管理技術.txt
│
├── scripts/
│   ├── simple_ocr.py         # 簡易 OCR 腳本
│   ├── ocr_pdf.py            # 完整 OCR 腳本
│   └── install_poppler.ps1   # Poppler 安裝腳本
│
├── install_ocr.bat           # 一鍵安裝
└── OCR處理.bat               # 一鍵處理
```

---

## ⚙️ 系統需求

| 項目 | 說明 |
|------|------|
| **Python** | 3.8+ |
| **磁碟空間** | ~500MB（安裝 Tesseract + Poppler） |
| **記憶體** | 建議 4GB+ |
| **網路** | 需要下載工具（首次安裝） |

---

## 🐛 常見問題

### Q1: `Tesseract not found`
**解決：**
1. 確認已執行 `install_ocr.bat`
2. 檢查 Tesseract 是否安裝：
   ```bash
   tesseract --version
   ```
3. 手動下載：https://github.com/UB-Mannheim/tesseract/wiki

---

### Q2: `Unable to find poppler`
**解決：**
1. 執行：`powershell -ExecutionPolicy Bypass -File scripts\install_poppler.ps1`
2. 或手動下載 Poppler 並解壓到 `poppler/` 資料夾

---

### Q3: OCR 結果不準確
**改進方法：**
1. 提高 DPI（修改腳本中的 `dpi=300` → `dpi=600`）
2. 使用更好的語言模型：
   ```bash
   # 下載更好的繁體中文模型
   https://github.com/tesseract-ocr/tessdata_best
   ```
3. 預處理圖片（增強對比度、去雜訊）

---

### Q4: 處理速度太慢
**加速方法：**
1. 降低 DPI（`dpi=150` 或 `dpi=200`）
2. 只處理部分頁面
3. 使用 GPU 加速（需要額外設定）

---

## 📊 效能參考

| PDF 類型 | 頁數 | DPI | 處理時間 |
|---------|------|-----|---------|
| 掃描版黑白 | 4 頁 | 300 | ~1-2 分鐘 |
| 掃描版彩色 | 4 頁 | 300 | ~2-3 分鐘 |
| 高品質掃描 | 10 頁 | 600 | ~5-8 分鐘 |

---

## 🎯 品質對比

### 原始 PDF（掃描版）
```
無法提取文字 ❌
```

### OCR 處理後
```
蕃茄栽培管理技術

一、品種選擇
建議選用抗病性強的品種...

二、育苗管理
播種前應進行種子消毒...
```
✅ **可搜尋、可複製、可向量化！**

---

## 💡 最佳實踐

1. **首次使用**
   - 執行 `install_ocr.bat` 完整安裝
   - 用小檔案測試（確認工具正常）

2. **日常使用**
   - 掃描版 PDF → 放入 `data/agriculture/`
   - 執行 `OCR處理.bat`
   - 檢查 `data/agriculture_ocr/` 的結果
   - 執行 `更新資料庫.bat`

3. **品質檢查**
   - 開啟生成的 `.txt` 檔
   - 檢查是否有亂碼或錯字
   - 必要時手動修正

---

## 🚀 自動化流程

想要完全自動化？修改 `更新資料庫.bat`：

```batch
@echo off
REM 1. 先執行 OCR
call OCR處理.bat

REM 2. 再更新資料庫
call .venv\Scripts\activate.bat
python scripts\smart_load_data.py
pause
```

---

## 📞 需要幫助？

遇到問題可以：
1. 查看錯誤訊息
2. 檢查 `data/agriculture_ocr/` 目錄
3. 執行 `check_pdfs.py` 診斷 PDF 類型
4. 回報具體錯誤訊息

---

**祝使用順利！** 🎉
