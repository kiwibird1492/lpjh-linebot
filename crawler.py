# crawler.py
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
    """ 抓取公告：日期 + 標題 + 連結 """
    try:
        r = requests.get(url, timeout=5, headers=HEADERS)
    except:
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    # 🔥 正確 selector：抓所有公告 li
    li_list = soup.select("ul.list li")

    for li in li_list:
        # 標題
        a = li.find("a")
        if not a:
            continue

        title = a.get_text(strip=True)
        href = a.get("href")

        # 日期（可有可無）
        date_tag = li.find("span", class_="news-date")
        date = date_tag.get_text(strip=True) if date_tag else ""

        items.append({
            "title": f"{date} {title}",
            "url": full_url(href)
        })

    return items


def search_school(category: str, keyword: str = ""):

    url = CATEGORY_URLS.get(category)
    if not url:
        return []

    items = fetch_page_items(url)

    # 關鍵字過濾
    if keyword:
        items = [i for i in items if keyword in i["title"]]

    return items[:10]
