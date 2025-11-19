# crawler.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lpjh.ylc.edu.tw"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# 崙背國中主要區塊 URL 對應
CATEGORY_URLS = {
    "校務布告欄": f"{BASE_URL}/latest-news",
    "公文轉知": f"{BASE_URL}/announcements",
    "教務處公告": f"{BASE_URL}/academics",
    "學務處公告": f"{BASE_URL}/students-affairs",
    "課後社團": f"{BASE_URL}/students-affairs",   # 多位於學務處
    "校車資訊": f"{BASE_URL}/students-affairs",     # 若抓不到 → 預設回答
    "行事曆": f"{BASE_URL}/calendar",               # 網站無固定頁 → 可能抓不到
    "午餐菜單": f"{BASE_URL}/lunch",               # 若無資料 → 預設回答
    "課表查詢": f"{BASE_URL}/academics",           # 多放在教務處位置
}


# 把相對路徑補成完整網址
def full_url(href):
    if not href:
        return None
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return f"{BASE_URL}/{href}"


# 主要爬蟲方法
def fetch_page_items(url):
    """ 抓取某一頁面的所有文章標題 + 連結 """
    try:
        r = requests.get(url, timeout=5, headers=HEADERS)
    except:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    items = []

    # 崙背國中是縣市政府共用架構 → 卡片 class="card-title"
    cards = soup.find_all(class_="card-title")
    for card in cards:
        title = card.get_text().strip()

        # 卡片父層通常會有 <a>
        link_tag = card.find_parent().find("a")
        href = link_tag.get("href") if link_tag else None

        items.append({
            "title": title,
            "url": full_url(href)
        })

    return items


def search_school(category: str, keyword: str = ""):
    """
    依類別抓取資料，並可選擇加關鍵字篩選。
    回傳格式：
    [
        {"title": "...", "url": "..."},
        ...
    ]
    """
    url = CATEGORY_URLS.get(category)
    if not url:
        return []

    items = fetch_page_items(url)

    # 若有輸入關鍵字 → 再過濾一次
    if keyword:
        results = [i for i in items if keyword in i["title"]]
    else:
        results = items

    # 特殊處理：午餐菜單 / 行事曆 / 校車資訊 可能網站沒有
    if category == "午餐菜單" and not results:
        return [{
            "title": "目前看不到午餐菜單，請稍後再試或洽學務處。",
            "url": None
        }]

    if category == "行事曆" and not results:
        return [{
            "title": "網站上目前沒有行事曆資料，請查看首頁或洽教務處。",
            "url": None
        }]

    if category == "校車資訊" and not results:
        return [{
            "title": "網站沒有校車資訊，通常公布於學務處或紙本公告。",
            "url": None
        }]

    if category == "課表查詢" and not results:
        return [{
            "title": "目前沒有課表查詢資料，通常由教務處公布。",
            "url": None
        }]

    return results[:10]  # 回前 10 筆即可
