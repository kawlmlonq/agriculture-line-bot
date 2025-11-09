"""
OCR PDF 處理腳本
自動檢測掃描版 PDF 並進行 OCR 處理
"""
import os
import sys
from pathlib import Path
from typing import List, Tuple
import hashlib

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def find_poppler_path():
    """尋找 Poppler 安裝路徑"""
    possible_paths = [
        project_root / "poppler" / "Library" / "bin",
        Path("C:/poppler/Library/bin"),
        Path("C:/Program Files/poppler/Library/bin"),
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "pdfinfo.exe").exists():
            return str(path)
    
    return None

def check_dependencies():
    """檢查必要的依賴是否已安裝"""
    missing = []
    
    try:
        import pytesseract
    except ImportError:
        missing.append("pytesseract")
    
    try:
        from pdf2image import convert_from_path
    except ImportError:
        missing.append("pdf2image")
    
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")
    
    try:
        import pypdf
    except ImportError:
        missing.append("pypdf")
    
    if missing:
        print("❌ 缺少以下依賴套件：")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n請執行以下命令安裝：")
        print(f"pip install {' '.join(missing)}")
        return False
    
    # 檢查 Tesseract 是否已安裝
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
    except Exception as e:
        print("❌ Tesseract OCR 未安裝或未設定！")
        print("\n請執行以下步驟：")
        print("1. 執行 install_ocr.bat 自動安裝")
        print("   或")
        print("2. 手動安裝：")
        print("   - 下載：https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - 安裝後設定 TESSDATA_PREFIX 環境變數")
        return False
    
    # 尋找 Poppler
    poppler_path = find_poppler_path()
    if poppler_path:
        print(f"✅ 找到 Poppler：{poppler_path}")
        os.environ['PATH'] = f"{poppler_path};{os.environ.get('PATH', '')}"
    else:
        print("⚠️  未找到 Poppler！")
        print("\n請執行 install_ocr.bat 自動安裝")
        return False
    
    return True

def is_image_based_pdf(pdf_path: Path, sample_pages: int = 3) -> bool:
    """檢查 PDF 是否為掃描版（圖片型）"""
    try:
        import pypdf
        
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            total_pages = len(reader.pages)
            pages_to_check = min(sample_pages, total_pages)
            
            total_text_length = 0
            for i in range(pages_to_check):
                text = reader.pages[i].extract_text()
                total_text_length += len(text.strip())
            
            # 如果平均每頁文字少於 100 字元，判定為掃描版
            avg_text_per_page = total_text_length / pages_to_check
            return avg_text_per_page < 100
    
    except Exception as e:
        print(f"⚠️  無法檢查 {pdf_path.name}：{e}")
        return False

def ocr_pdf(input_path: Path, output_path: Path, lang: str = "chi_tra+eng") -> bool:
    """
    對 PDF 進行 OCR 處理
    
    Args:
        input_path: 輸入 PDF 路徑
        output_path: 輸出 PDF 路徑
        lang: Tesseract 語言代碼 (chi_tra=繁體中文, eng=英文)
    
    Returns:
        是否成功
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
        from PIL import Image
        import pypdf
        from pypdf import PdfWriter, PdfReader
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        
        print(f"🔍 正在處理：{input_path.name}")
        
        # 將 PDF 轉換為圖片
        print("   📄 轉換 PDF 為圖片...")
        images = convert_from_path(input_path, dpi=300)
        
        # 創建臨時 PDF 來儲存 OCR 結果
        temp_pdfs = []
        
        for i, image in enumerate(images, 1):
            print(f"   🔤 OCR 處理第 {i}/{len(images)} 頁...", end="\r")
            
            # 執行 OCR
            text = pytesseract.image_to_string(image, lang=lang)
            
            # 將文字寫入臨時 PDF（使用簡單方法）
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from io import BytesIO
            
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=A4)
            
            # 註冊中文字體（如果可用）
            try:
                # Windows 系統字體
                pdfmetrics.registerFont(TTFont('Chinese', 'C:\\Windows\\Fonts\\msjh.ttc'))
                can.setFont('Chinese', 10)
            except:
                can.setFont('Helvetica', 10)
            
            # 寫入文字（簡單布局）
            text_object = can.beginText(50, 800)
            for line in text.split('\n'):
                if line.strip():
                    text_object.textLine(line[:80])  # 限制每行長度
            can.drawText(text_object)
            can.save()
            
            packet.seek(0)
            temp_pdfs.append(PdfReader(packet))
        
        print(f"\n   ✅ OCR 完成！共 {len(images)} 頁")
        
        # 合併所有頁面
        writer = PdfWriter()
        for pdf_reader in temp_pdfs:
            writer.add_page(pdf_reader.pages[0])
        
        # 儲存輸出
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"   💾 已儲存：{output_path.name}")
        return True
        
    except Exception as e:
        print(f"\n   ❌ OCR 失敗：{e}")
        import traceback
        traceback.print_exc()
        return False

def find_image_based_pdfs(data_dir: Path) -> List[Path]:
    """尋找所有需要 OCR 的 PDF"""
    image_based_pdfs = []
    
    print("🔍 掃描 PDF 檔案...")
    for pdf_file in data_dir.rglob("*.pdf"):
        if is_image_based_pdf(pdf_file):
            image_based_pdfs.append(pdf_file)
            print(f"   📷 發現掃描版：{pdf_file.name}")
        else:
            print(f"   ✅ 文字版：{pdf_file.name}")
    
    return image_based_pdfs

def main():
    """主程序"""
    print("=" * 60)
    print("🤖 PDF OCR 自動處理系統")
    print("=" * 60)
    print()
    
    # 檢查依賴
    print("📋 檢查依賴...")
    if not check_dependencies():
        print("\n❌ 請先安裝必要的依賴！")
        print("執行：install_ocr.bat")
        sys.exit(1)
    print("✅ 所有依賴已就緒！\n")
    
    # 設定路徑
    data_dir = project_root / "data" / "agriculture"
    output_dir = project_root / "data" / "agriculture_ocr"
    output_dir.mkdir(exist_ok=True)
    
    # 尋找需要處理的 PDF
    image_based_pdfs = find_image_based_pdfs(data_dir)
    
    if not image_based_pdfs:
        print("\n✅ 沒有發現需要 OCR 的掃描版 PDF！")
        return
    
    print(f"\n📋 發現 {len(image_based_pdfs)} 個掃描版 PDF 需要處理")
    print()
    
    # 處理每個 PDF
    success_count = 0
    for pdf_path in image_based_pdfs:
        output_path = output_dir / f"{pdf_path.stem}_ocr.pdf"
        
        if ocr_pdf(pdf_path, output_path):
            success_count += 1
            print(f"   ✅ 成功處理：{pdf_path.name}")
            
            # 詢問是否替換原檔案
            response = input(f"\n   要替換原檔案嗎？(y/n): ").strip().lower()
            if response == 'y':
                import shutil
                # 備份原檔案
                backup_path = pdf_path.parent / f"{pdf_path.stem}_原始.pdf"
                shutil.copy2(pdf_path, backup_path)
                print(f"   💾 原檔案已備份：{backup_path.name}")
                
                # 替換
                shutil.copy2(output_path, pdf_path)
                print(f"   ✅ 已替換原檔案！")
        else:
            print(f"   ❌ 處理失敗：{pdf_path.name}")
        
        print()
    
    # 總結
    print("=" * 60)
    print(f"✅ 完成！成功處理 {success_count}/{len(image_based_pdfs)} 個檔案")
    print(f"📁 OCR 檔案位置：{output_dir}")
    print("=" * 60)
    
    if success_count > 0:
        print("\n💡 下一步：")
        print("1. 檢查 OCR 結果的品質")
        print("2. 如果滿意，可將 OCR 後的檔案複製回 data/agriculture/")
        print("3. 執行 更新資料庫.bat 重新載入資料")

if __name__ == "__main__":
    main()
