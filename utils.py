# utils.py
# 關鍵字分類系統（智慧搜尋入口）

CATEGORY_KEYWORDS = {
    "校務布告欄": ["校務", "布告", "通知", "公告", "最新消息", "消息"],
    "公文轉知": ["公文", "轉知", "函", "來文"],
    "行事曆": ["行事曆", "行事", "calendar", "活動表"],
    "午餐菜單": ["午餐", "菜單", "便當", "營養午餐", "健康午餐", "午餐表"],
    "校車資訊": ["校車", "接駁", "交通", "乘車", "司機"],
    "課後社團": ["社團", "課後", "社團活動", "團務"],
    "學務處公告": ["學務", "訓育", "生輔", "衛生", "生活教育"],
    "教務處公告": ["教務", "課務", "課表", "註冊", "教學"],
    "課表查詢": ["課表", "排課", "時間表", "課程查詢"]
}


# 預設分類（當使用者輸入與分類無關的字）
DEFAULT_CATEGORY = "校務布告欄"


def detect_category(user_text: str) -> str:
    """
    根據使用者輸入文字，判斷最接近的分類
    回傳分類名稱（字串）
    """
    for category, keywords in CATEGORY_KEYWORDS.items():
        for k in keywords:
            if k in user_text:
                return category

    # 若找不到任何分類 → 回預設值
    return DEFAULT_CATEGORY


def get_all_categories():
    """回傳所有分類的清單（會用在主選單）"""
    return list(CATEGORY_KEYWORDS.keys())
