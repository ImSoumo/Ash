import asyncio
from Ash import app
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType

@app.on_message(filters.command("id"))
async def users_id(app, message: Message) -> None:
    users = "**┈───────┈🎐┈───────┈**\n\n"
    users += f"» ᴍᴇssᴀɢᴇ ɪᴅ : `{message.id}`\n"
    users += f"» ᴜsᴇʀ {message.from_user.mention} ɪᴅ : `{message.from_user.id}`\n"
    if message.reply_to_message and message.reply_to_message.from_user:
        users += f"» ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ : `{message.reply_to_message.id}`\n"
        users += f"» ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ {message.reply_to_message.from_user.mention}'s ɪᴅ : `{message.reply_to_message.from_user.id}`\n\n"
    elif message.reply_to_message and message.reply_to_message.photo:
        users += f"» ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ : `{message.reply_to_message.id}`\n"
        users += f"» ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ {message.reply_to_message.from_user.mention}'s ɪᴅ : `{message.reply_to_message.from_user.id}`\n"
        users += f"» ʀᴇᴘʟɪᴇᴅ ᴘʜᴏᴛᴏ ғɪʟᴇ ɪᴅ : `{message.reply_to_message.photo.file_id}`\n\n"
    gusers = message.text.split()[1:]
    for guser in gusers:
        try:
            user = await app.get_users(guser)
            users += f"» {user.mention}'s ɪᴅ : `{user.id}`\n"
        except Exception:
            users += ""
    if users:
        await message.reply(users)
    else:
        await message.reply("ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴜsᴇʀ ɪᴅs !")
