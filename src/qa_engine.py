"""
問答引擎 - 整合 RAG (檢索增強生成)
"""
from typing import List, Dict, Any
from groq import Groq
from config import Config
from prompts import Prompts


class QAEngine:
    """問答引擎"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.LLM_MODEL
        # 使用集中管理的提示詞
        self.prompts = Prompts
    
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
        
        # 使用集中管理的提示詞
        prompt = self.prompts.QA_USER_PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )

        try:
            # 呼叫 Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompts.QA_SYSTEM_PROMPT},
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
