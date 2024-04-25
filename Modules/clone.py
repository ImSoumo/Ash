from Ash import app
from pyrogram import filters, Client
from pyrogram.types import Message
from Anony import API_ID, API_HASH


@App.on_message(filters.command("clone"))
async def clone(bot, msg: Message):
    chat = msg.chat
    text = await msg.reply_photo(photo="https://graph.org/file/1f6b3738b92815eaf7f66.jpg", caption="**ᴜsᴀɢᴇ :** `/clone` **ʙᴏᴛ ᴛᴏᴋᴇɴ**")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("Booting Your Client")                   
        client = Client(":memory:", API_ID, API_HASH, bot_token=phone, plugins=dict{root="Modules"})
        await client.start()
        user = await client.get_me()
        await msg.reply(f"Your Client Has Been Successfully Started As @{user.username}!\n\nThanks for Cloning.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
