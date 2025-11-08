"""
系統檢查腳本 - 驗證環境設定
"""
import sys
import os

def check_python_version():
    """檢查 Python 版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 版本過舊，需要 3.8 或更新版本")
        print(f"  當前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python 版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_packages():
    """檢查必要套件"""
    required_packages = [
        ('flask', 'flask'),
        ('chromadb', 'chromadb'),
        ('sentence-transformers', 'sentence_transformers'),
        ('groq', 'groq'),
        ('line-bot-sdk', 'linebot'),
        ('python-dotenv', 'dotenv')
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} (未安裝)")
            missing_packages.append(package_name)
    
    return len(missing_packages) == 0, missing_packages

def check_env_file():
    """檢查環境變數檔案"""
    if not os.path.exists('.env'):
        print("✗ .env 檔案不存在")
        print("  請複製 .env.example 為 .env 並填入設定")
        return False
    
    print("✓ .env 檔案存在")
    
    # 檢查必要的環境變數
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'LINE_CHANNEL_ACCESS_TOKEN',
        'LINE_CHANNEL_SECRET',
        'GROQ_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            print(f"  ⚠️  {var} 需要設定")
            missing_vars.append(var)
        else:
            print(f"  ✓ {var} 已設定")
    
    return len(missing_vars) == 0

def check_data_directory():
    """檢查資料資料夾"""
    if not os.path.exists('data/agriculture'):
        print("✗ data/agriculture 資料夾不存在")
        return False
    
    files = os.listdir('data/agriculture')
    file_count = len([f for f in files if os.path.isfile(os.path.join('data/agriculture', f))])
    
    print(f"✓ data/agriculture 資料夾存在 ({file_count} 個檔案)")
    
    if file_count == 0:
        print("  ⚠️  資料夾是空的，請新增農業知識文件")
    
    return True

def check_vector_db():
    """檢查向量資料庫"""
    if not os.path.exists('vector_db'):
        print("⚠️  向量資料庫尚未建立")
        print("  請執行: python scripts\\load_data.py")
        return False
    
    print("✓ 向量資料庫資料夾存在")
    return True

def main():
    """主程式"""
    print("=" * 60)
    print("農業知識庫 LINE Bot - 系統檢查")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # 檢查 Python 版本
    print("【Python 環境】")
    if not check_python_version():
        all_ok = False
    print()
    
    # 檢查套件
    print("【Python 套件】")
    packages_ok, missing = check_packages()
    if not packages_ok:
        all_ok = False
        print()
        print(f"缺少套件: {', '.join(missing)}")
        print("執行安裝: pip install -r requirements.txt")
    print()
    
    # 檢查環境變數
    print("【環境變數】")
    if not check_env_file():
        all_ok = False
    print()
    
    # 檢查資料資料夾
    print("【資料檔案】")
    if not check_data_directory():
        all_ok = False
    print()
    
    # 檢查向量資料庫
    print("【向量資料庫】")
    check_vector_db()
    print()
    
    # 總結
    print("=" * 60)
    if all_ok:
        print("✓ 系統檢查完成，一切就緒！")
        print()
        print("可以執行:")
        print("  1. python scripts\\load_data.py  (如果尚未載入資料)")
        print("  2. python app.py                (啟動服務)")
    else:
        print("⚠️  系統檢查發現問題，請修正後再執行")
        print()
        print("常見解決方案:")
        print("  - 安裝套件: pip install -r requirements.txt")
        print("  - 設定環境: 編輯 .env 檔案")
        print("  - 準備資料: 將文件放入 data/agriculture/")
    print("=" * 60)

if __name__ == "__main__":
    main()
