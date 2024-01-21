from Lena import app
from pyrogram import filters, Client
from pyrogram.types import Message
from Config import API_ID, API_HASH


@app.on_message(filters.command("clone"))
async def clone(app: Client, message: Message):
    chat = message.chat
    Text = await message.reply("**Usᴀɢᴇ :** `/clone` **ʙᴏᴛ ᴛᴏᴋᴇɴ**")
    Token = message.text.split(None, 1)[1].strip()
    try:
        await Text.edit("Booting Your Client...")                   
        pbot = Client(
          ":memory:",
          api_id=API_ID,
          api_hash=API_HASH,
          bot_token=Token,
          plugins={"root": "Lena.Modules"}
        )
        await pbot.start()
        user = await pbot.get_me()
        await message.reply(f"Your Client Has Been Successfully Started As @{user.username}!\nThanks For Cloning.")
    except Exception as e:
        await msg.reply(f"**Error :** `{str(e)}`\nPress /start To Start Again !")
