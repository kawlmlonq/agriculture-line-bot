"""
問答引擎 - 整合 RAG (檢索增強生成)
"""
from typing import List, Dict, Any
from groq import Groq
from config import Config


class QAEngine:
    """問答引擎"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.LLM_MODEL
    
    def generate_answer(self, question: str, context_docs: List[Dict[str, Any]]) -> str:
        """
        使用 LLM 生成回答
        
        Args:
            question: 使用者問題
            context_docs: 相關文件列表
            
        Returns:
            生成的回答
        """
        # 組合上下文
        context = "\n\n".join([
            f"[參考資料 {i+1}]\n{doc['content']}"
            for i, doc in enumerate(context_docs)
        ])
        
        # 建立提示詞
        prompt = f"""你是一位專業的農業顧問，請根據以下參考資料回答使用者的問題。

參考資料：
{context}

使用者問題：{question}

請根據上述參考資料提供專業、準確的回答。如果參考資料中沒有相關資訊，請誠實說明。回答要清楚、具體，並使用繁體中文。"""

        try:
            # 呼叫 Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位專業的農業顧問，擅長回答各種農業相關問題。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            answer = response.choices[0].message.content.strip()
            return answer
        
        except Exception as e:
            print(f"LLM 生成錯誤: {e}")
            return "抱歉，我現在無法生成回答，請稍後再試。"
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        完整的問答流程
        
        Args:
            question: 使用者問題
            
        Returns:
            包含回答和來源的字典
        """
        # 1. 從向量資料庫檢索相關文件
        print(f"🔍 搜尋相關資料: {question}")
        relevant_docs = self.vector_store.search(question)
        
        if not relevant_docs:
            return {
                'answer': "抱歉，我在資料庫中找不到相關資訊。請嘗試換個方式提問。",
                'sources': []
            }
        
        # 2. 使用 LLM 生成回答
        print(f"🤖 生成回答...")
        answer = self.generate_answer(question, relevant_docs)
        
        # 3. 整理來源資訊
        sources = []
        for doc in relevant_docs:
            source_info = {
                'source': doc['metadata'].get('source', 'unknown'),
                'snippet': doc['content'][:100] + '...' if len(doc['content']) > 100 else doc['content']
            }
            sources.append(source_info)
        
        return {
            'answer': answer,
            'sources': sources
        }
    
    def answer_question_simple(self, question: str) -> str:
        """
        簡化版問答（直接返回答案文字）
        
        Args:
            question: 使用者問題
            
        Returns:
            回答文字
        """
        result = self.answer_question(question)
        return result['answer']
