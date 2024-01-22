from Lena import app
from pyrogram import filters, Client
from pyrogram.types import Message
from Config import API_ID, API_HASH

plugins = dict(
    root="Lena",
    include=[
        "Modules.telegraphFunc",
        "upscaleAi"
    ]
)

@app.on_message(filters.command("clone"))
async def cloneFunc(client: Client, message: Message):
    chat = message.chat
    text = await message.reply("**Usᴀɢᴇ :** `/clone` **ʙᴏᴛ ᴛᴏᴋᴇɴ**")
    bot_token = message.text.split(None, 1)[1].strip()
    try:
        await text.edit("**Booting Your Client...**")                   
        pbot = Client(
          ":Lena:",
          api_id=API_ID,
          api_hash=API_HASH,
          bot_token=bot_token,
          plugins=plugins
        )
        await pbot.start()
        user = await pbot.get_me()
        await message.reply(f"**Your Client Has Been Successfully Started As @{user.username}!**\n**Thanks For Cloning.**")
    except Exception as e:
        await message.reply(f"**Error :** `{str(e)}`\n**Press /start To Start Again !**")
