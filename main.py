import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.request import HTTPXRequest
import httpx

from bot.gemini_client import GeminiClient
from bot.handlers import PCControlBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_proxy_config():
    """
    Create proxy configuration for SOCKS proxy
    
    Returns:
        dict: Proxy configuration or None if no proxy needed
    """
    proxy_host = os.getenv('PROXY_HOST', '').strip()
    proxy_port = os.getenv('PROXY_PORT', '').strip()
    proxy_username = os.getenv('PROXY_USERNAME', '').strip()
    proxy_password = os.getenv('PROXY_PASSWORD', '').strip()
    
    if not proxy_host or not proxy_port:
        logger.info("No proxy configuration found, connecting directly")
        return None
    
    try:
        proxy_port = int(proxy_port)
    except ValueError:
        logger.error(f"Invalid proxy port: {proxy_port}")
        return None
    
    # Build proxy URL
    if proxy_username and proxy_password:
        proxy_url = f"socks5://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
    else:
        proxy_url = f"socks5://{proxy_host}:{proxy_port}"
    
    logger.info(f"Using SOCKS proxy: {proxy_host}:{proxy_port}")
    return proxy_url

def main():
    """
    Main function to run the Telegram bot
    """
    # Get environment variables
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    pc_api_base_url = os.getenv('PC_API_BASE_URL')
    
    # Validate required environment variables
    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
        return
    
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY environment variable is required")
        return
    
    if not pc_api_base_url:
        logger.error("PC_API_BASE_URL environment variable is required")
        return
    
    try:
        # Initialize Gemini client
        gemini_client = GeminiClient(gemini_api_key)
        
        # Initialize PC control bot
        pc_bot = PCControlBot(gemini_client, pc_api_base_url)
        
        # Create proxy configuration
        proxy_url = create_proxy_config()
        
        # Create Telegram application with proxy support
        if proxy_url:
            # Create HTTP client with SOCKS proxy
            httpx_client = httpx.AsyncClient(
                proxies=proxy_url,
                timeout=httpx.Timeout(30.0)
            )
            request = HTTPXRequest(
                http_version="1.1",
                client=httpx_client
            )
            application = Application.builder().token(telegram_token).request(request).build()
        else:
            # Create application without proxy
            application = Application.builder().token(telegram_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", pc_bot.start_command))
        application.add_handler(CommandHandler("help", pc_bot.help_command))
        application.add_handler(CommandHandler("status", pc_bot.status_command))
        
        # Add message handler for regular messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pc_bot.handle_message))
        
        # Add error handler
        application.add_error_handler(pc_bot.error_handler)
        
        logger.info("PC Manager Telegram Bot started successfully")
        
        # Run the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        return

if __name__ == '__main__':
    main()