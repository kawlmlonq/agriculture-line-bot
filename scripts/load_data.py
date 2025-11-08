"""
資料載入腳本 - 將文件載入向量資料庫
"""
import sys
import os

# 新增專案根目錄到路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from config import Config


def main():
    """主程式"""
    print("=" * 60)
    print("農業知識庫 - 資料載入程式")
    print("=" * 60)
    
    # 檢查資料夾是否存在
    if not os.path.exists(Config.DATA_PATH):
        os.makedirs(Config.DATA_PATH, exist_ok=True)
        print(f"\n已建立資料夾: {Config.DATA_PATH}")
        print(f"請將農業相關文件放入此資料夾，然後重新執行此腳本。")
        return
    
    # 初始化文件載入器
    print(f"\n📂 讀取資料夾: {Config.DATA_PATH}")
    loader = DocumentLoader(Config.DATA_PATH)
    
    # 載入所有文件
    documents = loader.load_directory()
    
    if not documents:
        print("\n⚠️  沒有找到任何文件")
        print(f"請將 PDF、DOCX 或 TXT 檔案放入 {Config.DATA_PATH} 資料夾")
        return
    
    # 分割文件成較小的區塊
    print(f"\n✂️  分割文件成區塊...")
    chunked_docs = loader.chunk_documents(documents, chunk_size=500, overlap=50)
    print(f"共 {len(chunked_docs)} 個文件區塊")
    
    # 初始化向量資料庫
    print(f"\n💾 初始化向量資料庫...")
    vector_store = VectorStore()
    
    # 顯示資料庫資訊
    info = vector_store.get_collection_info()
    print(f"集合名稱: {info['name']}")
    print(f"現有文件數: {info['count']}")
    
    # 詢問是否要清除現有資料
    if info['count'] > 0:
        response = input("\n⚠️  資料庫中已有資料，是否要清除並重新載入？(y/n): ")
        if response.lower() == 'y':
            vector_store.delete_collection()
            vector_store = VectorStore()
            print("✓ 已清除舊資料")
    
    # 新增文件到向量資料庫
    print(f"\n🚀 開始新增文件到向量資料庫...")
    vector_store.add_documents(chunked_docs)
    
    # 顯示最終資訊
    final_info = vector_store.get_collection_info()
    print(f"\n{'=' * 60}")
    print(f"✅ 資料載入完成！")
    print(f"{'=' * 60}")
    print(f"集合名稱: {final_info['name']}")
    print(f"文件總數: {final_info['count']}")
    print(f"儲存位置: {final_info['persist_directory']}")
    
    # 測試搜尋功能
    print(f"\n{'=' * 60}")
    print("🧪 測試搜尋功能")
    print(f"{'=' * 60}")
    vector_store.test_search("水稻種植方法")


if __name__ == "__main__":
    main()
