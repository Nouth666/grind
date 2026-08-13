import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

ADMIN_IDS = {
    int(admin_id.strip())
    for admin_id in os.getenv("ADMIN_IDS", "").split(",")
    if admin_id.strip().isdigit()
}

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан. Скопируй .env.example в .env и заполни его.")

if not ADMIN_IDS:
    raise RuntimeError("ADMIN_IDS не задан. Укажи свой Telegram ID в .env.")
