# flex.py
from linebot.models import FlexSendMessage


def flex_main_menu():
    """主選單（6 大分類）"""

    bubbles = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "崙背國中查詢系統", "weight": "bold", "size": "xl"},
                {"type": "separator", "margin": "md"},
                btn("校務布告欄"),
                btn("公文轉知"),
                btn("教務處公告"),
                btn("學務處公告"),
                btn("課後社團"),
                btn("快速連結"),
            ]
        }
    }

    return FlexSendMessage("主選單", bubbles)


def btn(name):
    return {
        "type": "box",
        "layout": "vertical",
        "margin": "md",
        "contents": [{
            "type": "button",
            "style": "primary",
            "action": {
                "type": "postback",
                "label": name,
                "data": f"category={name}"
            }
        }]
    }


def flex_article_list(category, items):
    """回覆查詢結果（文章列表）"""

    contents = []

    for item in items:
        contents.append({
            "type": "box",
            "layout": "vertical",
            "borderWidth": "1px",
            "cornerRadius": "md",
            "paddingAll": "10px",
            "margin": "md",
            "contents": [
                {"type": "text", "text": item["title"], "wrap": True},
                {"type": "text", "text": item["url"] or "無連結", "size": "sm", "color": "#555555", "wrap": True}
            ]
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"{category} 查詢結果", "weight": "bold", "size": "lg"},
                {"type": "separator", "margin": "md"},
            ] + contents
        }
    }

    return FlexSendMessage("查詢結果", bubble)
