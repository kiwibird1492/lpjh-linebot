# app.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage,
    PostbackEvent
)

from utils import detect_category
from flex import flex_main_menu, flex_article_list

# Firestore
import firebase_admin
from firebase_admin import credentials, firestore

import os

app = Flask(__name__)

# ---------------------------------------------------------
# 👉 Channel Secret / Access Token
# ---------------------------------------------------------
CHANNEL_ACCESS_TOKEN = "Km98R7jo9qa8ne8eBniDIRIEwQ2De0CAj7E8EKQam8ib2NwiYv/mdQ8VY2nA3dO96aFA0a1w8Wr3ZNcPFQyVG8cSaTKygfaJoOHWhSwVf1km13rqruY9oADAl1YNxJ6JMmQ1/IZDtVXnP68XYL7vuwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "46462ff62aa2638260553fa5a8a86eaf"
# ---------------------------------------------------------

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


# ---------------------------------------------------------
# 👉 Firestore 初始化
# ---------------------------------------------------------
CRED_PATH = "/etc/secrets/firebase-key.json"

if not firebase_admin._apps:
    if not os.path.exists(CRED_PATH):
        print("❌ Firebase 金鑰不存在：", CRED_PATH)
    else:
        print("✅ Firebase 金鑰已找到：", CRED_PATH)

    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ---------------------------------------------------------
# ⭐ Firestore 讀資料
# ---------------------------------------------------------
def read_from_firestore(category):
    doc_ref = db.collection("lpjh").document(category).get()
    if not doc_ref.exists:
        return []

    data = doc_ref.to_dict()
    return data.get("items", [])


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
# 1️⃣ 文字訊息：分類 + Firestore
# ---------------------------------------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_text = event.message.text.strip()

    # 顯示選單
    if user_text in ["選單", "menu", "Menu", "主選單"]:
        line_bot_api.reply_message(
            event.reply_token,
            flex_main_menu()
        )
        return

    # 自動判斷分類
    category = detect_category(user_text)

    # Firestore 查資料
    items = read_from_firestore(category)

    # 若使用者輸入關鍵字 → 過濾
    if user_text not in ["選單", category]:
        items = [i for i in items if user_text in i["title"]]

    # 回傳 Flex
    line_bot_api.reply_message(
        event.reply_token,
        flex_article_list(category, items)
    )


# ---------------------------------------------------------
# 2️⃣ Postback 按鈕
# ---------------------------------------------------------
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data

    if data.startswith("category="):
        category = data.replace("category=", "")
        items = read_from_firestore(category)

        line_bot_api.reply_message(
            event.reply_token,
            flex_article_list(category, items)
        )


# ---------------------------------------------------------
# 主程式（本機測試）
# ---------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
