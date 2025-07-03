import os
import logging
import google.generativeai as genai
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, api_key: str):
        """
        Initialize Gemini client with API key
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Define PC control functions for Gemini
        self.functions = [
            {
                "name": "turn_on_pc",
                "description": "Bật máy tính cá nhân."
            },
            {
                "name": "turn_off_pc", 
                "description": "Tắt máy tính cá nhân."
            },
            {
                "name": "check_pc_status",
                "description": "Kiểm tra trạng thái máy tính (online/offline)."
            }
        ]
        
        logger.info("Gemini client initialized successfully")
    
    async def analyze_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze user message to determine intent and extract function calls
        
        Args:
            message: User message to analyze
            
        Returns:
            Dict containing either function_call or natural_response
        """
        try:
            # Create a prompt that includes function definitions
            prompt = f"""
Bạn là một AI assistant điều khiển máy tính cá nhân. Phân tích tin nhắn sau và xác định xem người dùng muốn thực hiện hành động nào:

Tin nhắn: "{message}"

Các hành động có thể thực hiện:
1. turn_on_pc: Bật máy tính (các từ khóa: bật, mở, khởi động, turn on, start, power on)
2. turn_off_pc: Tắt máy tính (các từ khóa: tắt, đóng, shutdown, turn off, power off)
3. check_pc_status: Kiểm tra trạng thái máy tính (các từ khóa: kiểm tra, trạng thái, status, check)

Nếu tin nhắn có ý định thực hiện một trong 3 hành động trên, hãy trả lời CHÍNH XÁC với format:
FUNCTION_CALL: [tên_function]

Nếu không phải 3 hành động trên, hãy trả lời tự nhiên như một AI assistant thông thường.
"""
            
            # Generate response
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            logger.info(f"Gemini response: {response_text}")
            
            # Check if response contains function call
            if response_text.startswith("FUNCTION_CALL:"):
                function_name = response_text.replace("FUNCTION_CALL:", "").strip()
                
                # Validate function name
                valid_functions = ["turn_on_pc", "turn_off_pc", "check_pc_status"]
                if function_name in valid_functions:
                    return {
                        "type": "function_call",
                        "function_name": function_name
                    }
                else:
                    logger.warning(f"Invalid function name: {function_name}")
                    return {
                        "type": "natural_response",
                        "response": "Xin lỗi, tôi không hiểu yêu cầu của bạn. Hãy thử lại."
                    }
            else:
                # Natural response
                return {
                    "type": "natural_response", 
                    "response": response_text
                }
                
        except Exception as e:
            logger.error(f"Error analyzing message with Gemini: {e}")
            return {
                "type": "natural_response",
                "response": "Xin lỗi, đã xảy ra lỗi khi xử lý tin nhắn của bạn."
            }
    
    async def generate_natural_response(self, message: str) -> str:
        """
        Generate natural language response for general conversation
        
        Args:
            message: User message
            
        Returns:
            Natural language response
        """
        try:
            prompt = f"""
Bạn là một AI assistant thân thiện hỗ trợ điều khiển máy tính cá nhân. 
Hãy trả lời tin nhắn sau một cách tự nhiên và hữu ích:

Tin nhắn: "{message}"

Trả lời bằng tiếng Việt một cách thân thiện và hữu ích.
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating natural response: {e}")
            return "Xin lỗi, tôi không thể trả lời tin nhắn của bạn lúc này."