"""
測試圖片分析功能
"""
import sys
from pathlib import Path
from src.image_analyzer import ImageAnalyzer

def test_image_analysis(image_path: str):
    """測試圖片分析"""
    print("=" * 60)
    print("圖片分析測試")
    print("=" * 60)
    print()
    
    # 檢查檔案是否存在
    if not Path(image_path).exists():
        print(f"❌ 檔案不存在: {image_path}")
        return
    
    # 讀取圖片
    print(f"📂 讀取圖片: {image_path}")
    with open(image_path, 'rb') as f:
        image_content = f.read()
    
    print(f"✓ 圖片大小: {len(image_content)} bytes ({len(image_content) / 1024:.2f} KB)")
    print()
    
    # 初始化分析器
    print("🔧 初始化圖片分析器...")
    analyzer = ImageAnalyzer()
    print(f"✓ 使用模型: {analyzer.vision_model}")
    print()
    
    # 執行分析
    print("🔍 開始分析圖片...")
    print("-" * 60)
    
    try:
        result = analyzer.analyze_agriculture_image(image_content)
        print(result)
        print("-" * 60)
        print()
        print("✅ 分析成功！")
    except Exception as e:
        print(f"❌ 分析失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python test_image_analysis.py <圖片路徑>")
        print()
        print("範例:")
        print("  python test_image_analysis.py test_image.jpg")
        print("  python test_image_analysis.py C:\\path\\to\\image.png")
    else:
        test_image_analysis(sys.argv[1])
