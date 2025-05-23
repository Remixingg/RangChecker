from linebot import LineBotApi
from linebot.models import TextSendMessage
from flask import current_app

class LineService:

    def __init__(self):
        self.line_bot_api = None
        
    def initialize(self, app):
        token = app.config.get('CHANNEL_ACCESS_TOKEN')
        if not token:
            app.logger.warning("LINE CHANNEL_ACCESS_TOKEN not configured")
            return
        
        self.line_bot_api = LineBotApi(token)
        app.logger.info("LINE API client initialized")
    
    def send_reply(self, reply_token, response_payload):
        if not self.line_bot_api:
            current_app.logger.error("LINE API client not initialized")
            return False
            
        # convert to LINE format
        if response_payload["type"] == "text":
            messages = [TextSendMessage(text=response_payload["text"])]
            
            try:
                self.line_bot_api.reply_message(reply_token, messages)
                return True
            except Exception as e:
                current_app.logger.error(f"Error sending LINE reply: {str(e)}")
                return False
        else:
            current_app.logger.warning(f"Unsupported message type: {response_payload['type']}")
            return False


line_service = LineService()