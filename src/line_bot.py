"""
LINE Bot 處理器
"""
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction
)
from config import Config


class LineBotHandler:
    """LINE Bot 處理器"""
    
    def __init__(self, qa_engine):
        self.qa_engine = qa_engine
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        
        # 註冊訊息處理器
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            self._handle_text_message(event)
    
    def _handle_text_message(self, event):
        """處理文字訊息"""
        user_message = event.message.text
        user_id = event.source.user_id
        
        print(f"收到使用者 {user_id} 的訊息: {user_message}")
        
        # 處理特殊指令
        if user_message.startswith('/'):
            self._handle_command(event, user_message)
            return
        
        # 一般問答
        try:
            # 使用 QA 引擎生成回答
            result = self.qa_engine.answer_question(user_message)
            answer = result['answer']
            
            # 傳送回答
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=answer)
            )
            
            print(f"已回覆使用者: {answer[:50]}...")
        
        except Exception as e:
            print(f"處理訊息錯誤: {e}")
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，處理您的問題時發生錯誤，請稍後再試。")
            )
    
    def _handle_command(self, event, command):
        """處理特殊指令"""
        if command == '/help' or command == '/說明':
            help_text = """🌾 農業知識庫 LINE Bot 使用說明

【基本功能】
直接輸入問題，我會從農業知識庫中搜尋相關資料並回答您。

【範例問題】
• 水稻的種植季節是什麼時候？
• 如何防治番茄的病蟲害？
• 有機肥料的使用方法
• 葡萄的修剪技巧
• 溫室栽培注意事項

【指令列表】
/help 或 /說明 - 顯示此說明
/about 或 /關於 - 關於本系統
/topics 或 /主題 - 顯示可查詢的主題

有任何農業相關問題都可以直接問我！"""
            
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=help_text)
            )
        
        elif command == '/about' or command == '/關於':
            about_text = """🌾 農業知識庫 LINE Bot

這是一個結合向量資料庫和 AI 的智能農業顧問系統。

【技術特色】
• 使用向量資料庫進行語義搜尋
• 整合大型語言模型生成專業回答
• 支援繁體中文對話
• 即時回應您的農業問題

【資料來源】
系統會從專業農業知識庫中檢索相關資料，提供準確可靠的資訊。

如有任何問題或建議，歡迎隨時提出！"""
            
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=about_text)
            )
        
        elif command == '/topics' or command == '/主題':
            topics_text = """📚 可查詢的農業主題

【作物栽培】
• 水稻種植
• 番茄栽培
• 蔬菜栽培
• 果樹管理

【農業技術】
• 有機農業
• 設施栽培
• 病蟲害防治
• 施肥管理

【專業知識】
• 植物營養
• 土壤管理
• 灌溉技術
• 採收後處理

直接輸入您想了解的主題或具體問題即可！"""
            
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=topics_text)
            )
        
        else:
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"未知的指令: {command}\n輸入 /help 查看可用指令")
            )
    
    def handle_webhook(self, body, signature):
        """
        處理 LINE Webhook
        
        Args:
            body: 請求內容
            signature: 簽名
            
        Returns:
            是否處理成功
        """
        try:
            self.handler.handle(body, signature)
            return True
        except InvalidSignatureError:
            print("Invalid signature")
            return False
        except Exception as e:
            print(f"Webhook 處理錯誤: {e}")
            return False
    
    def push_message(self, user_id, message):
        """
        主動推送訊息給使用者
        
        Args:
            user_id: 使用者 ID
            message: 訊息內容
        """
        try:
            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=message)
            )
            print(f"已推送訊息給使用者 {user_id}")
        except Exception as e:
            print(f"推送訊息錯誤: {e}")
