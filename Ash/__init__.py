import Anony
import logging
from pyrogram import enums
from pyrogram.client import Client
from motor.motor_asyncio import AsyncIOMotorClient

cleanmode = {}

logging.basicConfig(
    level=logging.INFO,
    format="[Asʜ-Kᴇᴛᴄʜᴜᴍ] %(message)s",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()]
)
LOGGER = logging.getLogger("[Asʜ-Kᴇᴛᴄʜᴜᴍ]")
LOGGER.info("Asʜ-Kᴇᴛᴄʜᴜᴍ Sᴛᴀʀᴛɪɴɢ | Lɪᴄᴇɴsᴇᴅ Uɴᴅᴇʀ MIT Lɪᴄᴇɴsᴇ.")
LOGGER.info("Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ: Qᴜᴀʀᴛɴʏ")

app = Client(
    name="Asʜ-Kᴇᴛᴄʜᴜᴍ",
    api_id=Anony.API_ID,
    api_hash=Anony.API_HASH,
    bot_token=Anony.BOT_TOKEN,
    plugins=dict(root="Modules"),
    parse_mode=enums.ParseMode.MARKDOWN,
    mongodb=dict(connection=AsyncIOMotorClient(Anony.MONGO_URI)),
    max_concurrent_transmissions=Anony.MAX_CONCURRENT_TRANSMISSIONS
)
