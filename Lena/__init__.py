import asyncio
import Config
import time
import logging
from openai import OpenAI
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message

MOD_LOAD = []
MOD_NOLOAD = []
SUDOERS = filters.user()
StartTime = time.time()

FORMAT = "[LenaAi] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
LOGGER = logging.getLogger('[LenaAi]')
LOGGER.info("LenaAi Starting | Licensed Under BSD 3-Clause License")
LOGGER.info("Project Maintained By: https://github.com/its-soumo")

LenaAi = OpenAI(api_key="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")
Mongo = MongoClient(Config.DB_URL)
db = Mongo.Lena

async def getSudoers():
    global SUDOERS
    LOGGER.info("Loading Sudoers...")
    sudodb = db.sudo
    sudoers = await sudodb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in Config.SUDO_USERS:
        SUDOERS.add(user_id)
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudodb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)

loop = asyncio.get_event_loop()
loop.run_until_complete(getSudoers())

app = Client(
    "Lena",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

LOGGER.info("Starting Client...")
app.start()

Pyro = app.get_me()
BOT_ID = Pyro.id
BOT_NAME = Pyro.first_name + (Pyro.last_name or "")
BOT_USERNAME = Pyro.username
BOT_MENTION = Pyro.mention
BOT_DC_ID = Pyro.dc_id
