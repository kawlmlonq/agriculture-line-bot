"""
LINE Bot 處理器
"""
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    QuickReply, QuickReplyButton, MessageAction
)
from config import Config
from prompts import Prompts
from src.image_analyzer import ImageAnalyzer
import requests


class LineBotHandler:
    """LINE Bot 處理器"""
    
    def __init__(self, qa_engine):
        self.qa_engine = qa_engine
        self.image_analyzer = ImageAnalyzer()
        self.line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        self.prompts = Prompts  # 使用集中管理的提示詞
        
        # 儲存使用者最後上傳的圖片（簡單實現，實際應用可用資料庫）
        self.user_images = {}
        
        # 註冊文字訊息處理器
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            self._handle_text_message(event)
        
        # 註冊圖片訊息處理器
        @self.handler.add(MessageEvent, message=ImageMessage)
        def handle_image_message(event):
            self._handle_image_message(event)
    
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
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=self.prompts.HELP_MESSAGE)
            )
        
        elif command == '/about' or command == '/關於':
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=self.prompts.ABOUT_MESSAGE)
            )
        
        elif command == '/topics' or command == '/主題':
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=self.prompts.TOPICS_MESSAGE)
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
    
    def _handle_image_message(self, event):
        """處理圖片訊息"""
        user_id = event.source.user_id
        message_id = event.message.id
        
        print(f"收到使用者 {user_id} 的圖片訊息 (ID: {message_id})")
        
        try:
            # 先回覆使用者正在處理
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=self.prompts.IMAGE_PROCESSING)
            )
            
            # 下載圖片
            print(f"開始下載圖片 {message_id}")
            message_content = self.line_bot_api.get_message_content(message_id)
            
            image_content = b''
            chunk_count = 0
            for chunk in message_content.iter_content(chunk_size=1024):
                image_content += chunk
                chunk_count += 1
            
            print(f"圖片下載完成：{len(image_content)} bytes，{chunk_count} chunks")
            
            # 檢查圖片大小
            if len(image_content) == 0:
                raise ValueError("下載的圖片內容為空")
            
            if len(image_content) > 20 * 1024 * 1024:  # 20MB
                self.line_bot_api.push_message(
                    user_id,
                    TextSendMessage(text="⚠️ 圖片太大了！請傳送小於 20MB 的圖片。")
                )
                return
            
            # 儲存圖片內容（供後續文字問題使用）
            self.user_images[user_id] = image_content
            
            # 使用圖像分析器分析
            print(f"開始分析圖片...")
            analysis_result = self.image_analyzer.analyze_agriculture_image(image_content)
            print(f"分析完成，結果長度: {len(analysis_result)}")
            
            # 傳送分析結果
            response_message = f"{self.prompts.IMAGE_RESULT_PREFIX}{analysis_result}{self.prompts.IMAGE_RESULT_SUFFIX}"
            
            # 檢查訊息長度（LINE 限制 5000 字元）
            if len(response_message) > 4500:
                response_message = response_message[:4500] + "\n\n... (內容過長已截斷)"
            
            self.line_bot_api.push_message(
                user_id,
                TextSendMessage(text=response_message)
            )
            
            print(f"圖片分析完成並回覆使用者")
            
        except Exception as e:
            error_msg = f"圖片處理失敗：{str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            
            # 提供更友善的錯誤訊息
            user_message = "抱歉，圖片分析時發生錯誤。"
            
            if "download" in str(e).lower() or "content" in str(e).lower():
                user_message += "\n\n可能原因：無法下載圖片。請重新傳送。"
            elif "timeout" in str(e).lower():
                user_message += "\n\n可能原因：處理超時。請嘗試傳送較小的圖片。"
            elif "format" in str(e).lower():
                user_message += "\n\n可能原因：圖片格式不支援。請傳送 JPG 或 PNG 格式。"
            else:
                user_message += f"\n\n錯誤訊息：{str(e)[:100]}"
            
            try:
                self.line_bot_api.push_message(
                    user_id,
                    TextSendMessage(text=user_message)
                )
            except:
                print("無法傳送錯誤訊息給使用者")
    
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
