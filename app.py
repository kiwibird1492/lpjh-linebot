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
# 👉 在這裡填入自己的 Channel Access Token / Secret
# ---------------------------------------------------------
CHANNEL_ACCESS_TOKEN = "你的_LINE_CHANNEL_ACCESS_TOKEN"
CHANNEL_SECRET = "你的_LINE_CHANNEL_SECRET"
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
# 1️⃣ 文字訊息（查詢 + 顯示主選單）
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

    # 根據輸入文字自動判斷分類
    category = detect_category(user_text)

    # 搜尋該分類
    items = search_school(category, keyword=user_text)

    # 回傳 Flex 結果卡片
    line_bot_api.reply_message(
        event.reply_token,
        flex_article_list(category, items)
    )


# ---------------------------------------------------------
# 2️⃣ 按鈕按下（postback）事件 → 搜尋該分類
# ---------------------------------------------------------
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data  # 例如 "category=校務布告欄"

    if data.startswith("category="):
        category = data.replace("category=", "")

        # 搜尋資料
        items = search_school(category)

        # 回覆 Flex 結果
        line_bot_api.reply_message(
            event.reply_token,
            flex_article_list(category, items)
        )


# ---------------------------------------------------------
# 主程式
# ---------------------------------------------------------
if __name__ == "__main__":
    # 本機測試用（正式部署會用 WSGI）
    app.run(host="0.0.0.0", port=5000, debug=True)
