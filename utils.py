# utils.py

def detect_category(text):
    """依關鍵字自動判斷分類"""

    text = text.lower()

    # 🔥 快速連結關鍵字
    quick_keys = ["課表", "行事曆", "教育處", "在職", "食材", "e-mail", "email", "差勤", "學務系統"]
    for key in quick_keys:
        if key in text:
            return "快速連結"

    # 🔥 公告類
    if "校務" in text:
        return "校務布告欄"
    if "內部" in text:
        return "內部公告"
    if "獎學" in text or "獎金" in text:
        return "獎學金公告"
    if "公文" in text:
        return "公文轉知"
    if "招生" in text:
        return "招生專區"

    # 🔥 處室
    if "教務" in text:
        return "教務處公告"
    if "學務" in text:
        return "學務處公告"

    # 🔥 其他功能
    if "社團" in text:
        return "課後社團"
    if "校車" in text:
        return "校車資訊"
    if "午餐" in text:
        return "午餐菜單"
    if "課表" in text:
        return "課表查詢"

    return "校務布告欄"
