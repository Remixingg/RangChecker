
from flask import Blueprint, request, abort, current_app
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from ..services import process_command
from ..services import line_service

line_webhook_bp = Blueprint('line_webhook', __name__)
line_handler = None

@line_webhook_bp.record
def on_register(state):
    global line_handler
    app = state.app
    secret = app.config.get('CHANNEL_SECRET')
    
    if not secret:
        app.logger.warning("LINE CHANNEL_SECRET not configured")
        return
        
    line_handler = WebhookHandler(secret)
    app.logger.info("LINE webhook handler initialized")
    
    @line_handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        """Handle text messages from LINE."""
        user_message = event.message.text.strip()
        
        # Process the command
        response = process_command(user_message)
        if response:
            line_service.send_reply(event.reply_token, response)


@line_webhook_bp.route('/line', methods=['POST'])
def line_webhook():
    global line_handler
    
    if not line_handler:
        current_app.logger.error("LINE webhook handler not initialized")
        abort(500)
    
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        current_app.logger.warning("Missing X-Line-Signature header")
        abort(400)
    
    body = request.get_data(as_text=True)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        current_app.logger.warning("Invalid LINE webhook signature")
        abort(400)
    
    return 'OK'
