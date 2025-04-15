from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from commands.rang import handle_rang
from settings import dev
import os

app = Flask(__name__)

line_bot_api = LineBotApi(dev.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(dev.CHANNEL_SECRET)

@app.route('/')
def health_check():
    return 'healthy'

@app.route("/check-rang", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message.lower() == "/rang":
        response = handle_rang()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
