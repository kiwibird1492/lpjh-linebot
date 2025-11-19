# app.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    PostbackEvent
)

from utils import detect_category
from crawler import search_school
from flex import flex_main_menu, flex_article_list

import os

app = Flask(__name__)

# ---------------------------------------------------------
# 👉 填入你自己的 Channel Secret / Access Token
# ---------------------------------------------------------
CHANNEL_ACCESS_TOKEN = "Km98R7jo9qa8ne8eBniDIRIEwQ2De0CAj7E8EKQam8ib2NwiYv/mdQ8VY2nA3dO96aFA0a1w8Wr3ZNcPFQyVG8cSaTKygfaJoOHWhSwVf1km13rqruY9oADAl1YNxJ6JMmQ1/IZDtVXnP68XYL7vuwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "46462ff62aa2638260553fa5a8a86eaf"
# ---------------------------------------------------------

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


# ---------------------------------------------------------
# Webhook 主入口
# ---------------------------------------------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


# ---------------------------------------------------------
# 1️⃣ 文字訊息（關鍵字分類 + 搜尋）
# ---------------------------------------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_text = event.message.text.strip()

    # 若使用者輸入 "選單" → 顯示主選單
    if user_text in ["選單", "menu", "Menu", "主選單"]:
        line_bot_api.reply_message(
            event.reply_token,
            flex_main_menu()
        )
        return

    # 自動判斷分類
    category = detect_category(user_text)

    # 搜尋資料
    items = search_school(category, keyword=user_text)

    # 回傳 Flex 結果卡片
    line_bot_api.reply_message(
        event.reply_token,
        flex_article_list(category, items)
    )


# ---------------------------------------------------------
# 2️⃣ Postback（按按鈕選擇分類）
# ---------------------------------------------------------
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data

    if data.startswith("category="):
        category = data.replace("category=", "")

        items = search_school(category)

        line_bot_api.reply_message(
            event.reply_token,
            flex_article_list(category, items)
        )


# ---------------------------------------------------------
# 主程式（本機測試）
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
