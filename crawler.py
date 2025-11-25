from google.cloud import firestore
from google.oauth2 import service_account
import requests
from bs4 import BeautifulSoup

# ----------------------------------------
# Firestore 本機金鑰（你的 Windows 路徑）
# ----------------------------------------
CRED_PATH = "lpjh-bot-firebase-adminsdk-fbsvc-18c4745b55.json"

creds = service_account.Credentials.from_service_account_file(CRED_PATH)
db = firestore.Client(credentials=creds, project=creds.project_id)


# ---------------------------------------------------------
# ⭐ 更新 Firestore（爬蟲結果寫入）
# ---------------------------------------------------------
def update_firestore(category, items):
    doc_ref = db.collection("lpjh").document(category)
    doc_ref.set({"items": items})
    print(f"已更新 Firestore：{category}, 共 {len(items)} 筆資料")
