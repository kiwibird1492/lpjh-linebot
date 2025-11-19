# crawler.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lpjh.ylc.edu.tw"

# 🔥 強化版 headers（偽裝成 Chrome，避免 Render 被擋）
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

# 🔥 崙背國中分類對應
CATEGORY_URLS = {
    "校務布告欄": f"{BASE_URL}/latest-news",
    "內部公告": f"{BASE_URL}/internal-news",
    "獎學金公告": f"{BASE_URL}/scholarship",
    "公文轉知": f"{BASE_URL}/announcements",
    "招生專區": f"{BASE_URL}/admissions",
    "教務處公告": f"{BASE_URL}/academics",
    "學務處公告": f"{BASE_URL}/students-affairs",
    "課後社團": f"{BASE_URL}/students-affairs",
}

# 🔥 快速連結（你可以自由新增）
QUICK_LINKS = {
    "學務系統": "https://www.ylc.edu.tw/staff-system",
    "學校行事曆": f"{BASE_URL}/calendar",
    "課表查詢": f"{BASE_URL}/academics",
    "校園食材登入": "https://fatrace.tw",
    "全國在職進修網": "https://www1.inservice.edu.tw",
    "師生 e-mail": "https://mail.google.com",
}


# ----------------------------------------------------------
# URL 輔助
# ----------------------------------------------------------
def full_url(href):
    if not href:
        return None
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return f"{BASE_URL}/{href}"


# ----------------------------------------------------------
# 抓取公告：日期 + 標題 + 連結
# ----------------------------------------------------------
def fetch_page_items(url):
    try:
        r = requests.get(url, timeout=5, headers=HEADERS)
    except:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    li_list = soup.select("ul.list li")   # 🔥 正確 selector

    items = []
    for li in li_list:
        a = li.find("a")
        if not a:
            continue

        title = a.get_text(strip=True)
        href = a.get("href")

        # 日期
        date_tag = li.find("span", class_="news-date")
        date = date_tag.get_text(strip=True) if date_tag else ""

        items.append({
            "title": f"{date} {title}",
            "url": full_url(href)
        })

    return items


# ----------------------------------------------------------
# 單分類搜尋
# ----------------------------------------------------------
def search_school(category: str, keyword: str = ""):
    url = CATEGORY_URLS.get(category)
    if not url:
        return []

    items = fetch_page_items(url)

    # 關鍵字過濾
    if keyword:
        items = [i for i in items if keyword in i["title"]]

    return items[:10]


# ----------------------------------------------------------
# 全分類搜尋（全校公告一次搜）
# ----------------------------------------------------------
def global_search(keyword):
    results = []

    for cat, url in CATEGORY_URLS.items():
        items = fetch_page_items(url)
        for i in items:
            if keyword in i["title"]:
                results.append(i)

    # 去除重複 + 限制前 10 筆
    unique = []
    seen = set()

    for item in results:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique.append(item)

    return unique[:10]
