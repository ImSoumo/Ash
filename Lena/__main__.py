import Config
import asyncio
import importlib
from pyrogram import idle
from Lena import app, LOGGER
from Lena.Modules import ALL_MODULES

loop = asyncio.get_event_loop()

async def lenaStart():
    for all_module in ALL_MODULES:
        importlib.import_module("Lena.Modules." + all_module)
    LOGGER.info("Deployed Successfully !")
    await idle()
    LOGGER.info("Goodbye LenaAi Is Now Dead !")

if __name__ == "__main__":
    loop.run_until_complete(lenaStart())
