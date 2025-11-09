"""
自訂資料更新腳本 - 可以指定要新增的文件
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from config import Config


def add_specific_files(file_paths):
    """新增特定文件到向量資料庫"""
    print("=" * 60)
    print("自訂資料更新")
    print("=" * 60)
    
    # 初始化
    loader = DocumentLoader(Config.DATA_PATH)
    vector_store = VectorStore()
    
    # 顯示當前狀態
    info = vector_store.get_collection_info()
    print(f"\n當前文件數: {info['count']}")
    
    # 載入指定文件
    all_docs = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"⚠️  找不到文件: {file_path}")
            continue
            
        print(f"\n📂 載入: {file_path}")
        docs = loader.load_file(file_path)
        all_docs.extend(docs)
        print(f"✓ 載入 {len(docs)} 個片段")
    
    if not all_docs:
        print("\n❌ 沒有載入任何文件")
        return
    
    # 分割文件
    print(f"\n✂️  分割文件成區塊...")
    chunked_docs = loader.chunk_documents(all_docs, chunk_size=500, overlap=50)
    print(f"共 {len(chunked_docs)} 個文件區塊")
    
    # 新增到資料庫
    print(f"\n🚀 新增到向量資料庫...")
    vector_store.add_documents(chunked_docs)
    
    # 顯示結果
    final_info = vector_store.get_collection_info()
    print(f"\n{'=' * 60}")
    print(f"✅ 更新完成！")
    print(f"{'=' * 60}")
    print(f"文件總數: {info['count']} → {final_info['count']}")
    print(f"新增: {final_info['count'] - info['count']} 個文件區塊")


def remove_old_data_and_reload():
    """清除舊資料並重新載入所有文件"""
    print("=" * 60)
    print("完全重建資料庫")
    print("=" * 60)
    
    # 刪除舊資料
    vector_store = VectorStore()
    info = vector_store.get_collection_info()
    print(f"\n目前有 {info['count']} 個文件")
    
    confirm = input("\n⚠️  確定要清除所有資料並重新載入？(yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ 已取消")
        return
    
    vector_store.delete_collection()
    print("✓ 已清除舊資料")
    
    # 重新載入
    print("\n📂 重新載入所有文件...")
    os.system("python scripts/load_data.py")


if __name__ == "__main__":
    print("\n選擇操作模式：")
    print("1. 新增特定文件")
    print("2. 完全重建資料庫")
    print("3. 取消")
    
    choice = input("\n請選擇 (1/2/3): ")
    
    if choice == "1":
        print("\n請輸入要新增的文件路徑（相對於專案根目錄）")
        print("範例: data/agriculture/新文件.txt")
        print("多個文件用逗號分隔")
        
        paths = input("\n文件路徑: ").strip()
        if paths:
            file_list = [p.strip() for p in paths.split(",")]
            add_specific_files(file_list)
        else:
            print("❌ 未輸入文件路徑")
    
    elif choice == "2":
        remove_old_data_and_reload()
    
    else:
        print("❌ 已取消")
