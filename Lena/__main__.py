import Config
import asyncio
import datetime
import importlib
from pyrogram import idle
from Lena import app, LOGGER
from Lena.Database import cleanStage
from Lena.Modules import ALL_MODULES

loop = asyncio.get_event_loop()

async def lenaStart():
    for all_module in ALL_MODULES:
        importlib.import_module("Lena.Modules." + all_module)
    LOGGER.info("Deployed Successfully !")
    reData = await cleanStage()

    try:
        LOGGER.info("Getting Online Status...")
        if reData:
            await app.edit_message_text(
                reData["chat_id"],
                reData["message_id"],
                "**Bot ReStarted Successfully !**",
            )
        else:
            await app.send_message(Config.LOG_GROUP, "**// LenaAi Started //**")
    except Exception:
        pass
    
    await idle()
    await app.send_message(Config.LOG_GROUP, "**// LenaAi Is Now Dead //**")
    LOGGER.info("Goodbye LenaAi Is Now Dead !")

if __name__ == "__main__":
    loop.run_until_complete(lenaStart())
