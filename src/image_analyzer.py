"""
圖像分析引擎 - 使用 Groq Vision API
"""
import base64
import io
from groq import Groq
from config import Config
from PIL import Image


class ImageAnalyzer:
    """圖像分析器 - 用於分析農業相關圖片"""
    
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.vision_model = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    def encode_image(self, image_content: bytes) -> str:
        """
        將圖片編碼為 base64
        
        Args:
            image_content: 圖片的二進制內容
            
        Returns:
            base64 編碼的圖片字串
        """
        return base64.b64encode(image_content).decode('utf-8')
    
    def resize_image_if_needed(self, image_content: bytes, max_size: int = 1024) -> bytes:
        """
        如果圖片太大就縮小
        
        Args:
            image_content: 原始圖片內容
            max_size: 最大尺寸（寬或高）
            
        Returns:
            處理後的圖片內容
        """
        try:
            image = Image.open(io.BytesIO(image_content))
            
            # 檢查是否需要縮小
            if image.width > max_size or image.height > max_size:
                # 計算縮放比例
                ratio = min(max_size / image.width, max_size / image.height)
                new_size = (int(image.width * ratio), int(image.height * ratio))
                
                # 縮小圖片
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                
                # 轉換回 bytes
                output = io.BytesIO()
                image.save(output, format=image.format or 'JPEG')
                return output.getvalue()
            
            return image_content
        except Exception as e:
            print(f"圖片處理錯誤: {e}")
            return image_content
    
    def analyze_agriculture_image(self, image_content: bytes, user_question: str = None) -> str:
        """
        分析農業相關圖片
        
        Args:
            image_content: 圖片的二進制內容
            user_question: 使用者的問題（選填）
            
        Returns:
            分析結果文字
        """
        try:
            # 縮小圖片（如果需要）
            image_content = self.resize_image_if_needed(image_content)
            
            # 編碼圖片
            base64_image = self.encode_image(image_content)
            
            # 建立提示詞
            if user_question:
                prompt = f"""你是一位專業的農業專家。請仔細分析這張圖片並回答使用者的問題。

使用者的問題：{user_question}

請提供：
1. 圖片內容的描述
2. 針對問題的專業分析和建議
3. 如果是病蟲害，請說明可能的原因和處理方法
4. 如果是作物，請評估生長狀況

請用繁體中文回答，內容要專業且實用。"""
            else:
                prompt = """你是一位專業的農業專家。請仔細分析這張農業相關的圖片。

請提供以下資訊：
1. **圖片內容**：描述看到什麼（植物、作物、病蟲害等）
2. **狀態評估**：評估植物或作物的健康狀況
3. **問題診斷**：如果有問題，指出可能的病蟲害或其他問題
4. **建議措施**：提供具體的改善建議或處理方法
5. **預防建議**：如何預防類似問題

請用繁體中文回答，內容要專業且實用。"""
            
            # 呼叫 Groq Vision API
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"圖片分析發生錯誤: {str(e)}"
            print(error_msg)
            return f"抱歉，圖片分析時發生錯誤。請確保圖片清晰可見，然後再試一次。\n\n錯誤訊息：{str(e)}"
    
    def quick_identify(self, image_content: bytes) -> str:
        """
        快速識別圖片內容
        
        Args:
            image_content: 圖片的二進制內容
            
        Returns:
            簡短的識別結果
        """
        try:
            image_content = self.resize_image_if_needed(image_content)
            base64_image = self.encode_image(image_content)
            
            prompt = "請用一句話簡短描述這張圖片的主要內容。如果是植物或作物，請說明種類。用繁體中文回答。"
            
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.5,
                max_tokens=100
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"識別失敗：{str(e)}"
