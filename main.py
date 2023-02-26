#coding=utf8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import configparser


# LINE 聊天機器人的基本資料
config = configparser.ConfigParser() 
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

#資料庫連接
import pymssql
conn = pymssql.connect(
    server='DESKTOP-TS38KVS\SQLEXPRESS'
    , user='Alan'
    , password='0415061094'
    , database='iLearningSystem'
)
cursor = conn.cursor()

app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #echo
    msg= event.message.text
    message = TextSendMessage(text=msg)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)