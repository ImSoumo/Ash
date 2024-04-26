"""



import asyncio
from Ash import app
from pyrogram import filters
from pyrogram.types import Message, User, Chat
from pyrogram.enums import ChatType

@app.on_message(filters.command("id"))
async def users_id(app, message: Message) -> None:
    users_info = "┈───────┈🎐┈───────┈\n\n"

    # Message ID and sender's ID
    users_info += f"» ᴍᴇssᴀɢᴇ ɪᴅ : `{message.message_id}`\n"
    users_info += f"» ᴜsᴇʀ {message.from_user.mention} ɪᴅ : `{message.from_user.id}`\n\n"

    # Handling reply-to message details
    if message.reply_to_message:
        reply_message = message.reply_to_message

        if reply_message.from_user:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ : `{reply_message.message_id}`\n"
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ {reply_message.from_user.mention}'s ɪᴅ : `{reply_message.from_user.id}`\n"

        if reply_message.photo:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴘʜᴏᴛᴏ ғɪʟᴇ ɪᴅ : `{reply_message.photo.file_id}`\n"

        if reply_message.sticker:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ sᴛɪᴄᴋᴇʀ ғɪʟᴇ ɪᴅ : `{reply_message.sticker.file_id}`\n"

        if reply_message.animation:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴀɴɪᴍᴀᴛɪᴏɴ ғɪʟᴇ ɪᴅ : `{reply_message.animation.file_id}`\n"

        if reply_message.document:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴅᴏᴄᴜᴍᴇɴᴛ ғɪʟᴇ ɪᴅ : `{reply_message.document.file_id}`\n"

        if reply_message.forward_from_chat:
            users_info += f"» ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀᴛ ɪᴅ : `{reply_message.forward_from_chat.id}`\n"

        if reply_message.forward_from:
            users_info += f"» ғᴏʀᴡᴀʀᴅᴇᴅ ʙʏ ᴜsᴇʀ {reply_message.forward_from.mention}'s ɪᴅ : `{reply_message.forward_from.id}`\n"

    # Handling mentioned user IDs
    mentioned_user_ids = [int(user_id) for user_id in message.text.split()[1:] if user_id.isdigit()]
    for user_id in mentioned_user_ids:
        try:
            user = await app.get_users(user_id)
            users_info += f"» {user.mention}'s ɪᴅ : `{user_id}`\n"
        except Exception:
            pass

    # Sending the composed user info message
    if users_info:
        await message.reply(users_info)
    else:
        await message.reply("ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴜsᴇʀ ɪᴅs !")

"""






import asyncio
from Ash import app
from pyrogram import filters
from pyrogram.types import Message, User, Chat
from pyrogram.enums import ChatType

@app.on_message(filters.command("id"))
async def users_id(app, message: Message) -> None:
    users_info = "┈───────┈🎐┈───────┈\n\n"

    # Message ID and sender's ID
    users_info += f"» ᴍᴇssᴀɢᴇ ɪᴅ : `{message.id}`\n"
    users_info += f"» ᴜsᴇʀ {message.from_user.mention} ɪᴅ : `{message.from_user.id}`\n\n"

    # Handling reply-to message details
    if message.reply_to_message:
        reply_message = message.reply_to_message

        if reply_message.from_user:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ : `{reply_message.id}`\n"
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ {reply_message.from_user.mention}'s ɪᴅ : `{reply_message.from_user.id}`\n"

        if reply_message.photo:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴘʜᴏᴛᴏ ғɪʟᴇ ɪᴅ : `{reply_message.photo.file_id}`\n"

        if reply_message.sticker:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ sᴛɪᴄᴋᴇʀ ғɪʟᴇ ɪᴅ : `{reply_message.sticker.file_id}`\n"

        if reply_message.animation:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴀɴɪᴍᴀᴛɪᴏɴ ғɪʟᴇ ɪᴅ : `{reply_message.animation.file_id}`\n"

        if reply_message.document:
            users_info += f"» ʀᴇᴘʟɪᴇᴅ ᴅᴏᴄᴜᴍᴇɴᴛ ғɪʟᴇ ɪᴅ : `{reply_message.document.file_id}`\n"

        if reply_message.forward_from_chat:
            users_info += f"» ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀᴛ ɪᴅ : `{reply_message.forward_from_chat.id}`\n"

        if reply_message.forward_from:
            users_info += f"» ғᴏʀᴡᴀʀᴅᴇᴅ ʙʏ ᴜsᴇʀ {reply_message.forward_from.mention}'s ɪᴅ : `{reply_message.forward_from.id}`\n"

    # Handling mentioned user IDs and channel IDs
    mentioned_ids = [id_str.strip() for id_str in message.text.split()[1:]]
    for id_str in mentioned_ids:
        try:
            user_or_chat_id = int(id_str)
            if user_or_chat_id > 0:
                # Positive ID is a user ID
                user = await app.get_users(user_or_chat_id)
                users_info += f"» {user.mention}'s ɪᴅ : `{user_or_chat_id}`\n"
            elif user_or_chat_id < 0:
                # Negative ID is a channel ID
                chat = await app.get_chat(user_or_chat_id)
                users_info += f"» Channel: `{chat.title}` (ID: `{user_or_chat_id}`)\n"
        except Exception:
            pass

    if users_info:
        await message.reply(users_info)
    else:
        await message.reply("ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴜsᴇʀ ɪᴅs !")










