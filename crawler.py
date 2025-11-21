import requests
from google.cloud import firestore
from bs4 import BeautifulSoup
import datetime
import time

# -------------------------------
# 🔥 Firebase 初始化
# -------------------------------
db = firestore.Client.from_service_account_json("lpjh-bot-firebase-adminsdk-fbsvc-18c4745b55.json")



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
            "url": full_url(row.get("url", "")),
        })

    return items[:10]


def update_firestore():
    print("開始更新公告資料...")

    for category in CATEGORY_API.keys():
        print(f"正在抓取：{category}")
        items = fetch_page_items(category)

        db.collection("lpjh").document(category).set({
            "updated": datetime.datetime.now(),
            "items": items
        })

        print(f"✔ 已更新：{category}")

    print("🔥 所有公告更新完成！")


# -------------------------------
# 🔥 每 5 分鐘自動更新一次
# -------------------------------
if __name__ == "__main__":
    while True:
        update_firestore()
        print("等待 5 分鐘後再次更新...\n")
        time.sleep(300)
