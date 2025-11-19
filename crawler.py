import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lpjh.ylc.edu.tw"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# 崙背國中分類對應
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

def full_url(href):
    if not href:
        return None
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return f"{BASE_URL}/{href}"

def fetch_page_items(url):
    """抓取公告：日期 + 標題 + 連結（正確版本）"""
    try:
        r = requests.get(url, timeout=5, headers=HEADERS)
    except:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    # 🔥 崙背國中使用 <tr> 來放公告
    rows = soup.select("table tbody tr")

    for row in rows:
        date_td = row.find("td", class_="news-date")
        a = row.find("a")

        if not a:
            continue

        date = date_td.get_text(strip=True) if date_td else ""
        title = a.get_text(strip=True)
        href = a["href"]

        items.append({
            "title": f"{date} {title}",
            "url": full_url(href)
        })

    return items

def search_school(category, keyword=""):
    url = CATEGORY_URLS.get(category)
    if not url:
        return []

    items = fetch_page_items(url)

    # 關鍵字搜尋
    if keyword:
        items = [i for i in items if keyword in i["title"]]

    # 無結果回預設項
    if not items:
        return [{
            "title": f"目前查無「{category}」相關資訊。",
            "url": None
        }]

    return items[:10]
