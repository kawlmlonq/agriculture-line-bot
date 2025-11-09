"""
Flask 主應用程式 - LINE Bot 伺服器
"""
from flask import Flask, request, abort
from config import Config
from src.vector_store import VectorStore
from src.qa_engine import QAEngine
from src.line_bot import LineBotHandler

# 初始化 Flask 應用
app = Flask(__name__)

# 初始化向量資料庫和 QA 引擎
print("🚀 初始化系統...")
vector_store = VectorStore()
qa_engine = QAEngine(vector_store)
line_bot_handler = LineBotHandler(qa_engine)

print(f"✓ 向量資料庫已載入: {vector_store.get_collection_info()['count']} 個文件")
print(f"✓ LINE Bot 已就緒")


@app.route("/")
def home():
    """首頁"""
    return """
    <h1>🌾 農業知識庫 LINE Bot</h1>
    <p>系統運行中...</p>
    <ul>
        <li>向量資料庫文件數: {}</li>
        <li>狀態: 正常運行</li>
    </ul>
    <p>請透過 LINE 加入 Bot 開始使用</p>
    """.format(vector_store.get_collection_info()['count'])


@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook 回調"""
    # 取得 X-Line-Signature header
    signature = request.headers.get('X-Line-Signature', '')
    
    # 取得請求內容
    body = request.get_data(as_text=True)
    
    # 處理 webhook
    if not line_bot_handler.handle_webhook(body, signature):
        abort(400)
    
    return 'OK'


@app.route("/health")
def health():
    """健康檢查"""
    try:
        info = vector_store.get_collection_info()
        return {
            'status': 'healthy',
            'vector_db': {
                'collection': info['name'],
                'documents': info['count']
            }
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }, 500


@app.route("/test", methods=['POST'])
def test_qa():
    """
    測試問答功能（開發用）
    
    安全提示：
    - 生產環境請在 .env 設定 ENABLE_TEST_ENDPOINT=False 停用此端點
    - 或設定 TEST_API_KEY 並在請求中加入 X-API-Key header
    """
    # 檢查是否啟用測試端點
    if not Config.ENABLE_TEST_ENDPOINT:
        abort(404)  # 生產環境返回 404，讓攻擊者以為端點不存在
    
    # 如果有設定 TEST_API_KEY（不是預設值），則需要驗證
    if Config.TEST_API_KEY != 'dev-test-key-change-in-production':
        api_key = request.headers.get('X-API-Key')
        if api_key != Config.TEST_API_KEY:
            print(f"⚠️  未授權的測試端點存取嘗試：{request.remote_addr}")
            abort(401, description='Unauthorized: Invalid API Key')
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return {'error': 'No question provided'}, 400
    
    try:
        result = qa_engine.answer_question(question)
        return {
            'question': question,
            'answer': result['answer'],
            'sources': result['sources']
        }
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌾 農業知識庫 LINE Bot 伺服器")
    print("=" * 60)
    print(f"伺服器位址: http://localhost:{Config.PORT}")
    print(f"Webhook URL: http://localhost:{Config.PORT}/callback")
    print(f"健康檢查: http://localhost:{Config.PORT}/health")
    print("=" * 60 + "\n")
    
    # 啟動 Flask 應用 (關閉 debug 避免重啟問題)
    # 支援雲端部署（從環境變數讀取 PORT）
    import os
    port = int(os.getenv('PORT', Config.PORT))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
