import os
from dotenv import load_dotenv

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6533944592:AAHAT5e3tjRy-qJBArPNUwYc3xT9hIhk3Vg")
API_ID = int(os.environ.get("API_ID", "26850449"))
API_HASH = os.environ.get("API_HASH", "72a730c380e68095a8549ad7341b0608")
SUDO_USERS = list(map(int, os.environ.get("SUDO_USERS", "5896960462 1916369262 6517565595").split()))
LOG_GROUP = int(os.environ.get("LOG_GROUP", "-1001850524099"))
DB_URL = os.environ.get("DB_URL", "mongodb+srv://user:user123@cluster0.enc7mot.mongodb.net/?retryWrites=true&w=majority")
