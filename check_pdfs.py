"""檢查所有 PDF 檔案狀態"""
import os
from pathlib import Path
from pypdf import PdfReader

data_path = Path('./data/agriculture')

print("=" * 60)
print("PDF 檔案狀態檢查")
print("=" * 60)

for pdf_file in data_path.glob('*.pdf'):
    print(f"\n📄 {pdf_file.name}")
    try:
        reader = PdfReader(str(pdf_file))
        pages = len(reader.pages)
        
        # 檢查前3頁是否有文字
        has_text = False
        for i in range(min(3, pages)):
            text = reader.pages[i].extract_text()
            if text.strip():
                has_text = True
                break
        
        print(f"   頁數: {pages}")
        print(f"   類型: {'✅ 文字型 PDF' if has_text else '❌ 圖片型 PDF（需要 OCR）'}")
        
    except Exception as e:
        print(f"   ❌ 錯誤: {e}")
