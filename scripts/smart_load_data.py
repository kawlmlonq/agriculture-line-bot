"""
智能資料載入腳本 - 只處理新增或修改的文件
"""
import sys
import os
import json
import hashlib
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from config import Config


# 檔案追蹤記錄路徑
TRACKING_FILE = os.path.join(Config.VECTOR_DB_PATH, 'file_tracking.json')


def get_file_hash(file_path):
    """計算檔案的 MD5 hash"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"⚠️  無法計算 hash: {file_path} - {e}")
        return None


def load_tracking_data():
    """載入檔案追蹤記錄"""
    if os.path.exists(TRACKING_FILE):
        try:
            with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_tracking_data(data):
    """儲存檔案追蹤記錄"""
    os.makedirs(os.path.dirname(TRACKING_FILE), exist_ok=True)
    with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_files_to_process(data_path):
    """
    取得需要處理的檔案
    
    Returns:
        tuple: (新檔案列表, 修改檔案列表, 未變更檔案列表)
    """
    tracking_data = load_tracking_data()
    
    new_files = []
    modified_files = []
    unchanged_files = []
    
    # 掃描資料夾中的所有檔案
    for root, dirs, files in os.walk(data_path):
        for file in files:
            # 只處理支援的檔案格式
            if not file.lower().endswith(('.txt', '.pdf', '.docx', '.xlsx')):
                continue
            
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, data_path)
            
            # 計算檔案 hash
            current_hash = get_file_hash(file_path)
            if current_hash is None:
                continue
            
            # 取得檔案修改時間
            mtime = os.path.getmtime(file_path)
            
            # 檢查檔案是否已存在於追蹤記錄中
            if relative_path in tracking_data:
                old_hash = tracking_data[relative_path].get('hash')
                if old_hash == current_hash:
                    unchanged_files.append(file_path)
                else:
                    modified_files.append(file_path)
            else:
                new_files.append(file_path)
    
    return new_files, modified_files, unchanged_files


def main():
    """主程式"""
    print("=" * 60)
    print("農業知識庫 - 智能資料載入程式")
    print("=" * 60)
    
    # 檢查資料夾是否存在
    if not os.path.exists(Config.DATA_PATH):
        os.makedirs(Config.DATA_PATH, exist_ok=True)
        print(f"\n已建立資料夾: {Config.DATA_PATH}")
        print(f"請將農業相關文件放入此資料夾，然後重新執行此腳本。")
        return
    
    # 分析需要處理的檔案
    print(f"\n📂 掃描資料夾: {Config.DATA_PATH}")
    new_files, modified_files, unchanged_files = get_files_to_process(Config.DATA_PATH)
    
    # 顯示掃描結果
    print(f"\n📊 掃描結果:")
    print(f"   ✅ 未變更檔案: {len(unchanged_files)} 個")
    print(f"   🆕 新增檔案: {len(new_files)} 個")
    print(f"   📝 修改檔案: {len(modified_files)} 個")
    
    # 顯示詳細資訊
    if unchanged_files:
        print(f"\n✅ 未變更檔案（跳過）:")
        for f in unchanged_files:
            print(f"   • {os.path.basename(f)}")
    
    if new_files:
        print(f"\n🆕 新增檔案:")
        for f in new_files:
            print(f"   • {os.path.basename(f)}")
    
    if modified_files:
        print(f"\n📝 修改檔案:")
        for f in modified_files:
            print(f"   • {os.path.basename(f)}")
    
    # 如果沒有需要處理的檔案
    files_to_process = new_files + modified_files
    if not files_to_process:
        print(f"\n✅ 所有檔案都已是最新狀態，無需更新！")
        return
    
    # 詢問是否繼續
    print(f"\n總共需要處理 {len(files_to_process)} 個檔案")
    response = input("是否繼續？(y/n): ")
    if response.lower() != 'y':
        print("已取消")
        return
    
    # 初始化文件載入器
    loader = DocumentLoader(Config.DATA_PATH)
    
    # 只載入需要處理的檔案
    all_docs = []
    tracking_data = load_tracking_data()
    
    for file_path in files_to_process:
        relative_path = os.path.relpath(file_path, Config.DATA_PATH)
        print(f"\n📄 處理: {os.path.basename(file_path)}")
        
        try:
            # 根據檔案類型選擇載入方法
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.txt':
                docs = loader.load_txt(file_path)
            elif file_ext == '.pdf':
                docs = loader.load_pdf(file_path)
            elif file_ext in ['.docx', '.doc']:
                docs = loader.load_docx(file_path)
            elif file_ext == '.xlsx':
                docs = loader.load_xlsx(file_path)
            else:
                print(f"   ✗ 不支援的檔案格式: {file_ext}")
                continue
            
            all_docs.extend(docs)
            
            # 更新追蹤記錄
            tracking_data[relative_path] = {
                'hash': get_file_hash(file_path),
                'mtime': os.path.getmtime(file_path),
                'processed_at': datetime.now().isoformat(),
                'chunks': len(docs)
            }
            
            print(f"   ✓ 載入 {len(docs)} 個片段")
        except Exception as e:
            print(f"   ✗ 載入失敗: {e}")
    
    if not all_docs:
        print("\n⚠️  沒有成功載入任何文件")
        return
    
    # 分割文件成較小的區塊
    print(f"\n✂️  分割文件成區塊...")
    chunked_docs = loader.chunk_documents(all_docs, chunk_size=500, overlap=50)
    print(f"共 {len(chunked_docs)} 個文件區塊")
    
    # 初始化向量資料庫
    print(f"\n💾 初始化向量資料庫...")
    vector_store = VectorStore()
    
    # 顯示資料庫資訊
    info = vector_store.get_collection_info()
    print(f"集合名稱: {info['name']}")
    print(f"現有文件數: {info['count']}")
    
    # 如果是修改檔案，需要先刪除舊資料
    if modified_files:
        print(f"\n🗑️  注意: 修改的檔案需要先刪除舊資料")
        print(f"   建議: 使用完全重建模式")
        response = input("是否清除所有資料並重新載入？(y/n): ")
        if response.lower() == 'y':
            vector_store.delete_collection()
            vector_store = VectorStore()
            print("✓ 已清除舊資料")
            
            # 重新載入所有檔案（包含未變更的）
            print("\n📂 重新載入所有檔案...")
            all_files = unchanged_files + files_to_process
            all_docs = []
            
            for file_path in all_files:
                file_ext = os.path.splitext(file_path)[1].lower()
                try:
                    if file_ext == '.txt':
                        docs = loader.load_txt(file_path)
                    elif file_ext == '.pdf':
                        docs = loader.load_pdf(file_path)
                    elif file_ext in ['.docx', '.doc']:
                        docs = loader.load_docx(file_path)
                    elif file_ext == '.xlsx':
                        docs = loader.load_xlsx(file_path)
                    else:
                        continue
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"   ✗ {os.path.basename(file_path)}: {e}")
            
            chunked_docs = loader.chunk_documents(all_docs, chunk_size=500, overlap=50)
            print(f"共 {len(chunked_docs)} 個文件區塊")
    
    # 新增文件到向量資料庫
    print(f"\n🚀 開始新增文件到向量資料庫...")
    vector_store.add_documents(chunked_docs)
    
    # 儲存追蹤記錄
    save_tracking_data(tracking_data)
    
    # 顯示最終資訊
    final_info = vector_store.get_collection_info()
    print(f"\n{'=' * 60}")
    print(f"✅ 資料載入完成！")
    print(f"{'=' * 60}")
    print(f"集合名稱: {final_info['name']}")
    print(f"文件總數: {final_info['count']}")
    print(f"儲存位置: {final_info['persist_directory']}")
    print(f"追蹤記錄: {TRACKING_FILE}")
    
    # 測試搜尋功能
    print(f"\n{'=' * 60}")
    print("🧪 測試搜尋功能")
    print(f"{'=' * 60}")
    vector_store.test_search("水稻種植方法")


if __name__ == "__main__":
    main()
