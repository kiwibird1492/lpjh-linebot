from linebot.models import FlexSendMessage

def flex_main_menu():
    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "快速選單", "weight": "bold", "size": "xl"},
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        _menu_button("校務布告欄"),
                        _menu_button("內部公告"),
                        _menu_button("獎學金公告"),
                        _menu_button("公文轉知"),
                        _menu_button("招生專區"),
                        _menu_button("教務處公告"),
                        _menu_button("學務處公告"),
                    ]
                }
            ]
        }
    }
    return FlexSendMessage(alt_text="主選單", contents=bubble)


def _menu_button(name):
    return {
        "type": "button",
        "style": "primary",
        "margin": "sm",
        "action": {
            "type": "postback",
            "label": name,
            "data": f"category={name}"
        }
    }


# 🔥 文章列表（你現在缺的就是這個）
def flex_article_list(category, items):

    article_boxes = []

    for item in items:
        title = item["title"]
        url = item["url"]

        article_boxes.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "spacing": "sm",
            "contents": [
                {"type": "text", "text": title, "wrap": True},
                {"type": "button",
                 "style": "link",
                 "height": "sm",
                 "action": {
                     "type": "uri",
                     "label": "🔗 前往查看",
                     "uri": url if url else "https://lpjh.ylc.edu.tw"
                 }}
            ]
        })

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"{category} 查詢結果", "weight": "bold", "size": "xl"},
                {"type": "separator", "margin": "md"},
            ] + article_boxes
        }
    }

    return FlexSendMessage(alt_text=f"{category} 查詢結果", contents=bubble)
