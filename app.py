from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('E0f9jATU39o6kjDOnwU/gWFU2MbpD6/jiCTTO1YfV4U9hed9GWp/OO6+wpo1B7U4ZHlzzY+1euftOsVcoHN2Yl1erNalWR4PUG1/UP05+qSgYzHdCAYqxcPTBX3PC8+8Q9dmfJDE+aNjUtuenIs8PgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c25577f53b890ad08f72f8d50a0496cd')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()