"""
設定檔 - 管理環境變數和應用程式設定
"""
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Config:
    """應用程式設定"""
    
    # LINE Bot 設定
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
    
    # Groq 設定
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # 向量資料庫設定
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './vector_db')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'agriculture_qa')
    
    # 文件資料夾
    DATA_PATH = './data/agriculture'
    
    # 伺服器設定
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # 測試端點設定（建議生產環境不啟用）
    ENABLE_TEST_ENDPOINT = os.getenv('ENABLE_TEST_ENDPOINT', 'False').lower() == 'true'
    TEST_API_KEY = os.getenv('TEST_API_KEY', 'dev-test-key-change-in-production')
    
    # 模型設定
    EMBEDDING_MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    LLM_MODEL = 'llama-3.3-70b-versatile'  # Groq 的最新模型
    
    # RAG 設定
    TOP_K_RESULTS = 3  # 檢索前 K 個最相關的文件
    MAX_TOKENS = 500   # LLM 回答的最大 token 數
    TEMPERATURE = 0.7   # LLM 生成的溫度參數
