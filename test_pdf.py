"""
測試 PDF 載入
"""
import sys
sys.path.insert(0, '.')

from pypdf import PdfReader

file_path = './data/agriculture/蕃茄栽培管理技術.pdf'

try:
    print(f"嘗試載入: {file_path}")
    reader = PdfReader(file_path)
    print(f"PDF 頁數: {len(reader.pages)}")
    
    for i, page in enumerate(reader.pages[:3]):  # 只檢查前3頁
        text = page.extract_text()
        print(f"\n--- 第 {i+1} 頁 ---")
        print(f"文字長度: {len(text)}")
        print(f"是否有內容: {bool(text.strip())}")
        if text.strip():
            print(f"前100字: {text[:100]}")
        else:
            print("⚠️ 無法提取文字")
            
except Exception as e:
    print(f"錯誤: {e}")
    import traceback
    traceback.print_exc()
