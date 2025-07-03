import os
import logging
import requests
from typing import Dict, Any
from telegram import Update
from telegram.ext import ContextTypes

from .gemini_client import GeminiClient

logger = logging.getLogger(__name__)

class PCControlBot:
    def __init__(self, gemini_client: GeminiClient, pc_api_base_url: str):
        """
        Initialize PC Control Bot
        
        Args:
            gemini_client: Gemini client instance
            pc_api_base_url: Base URL for PC API
        """
        self.gemini_client = gemini_client
        self.pc_api_base_url = pc_api_base_url.rstrip('/')
        logger.info(f"PC Control Bot initialized with API base URL: {self.pc_api_base_url}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle /start command
        """
        user = update.effective_user
        welcome_message = f"""
🖥️ **Chào mừng {user.first_name}!**

Tôi là bot điều khiển máy tính cá nhân của bạn. Tôi có thể:

🔵 **Bật máy tính** - Gửi: "bật máy tính", "mở máy", "turn on pc"
🔴 **Tắt máy tính** - Gửi: "tắt máy tính", "shutdown", "turn off pc"
📊 **Kiểm tra trạng thái** - Gửi: "kiểm tra máy tính", "trạng thái", "status"

Bạn cũng có thể chat bình thường với tôi! 😊

Hãy gửi tin nhắn để bắt đầu điều khiển máy tính của bạn.
"""
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle /help command
        """
        help_message = """
🆘 **Hướng dẫn sử dụng:**

**Các lệnh điều khiển máy tính:**
• Bật máy: "bật máy tính", "mở máy", "khởi động máy"
• Tắt máy: "tắt máy tính", "shutdown", "tắt nguồn"
• Kiểm tra: "kiểm tra máy tính", "trạng thái máy", "pc status"

**Các lệnh bot:**
• /start - Bắt đầu sử dụng bot
• /help - Hiển thị hướng dẫn này
• /status - Kiểm tra trạng thái máy tính

**Lưu ý:**
• Bạn có thể chat bình thường với bot
• Bot sẽ tự động nhận diện ý định điều khiển máy tính
• Hỗ trợ cả tiếng Việt và tiếng Anh
"""
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle /status command - check PC status
        """
        try:
            status_response = await self._check_pc_status()
            await update.message.reply_text(status_response)
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text("❌ Không thể kiểm tra trạng thái máy tính lúc này.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle regular messages from users
        """
        user_message = update.message.text
        user = update.effective_user
        
        logger.info(f"Received message from {user.first_name} ({user.id}): {user_message}")
        
        try:
            # Analyze message with Gemini
            analysis_result = await self.gemini_client.analyze_message(user_message)
            
            if analysis_result["type"] == "function_call":
                # Execute PC control function
                function_name = analysis_result["function_name"]
                response = await self._execute_pc_function(function_name)
                await update.message.reply_text(response)
                
            elif analysis_result["type"] == "natural_response":
                # Send natural response
                response = analysis_result["response"]
                await update.message.reply_text(response)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text("❌ Xin lỗi, đã xảy ra lỗi khi xử lý tin nhắn của bạn.")
    
    async def _execute_pc_function(self, function_name: str) -> str:
        """
        Execute PC control function based on function name
        
        Args:
            function_name: Name of the function to execute
            
        Returns:
            Response message
        """
        try:
            if function_name == "turn_on_pc":
                return await self._turn_on_pc()
            elif function_name == "turn_off_pc":
                return await self._turn_off_pc()
            elif function_name == "check_pc_status":
                return await self._check_pc_status()
            else:
                return "❌ Chức năng không được hỗ trợ."
                
        except Exception as e:
            logger.error(f"Error executing PC function {function_name}: {e}")
            return f"❌ Lỗi khi thực hiện chức năng {function_name}."
    
    async def _turn_on_pc(self) -> str:
        """
        Turn on PC via API
        
        Returns:
            Response message
        """
        try:
            url = f"{self.pc_api_base_url}/turn-on"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                logger.info("PC turned on successfully")
                return "✅ Máy tính đã được bật thành công!"
            else:
                logger.error(f"Failed to turn on PC: {response.status_code}")
                return f"❌ Không thể bật máy tính. Mã lỗi: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error turning on PC: {e}")
            return "❌ Không thể kết nối đến máy tính. Vui lòng kiểm tra kết nối mạng."
    
    async def _turn_off_pc(self) -> str:
        """
        Turn off PC via API
        
        Returns:
            Response message
        """
        try:
            url = f"{self.pc_api_base_url}/turn-off"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                logger.info("PC turned off successfully")
                return "✅ Máy tính đã được tắt thành công!"
            else:
                logger.error(f"Failed to turn off PC: {response.status_code}")
                return f"❌ Không thể tắt máy tính. Mã lỗi: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error turning off PC: {e}")
            return "❌ Không thể kết nối đến máy tính. Vui lòng kiểm tra kết nối mạng."
    
    async def _check_pc_status(self) -> str:
        """
        Check PC status via API
        
        Returns:
            Response message
        """
        try:
            url = f"{self.pc_api_base_url}/is-online"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Assume API returns JSON with online status
                try:
                    data = response.text
                    is_online = data == "true"
                    
                    if is_online:
                        logger.info("PC is online")
                        return "🟢 Máy tính đang hoạt động (Online)"
                    else:
                        logger.info("PC is offline")
                        return "🔴 Máy tính đang tắt (Offline)"
                        
                except ValueError:
                    # If response is not JSON, assume plain text
                    if "online" in response.text.lower() or "true" in response.text.lower():
                        return "🟢 Máy tính đang hoạt động (Online)"
                    else:
                        return "🔴 Máy tính đang tắt (Offline)"
            else:
                logger.error(f"Failed to check PC status: {response.status_code}")
                return f"❌ Không thể kiểm tra trạng thái máy tính. Mã lỗi: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error checking PC status: {e}")
            return "❌ Không thể kết nối đến máy tính. Vui lòng kiểm tra kết nối mạng."
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle errors that occur during bot operation
        """
        logger.error(f"Exception while handling an update: {context.error}")
        
        if update and hasattr(update, 'message') and update.message:
            await update.message.reply_text(
                "❌ Đã xảy ra lỗi không mong muốn. Vui lòng thử lại sau."
            )