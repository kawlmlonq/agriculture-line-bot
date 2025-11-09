"""
圖像分析引擎 - 使用 Groq Vision API
"""
import base64
import io
from groq import Groq
from config import Config
from prompts import Prompts
from PIL import Image


class ImageAnalyzer:
    """圖像分析器 - 用於分析農業相關圖片"""
    
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.vision_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        # 使用集中管理的提示詞
        self.prompts = Prompts
    
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
        如果圖片太大就縮小，並確保格式正確
        
        Args:
            image_content: 原始圖片內容
            max_size: 最大尺寸（寬或高）
            
        Returns:
            處理後的圖片內容
        """
        try:
            image = Image.open(io.BytesIO(image_content))
            print(f"原始圖片: {image.format}, 大小: {image.width}x{image.height}, 模式: {image.mode}")
            
            # 轉換為 RGB 模式（如果不是）
            if image.mode not in ('RGB', 'RGBA'):
                print(f"轉換圖片模式從 {image.mode} 到 RGB")
                image = image.convert('RGB')
            elif image.mode == 'RGBA':
                # 將 RGBA 轉換為 RGB（移除透明度）
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background
            
            # 檢查是否需要縮小
            if image.width > max_size or image.height > max_size:
                ratio = min(max_size / image.width, max_size / image.height)
                new_size = (int(image.width * ratio), int(image.height * ratio))
                print(f"縮小圖片從 {image.width}x{image.height} 到 {new_size[0]}x{new_size[1]}")
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # 統一輸出為 JPEG 格式
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85)
            result = output.getvalue()
            print(f"處理後圖片大小: {len(result)} bytes")
            return result
            
        except Exception as e:
            print(f"圖片處理錯誤: {e}")
            import traceback
            traceback.print_exc()
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
            print(f"開始分析圖片，原始大小: {len(image_content)} bytes")
            
            # 檢查圖片大小
            if len(image_content) == 0:
                return "錯誤：收到的圖片內容為空。"
            
            if len(image_content) > 10 * 1024 * 1024:  # 10MB
                print(f"警告：圖片過大 ({len(image_content)} bytes)，將會縮小")
            
            # 縮小圖片（如果需要）
            image_content = self.resize_image_if_needed(image_content, max_size=800)
            
            # 編碼圖片
            base64_image = self.encode_image(image_content)
            print(f"Base64 編碼長度: {len(base64_image)}")
            
            # 使用集中管理的提示詞
            if user_question:
                prompt = self.prompts.IMAGE_ANALYSIS_WITH_QUESTION.format(question=user_question)
            else:
                prompt = self.prompts.IMAGE_ANALYSIS_GENERAL
            
            print(f"呼叫 Groq Vision API，模型: {self.vision_model}")
            
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
            
            result = response.choices[0].message.content
            print(f"API 回應成功，回答長度: {len(result)}")
            return result
            
        except Exception as e:
            error_msg = f"圖片分析發生錯誤: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            
            # 根據錯誤類型提供更具體的訊息
            if "rate_limit" in str(e).lower():
                return "抱歉，API 使用量已達上限。請稍後再試。"
            elif "invalid" in str(e).lower() or "format" in str(e).lower():
                return "抱歉，圖片格式可能不支援。請嘗試傳送 JPG 或 PNG 格式的圖片。"
            elif "timeout" in str(e).lower():
                return "抱歉，分析超時。請嘗試傳送較小的圖片。"
            else:
                return f"抱歉，圖片分析時發生錯誤。\n\n技術細節：{str(e)[:100]}"
    
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
            
            # 使用集中管理的提示詞
            prompt = self.prompts.IMAGE_QUICK_IDENTIFY
            
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
