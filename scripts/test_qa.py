"""
測試腳本 - 本地測試問答功能
"""
import sys
import os

# 新增專案根目錄到路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vector_store import VectorStore
from src.qa_engine import QAEngine


def main():
    """主程式"""
    print("=" * 60)
    print("農業知識庫 - 問答測試")
    print("=" * 60)
    
    # 初始化系統
    print("\n初始化向量資料庫...")
    vector_store = VectorStore()
    
    info = vector_store.get_collection_info()
    print(f"✓ 向量資料庫已載入")
    print(f"  集合名稱: {info['name']}")
    print(f"  文件數量: {info['count']}")
    
    if info['count'] == 0:
        print("\n⚠️  向量資料庫是空的！")
        print("請先執行: python scripts\\load_data.py")
        return
    
    print("\n初始化問答引擎...")
    qa_engine = QAEngine(vector_store)
    print("✓ 問答引擎已就緒")
    
    # 測試問題列表
    test_questions = [
        "水稻的種植季節是什麼時候？",
        "如何防治番茄的病蟲害？",
        "有機肥料有哪些種類？",
        "葡萄需要怎麼修剪？",
        "溫室栽培要注意什麼？"
    ]
    
    print("\n" + "=" * 60)
    print("開始測試")
    print("=" * 60)
    
    # 測試模式選擇
    print("\n請選擇測試模式：")
    print("1. 自動測試（使用預設問題）")
    print("2. 互動測試（輸入自己的問題）")
    
    choice = input("\n請選擇 (1/2): ").strip()
    
    if choice == "1":
        # 自動測試
        for i, question in enumerate(test_questions, 1):
            print(f"\n{'=' * 60}")
            print(f"測試 {i}/{len(test_questions)}")
            print(f"{'=' * 60}")
            print(f"問題: {question}")
            print(f"{'-' * 60}")
            
            result = qa_engine.answer_question(question)
            print(f"回答: {result['answer']}")
            print(f"\n參考來源:")
            for j, source in enumerate(result['sources'][:2], 1):
                print(f"  {j}. {source['source']}")
            
            input("\n按 Enter 繼續下一題...")
    
    else:
        # 互動測試
        print("\n" + "=" * 60)
        print("互動測試模式（輸入 'exit' 或 'quit' 結束）")
        print("=" * 60)
        
        while True:
            question = input("\n請輸入問題: ").strip()
            
            if question.lower() in ['exit', 'quit', '結束', '退出']:
                print("測試結束，謝謝使用！")
                break
            
            if not question:
                continue
            
            print(f"\n{'-' * 60}")
            result = qa_engine.answer_question(question)
            print(f"回答: {result['answer']}")
            print(f"\n參考來源:")
            for i, source in enumerate(result['sources'][:2], 1):
                print(f"  {i}. {source['source']}")
            print(f"{'-' * 60}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程式已中斷")
    except Exception as e:
        print(f"\n錯誤: {e}")
        import traceback
        traceback.print_exc()
