"""
向量資料庫管理 - 使用 ChromaDB
"""
import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from config import Config


class VectorStore:
    """向量資料庫管理器"""
    
    def __init__(self, persist_directory: str = None, collection_name: str = None):
        self.persist_directory = persist_directory or Config.VECTOR_DB_PATH
        self.collection_name = collection_name or Config.COLLECTION_NAME
        
        # 建立持久化資料夾
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # 初始化 ChromaDB (使用 PersistentClient)
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 載入嵌入模型
        print(f"載入嵌入模型: {Config.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # 取得或建立集合
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"✓ 載入現有集合: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "農業知識向量資料庫"}
            )
            print(f"✓ 建立新集合: {self.collection_name}")
    
    def add_documents(self, documents: List[Any], batch_size: int = 100):
        """
        新增文件到向量資料庫
        
        Args:
            documents: 文件列表 (Document 物件)
            batch_size: 批次處理大小
        """
        if not documents:
            print("沒有文件需要新增")
            return
        
        print(f"\n開始新增 {len(documents)} 個文件到向量資料庫...")
        
        # 批次處理
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # 提取內容和元資料
            contents = [doc.content for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            ids = [f"doc_{i + j}" for j in range(len(batch))]
            
            # 生成嵌入向量
            embeddings = self.embedding_model.encode(contents).tolist()
            
            # 新增到 ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=contents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"  已處理 {min(i + batch_size, len(documents))}/{len(documents)} 個文件")
        
        print("✓ 所有文件已新增完成")
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        搜尋相關文件
        
        Args:
            query: 查詢文字
            top_k: 返回前 K 個結果
            
        Returns:
            相關文件列表
        """
        if top_k is None:
            top_k = Config.TOP_K_RESULTS
        
        # 生成查詢向量
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # 搜尋
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        # 格式化結果
        documents = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                doc = {
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                }
                documents.append(doc)
        
        return documents
    
    def delete_collection(self):
        """刪除集合"""
        self.client.delete_collection(name=self.collection_name)
        print(f"✓ 已刪除集合: {self.collection_name}")
    
    def get_collection_info(self) -> Dict[str, Any]:
        """取得集合資訊"""
        count = self.collection.count()
        return {
            'name': self.collection_name,
            'count': count,
            'persist_directory': self.persist_directory
        }
    
    def test_search(self, query: str = "水稻種植"):
        """測試搜尋功能"""
        print(f"\n測試搜尋: '{query}'")
        results = self.search(query, top_k=3)
        
        print(f"\n找到 {len(results)} 個相關文件:\n")
        for i, doc in enumerate(results, 1):
            print(f"--- 文件 {i} (距離: {doc['distance']:.4f}) ---")
            print(f"內容: {doc['content'][:200]}...")
            print(f"來源: {doc['metadata'].get('source', 'unknown')}")
            print()
