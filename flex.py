# flex.py
from linebot.models import (
    FlexSendMessage, BubbleContainer, BoxComponent,
    TextComponent, ButtonComponent, SeparatorComponent,
    PostbackAction, URIAction
)

# 你定義過的分類（照 utils.py 順序一致）
MENU_ITEMS = [
    ("📘", "校務布告欄"),
    ("📄", "公文轉知"),
    ("🗓", "行事曆"),
    ("🍱", "午餐菜單"),
    ("🚌", "校車資訊"),
    ("🎯", "課後社團"),
    ("📚", "學務處公告"),
    ("📖", "教務處公告"),
    ("🗂", "課表查詢"),
]


def flex_main_menu():
    """
    產生「主選單」Flex Message
    9 個按鈕（Emoji + 類別名稱）
    """
    buttons = []

    for icon, title in MENU_ITEMS:
        buttons.append(
            ButtonComponent(
                action=PostbackAction(
                    label=f"{icon} {title}",
                    data=f"category={title}"
                ),
                style="secondary",
                height="sm",
                color="#f0f0f0"
            )
        )

    body = BoxComponent(
        layout="vertical",
        contents=[
            TextComponent(
                text="📌 崙背國中資訊查詢選單",
                weight="bold",
                size="lg",
                wrap=True,
                color="#333333"
            ),
            SeparatorComponent(margin="md"),
            BoxComponent(
                layout="vertical",
                margin="md",
                spacing="sm",
                contents=buttons
            )
        ]
    )

    bubble = BubbleContainer(
        direction="ltr",
        body=body
    )

    return FlexSendMessage(alt_text="崙背國中主選單", contents=bubble)



def flex_article_list(title_text, items):
    """
    將搜尋結果（文章列表）轉成 Flex 卡片
    items 格式：
    [{"title": "...", "url": "..."}]
    """
    contents = []

    # 每則文章一個方塊
    for item in items:
        block = BoxComponent(
            layout="vertical",
            margin="sm",
            spacing="sm",
            contents=[
                TextComponent(
                    text=f"• {item['title']}",
                    weight="bold",
                    wrap=True,
                    size="sm"
                ),
                ButtonComponent(
                    action=URIAction(
                        label="查看內容",
                        uri=item["url"] if item["url"] else "https://lpjh.ylc.edu.tw"
                    ),
                    height="sm",
                    style="primary",
                    color="#4a90e2"
                ),
                SeparatorComponent()
            ]
        )
        contents.append(block)

    # 如果沒有任何文章
    if not contents:
        contents.append(
            TextComponent(
                text="目前無相關資料。",
                size="md",
                weight="bold",
                wrap=True
            )
        )

    body = BoxComponent(
        layout="vertical",
        contents=[
            TextComponent(
                text=f"📘 {title_text}",
                weight="bold",
                size="lg",
                color="#333333",
                wrap=True
            ),
            SeparatorComponent(margin="md"),
            BoxComponent(
                layout="vertical",
                margin="md",
                spacing="md",
                contents=contents
            )
        ]
    )

    bubble = BubbleContainer(
        direction="ltr",
        body=body
    )

    return FlexSendMessage(
        alt_text=f"{title_text} 查詢結果",
        contents=bubble
    )
