# crawler.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lpjh.ylc.edu.tw"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ---------------------------------------------------------
# 🔥 崙背國中公告分類 URL
# ---------------------------------------------------------
CATEGORY_URLS = {
    "校務布告欄": f"{BASE_URL}/latest-news",
    "內部公告": f"{BASE_URL}/internal-news",
    "獎學金公告": f"{BASE_URL}/scholarship",
    "公文轉知": f"{BASE_URL}/announcements",
    "招生專區": f"{BASE_URL}/admissions",
    "教務處公告": f"{BASE_URL}/academics",
    "學務處公告": f"{BASE_URL}/students-affairs",
    "課後社團": f"{BASE_URL}/students-affairs",
    "課表查詢": f"{BASE_URL}/academics",
}

# ---------------------------------------------------------
# 🔥 快速連結（固定，不需要爬）
# ---------------------------------------------------------
QUICK_LINKS = {
    "學務系統": "https://www.yunlin.edu.tw/stuAffairs",
    "雲林縣教育處": "https://www.ylc.edu.tw",
    "全國在職進修網": "https://www1.inservice.edu.tw",
    "校園食材登入平台": "https://fatrace.tw",
    "學習扶助評量": "https://assist.moe.edu.tw",
    "師生e-mail": "https://mail.google.com",
    "第一學期課表": f"{BASE_URL}/academics",
    "第二學期行事曆": f"{BASE_URL}/calendar",
    "線上差勤系統": None,  # 需登入
}


def full_url(href):
    if not href:
        return None
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return f"{BASE_URL}/{href}"


# ---------------------------------------------------------
# 🔥 爬公告用
# ---------------------------------------------------------
def fetch_page_items(url):
    try:
        r = requests.get(url, timeout=5, headers=HEADERS)
    except:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    cards = soup.find_all(class_="card-title")
    for card in cards:
        title = card.get_text().strip()
        link_tag = card.find_parent().find("a")
        href = link_tag.get("href") if link_tag else None

        items.append({
            "title": title,
            "url": full_url(href)
        })

    return items


# ---------------------------------------------------------
# 🔥 主搜尋功能（公告 + 快速連結）
# ---------------------------------------------------------
def search_school(category: str, keyword: str = ""):
    # 🔥 若是快速連結 → 不爬，直接比對
    if category == "快速連結":
        results = []
        for name, url in QUICK_LINKS.items():
            if keyword.replace(" ", "") in name.replace(" ", ""):
                results.append({
                    "title": name,
                    "url": url or "需登入校內系統"
                })
        return results or [{"title": "查無相關快速連結", "url": None}]

    # 🔥 一般公告
    url = CATEGORY_URLS.get(category)
    if not url:
        return []

    items = fetch_page_items(url)

    if keyword:
        items = [i for i in items if keyword in i["title"]]

    return items[:10]
