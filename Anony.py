from os import getenv

API_ID = int(getenv("API_ID", "26850449"))
LOGGER_GROUP = int(getenv("LOGGER_GROUP", "-1002130134327"))
API_HASH = str(getenv("API_HASH", "72a730c380e68095a8549ad7341b0608"))
SUDOERS = list(getenv("SUDOERS", "5896960462 1916369262 6517565595").split())
BOT_TOKEN = str(getenv("TELEGRAM_BOT_TOKEN", "6471845659:AAGEUoyD5zhUS2rdSc7DKRMb02p3_89Sbrs"))
MONGO_URI = str(getenv("MONGO_URI", "mongodb+srv://nandhaxd:rw5T7YJRjsE3fmk3@cluster0.80igexg.mongodb.net/?retryWrites=true&w=majority"))

MAX_CONCURRENT_TRANSMISSIONS = 1
PREFIXS = []
