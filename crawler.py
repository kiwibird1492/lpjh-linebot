import requests

BASE_URL = "https://lpjh.ylc.edu.tw"
HEADERS = {"User-Agent": "Mozilla/5.0"}

CATEGORY_API = {
    "校務布告欄": "latest-news",
    "內部公告": "internal-news",
    "獎學金公告": "scholarship",
    "公文轉知": "announcements",
    "招生專區": "admissions",
    "教務處公告": "academics",
    "學務處公告": "students-affairs",
    "課後社團": "students-affairs",
}


def full_url(href):
    if href.startswith("http"):
        return href
    return BASE_URL + href


def fetch_page_items(category_key, page=1):
    """
    使用 API 抓公告（不再抓 HTML）
    """
    api_path = CATEGORY_API.get(category_key)
    if not api_path:
        return []

    url = f"{BASE_URL}/{api_path}?ajax=1&page={page}"

    try:
        r = requests.get(url, timeout=8, headers=HEADERS)
        data = r.json()
    except:
        return []

    items = []

    for row in data.get("data", []):
        items.append({
            "title": f"{row.get('date', '')} {row.get('title', '')}",
            "url": full_url(row.get("url", ""))
        })

    return items


def search_school(category, keyword=""):
    # 直接抓 API 第一頁資料
    items = fetch_page_items(category, page=1)

    # 關鍵字過濾
    if keyword:
        items = [i for i in items if keyword in i["title"]]

    return items[:10]
