import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DB_PATH = os.environ.get("DB_PATH", "stillalive.db")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0")) or None
