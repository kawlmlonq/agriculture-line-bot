"""
簡化版 OCR PDF 處理腳本
使用 pytesseract 將掃描版 PDF 轉換為可搜尋的文字檔
"""
import os
import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_simple_dependencies():
    """檢查基本依賴"""
    try:
        import pytesseract
        import PIL
        from pdf2image import convert_from_path
        
        # 設定 Tesseract 路徑
        import os
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                print(f"✅ 找到 Tesseract：{path}")
                break
        
        return True
    except ImportError as e:
        print(f"❌ 缺少依賴：{e}")
        print("\n請先執行：install_ocr.bat")
        return False

def find_poppler():
    """尋找 Poppler"""
    paths = [
        project_root / "poppler" / "poppler-24.08.0" / "Library" / "bin",
        project_root / "poppler" / "Library" / "bin",
        Path("C:/poppler/Library/bin"),
    ]
    
    for p in paths:
        if p.exists() and (p / "pdfinfo.exe").exists():
            return str(p)
    return None

def ocr_pdf_to_text(pdf_path: Path, lang: str = "chi_tra+eng") -> str:
    """
    將 PDF 轉換為文字（使用 OCR）
    
    Returns:
        提取的文字內容
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
        
        # 設定 Poppler 路徑
        poppler_path = find_poppler()
        if not poppler_path:
            print("❌ 找不到 Poppler！請執行 install_ocr.bat")
            return None
        
        print(f"📄 轉換 PDF 為圖片：{pdf_path.name}")
        
        # 轉換 PDF 為圖片
        images = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=poppler_path
        )
        
        print(f"🔤 執行 OCR（共 {len(images)} 頁）...")
        
        # 對每頁執行 OCR
        all_text = []
        for i, image in enumerate(images, 1):
            print(f"   處理第 {i}/{len(images)} 頁...", end="\r")
            text = pytesseract.image_to_string(image, lang=lang)
            all_text.append(f"=== 第 {i} 頁 ===\n{text}\n")
        
        print(f"\n✅ OCR 完成！")
        
        return "\n".join(all_text)
        
    except Exception as e:
        print(f"❌ OCR 失敗：{e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("=" * 60)
    print("🤖 簡易 PDF OCR 工具")
    print("=" * 60)
    print()
    
    # 檢查依賴
    if not check_simple_dependencies():
        sys.exit(1)
    
    # 設定路徑
    data_dir = project_root / "data" / "agriculture"
    output_dir = project_root / "data" / "agriculture_ocr"
    output_dir.mkdir(exist_ok=True)
    
    # 尋找掃描版 PDF（這裡我們知道是哪一個）
    target_pdf = data_dir / "蕃茄栽培管理技術.pdf"
    
    if not target_pdf.exists():
        print(f"❌ 找不到檔案：{target_pdf}")
        print("\n請確認 PDF 檔案位於 data/agriculture/ 目錄")
        sys.exit(1)
    
    print(f"📁 找到檔案：{target_pdf.name}")
    print()
    
    # 執行 OCR
    text = ocr_pdf_to_text(target_pdf)
    
    if text:
        # 儲存為文字檔
        output_txt = output_dir / f"{target_pdf.stem}.txt"
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"\n💾 已儲存為文字檔：{output_txt}")
        print(f"   文字長度：{len(text)} 字元")
        
        # 顯示前 500 字元預覽
        print("\n📝 內容預覽：")
        print("-" * 60)
        print(text[:500])
        print("-" * 60)
        
        print("\n✅ 完成！")
        print("\n💡 下一步：")
        print("1. 檢查文字檔內容是否正確")
        print("2. 如果正確，將文字檔複製到 data/agriculture/")
        print("3. 執行 更新資料庫.bat 重新載入")
    else:
        print("\n❌ OCR 失敗！")
        sys.exit(1)

if __name__ == "__main__":
    main()
