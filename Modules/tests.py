import time
import re
import asyncio
from pyrogram.types import *
from typing import Union
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from Ash.AFK_db import add_afk, cleanmode_off, cleanmode_on, is_afk, remove_afk, is_cleanmode_on
from Ash import app
from Ash.Helper import get_readable_time2
from Ash.Core import put_cleanmode

X = ["!", ".", "/", "?", "$"]

@app.on_message(filters.command(["test"], X))
async def active_afk(app, ctx:Message) -> None:
    if ctx.sender_chat:
        return
    user_id = ctx.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            if afktype == "animation":
                send = (
                    await ctx.reply_animation(
                        data,
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n").format(
                            usr=ctx.from_user.mention, id=ctx.from_user.id, tm=seenago
                        ),
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_animation(
                        data,
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n**ʀᴇᴀsᴏɴ:** {reas}\n\n").format(
                            usr=ctx.from_user.mention,
                            id=ctx.from_user.id,
                            tm=seenago,
                            reas=reasonafk,
                        ),
                    )
                )
            elif afktype == "photo":
                send = (
                    await ctx.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n").format(
                            usr=ctx.from_user.mention, id=ctx.from_user.id, tm=seenago
                        ),
                    )
                    if str(reasonafk) == "None"
                    else await ctx.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n**ʀᴇᴀsᴏɴ:** {reas}\n\n").format(
                            usr=ctx.from_user.first_name, tm=seenago, reas=reasonafk
                        ),
                    )
                )
            elif afktype == "text":
                send = await ctx.reply_text(
                    ("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n").format(
                        usr=ctx.from_user.mention, id=ctx.from_user.id, tm=seenago
                    ),
                    disable_web_page_preview=True
                )
            elif afktype == "text_reason":
                send = await ctx.reply_text(
                    ("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n**ʀᴇᴀsᴏɴ:** {reas}\n\n").format(
                        usr=ctx.from_user.mention,
                        id=ctx.from_user.id,
                        tm=seenago,
                        reas=reasonafk,
                    ),
                    disable_web_page_preview=True
                )
        except Exception:
            send = await ctx.reply_text(
                ("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ").format(
                    usr=ctx.from_user.first_name, id=ctx.from_user.id
                ),
                disable_web_page_preview=True
            )
        await put_cleanmode(ctx.chat.id, send.id)
        return
    if len(ctx.command) == 1 and not ctx.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and not ctx.reply_to_message:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.animation:
        _data = ctx.reply_to_message.animation.file_id
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(ctx.command) > 1 and ctx.reply_to_message.photo:
        await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
        _reason = ctx.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(ctx.command) == 1 and ctx.reply_to_message.sticker:
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif len(ctx.command) > 1 and ctx.reply_to_message.sticker:
        _reason = (ctx.text.split(None, 1)[1].strip())[:100]
        if ctx.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await app.download_media(ctx.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
    send = await ctx.reply_text(
        ("{usr} [`{id}`] ɪꜱ ɴᴏᴡ ᴀꜰᴋ !").format(usr=ctx.from_user.mention, id=ctx.from_user.id)
    )
    await put_cleanmode(ctx.chat.id, send.id)


ADMIN = []

async def group_admins(chat_id):
    async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        ADMIN.append(member.user.id)
    return ADMIN

def segs_markup(status: Union[bool, str]):
    buttons = [
        [
            InlineKeyboardButton(text="🥤 Cʟᴇᴀɴ Mᴏᴅᴇ", callback_data="cleanmode_answer"),
            InlineKeyboardButton(
                text="✅ Eɴᴀʙʟᴇᴅ" if status == True else "❌ Dɪsᴀʙʟᴇᴅ",
                callback_data="cleanmode",
            ),
        ],
        [
            InlineKeyboardButton(text="🗑 Cʟᴏsᴇ Aғᴋ Mᴇɴᴜ", callback_data="close"),
        ],
    ]
    return buttons

@app.on_message(filters.command("afkmode", X))
async def afk_state(app:app, ctx:Message) -> None:
    if ctx.from_user.id not in await group_admins(ctx.chat.id):
        return await ctx.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ.")
    mode = await is_cleanmode_on(ctx.chat.id)
    segs = segs_markup()
    return await ctx.reply(
        (
            f"**⚙️ Aғᴋ Mᴏᴅᴇ Sᴇᴛᴛɪɴɢs :**\n\n"
            f"**🖇 Gʀᴏᴜᴘ :** {ctx.chat.title}\n"
            f"**🔖 Gʀᴏᴜᴘ ɪᴅ :** `{ctx.chat.id}`\n\n"
            f"**💡Cʜᴏᴏsᴇ ᴛʜᴇ ғᴜɴᴄᴛɪᴏɴ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴇᴅɪᴛ ᴏʀ ᴄʜᴀɴɢᴇ.**"
        ),
        reply_markup=InlineKeyboardMarkup(segs)
    )

@app.on_callback_query(filters.regex("close"))
async def on_close_button(client, CallbackQuery):
    await CallbackQuery.answer()
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex("cleanmode_answer"))
async def on_cleanmode_button(client, CallbackQuery):
    await CallbackQuery.answer("⁉️ Wʜᴀᴛ ɪs Tʜɪs ?\n\nWʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ Bᴏᴛ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ɪᴛs ᴍᴇssᴀɢᴇ ᴀғᴛᴇʀ 5 Mɪɴs ᴛᴏ ᴍᴀᴋᴇ ʏᴏᴜʀ ᴄʜᴀᴛ ᴄʟᴇᴀɴ ᴀɴᴅ ᴄʟᴇᴀʀ.", show_alert=True)

@app.on_callback_query(filters.regex("cleanmode"))
async def on_cleanmode_change(client, CallbackQuery):
    admin = await app.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    if admin.status in ["ChatMemberStatus.OWNER", "ChatMemberStatus.ADMINISTRATOR"]:
        pass
    else:
        return await CallbackQuery.answer("Only Admins can perform this action.", show_alert=True)
    await CallbackQuery.answer()
    status = None
    if await is_cleanmode_on(CallbackQuery.message.chat.id):
        await cleanmode_off(CallbackQuery.message.chat.id)
    else:
        await cleanmode_on(CallbackQuery.message.chat.id)
        status = True
    buttons = segs_markup(status)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return


@app.on_message(filters.command(["afkdel"], X) & filters.group)
async def afk_state(Guardian, ctx: Message):
    if not ctx.from_user:
        return
    if len(ctx.command) == 1:
        return await ctx.reply_text(
            ("**ᴜꜱᴀɢᴇ :** /afkdel [ᴇɴᴀʙʟᴇ|ᴅɪꜱᴀʙʟᴇ] ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪꜱᴀʙʟᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ.")
        )
    chat_id = ctx.chat.id
    state = ctx.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await cleanmode_on(chat_id)
        await ctx.reply("ᴇɴᴀʙʟᴇᴅ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴋ ᴍᴇꜱꜱᴀɢᴇ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.")
    elif state == "disable":
        await cleanmode_off(chat_id)
        await ctx.reply("ᴅɪꜱᴀʙʟᴇᴅ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴋ ᴍᴇꜱꜱᴀɢᴇ.")
    else:
        await ctx.reply("**ᴜꜱᴀɢᴇ :** /afkdel [ᴇɴᴀʙʟᴇ|ᴅɪꜱᴀʙʟᴇ] ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪꜱᴀʙʟᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ.")


@app.on_message(
    filters.all & filters.group & ~filters.bot & ~filters.via_bot
)
async def afk_watcher_func(self:Client, ctx:Message) -> None:
    if ctx.sender_chat:
        return
    userid = ctx.from_user.id
    user_name = ctx.from_user.mention
    msg = ""
    replied_user_id = 0
    verifier, reasondb = await is_afk(ctx.from_user.id)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time2((int(time.time() - timeafk)))
            if afktype == "text":
                msg += ("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n").format(
                    usr=user_name, id=userid, tm=seenago
                )
            if afktype == "text_reason":
                msg += ("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n**ʀᴇᴀsᴏɴ:** {reas}\n\n").format(
                    usr=user_name, id=userid, tm=seenago, reas=reasonafk
                )
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await ctx.reply_animation(
                        data,
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n").format(
                            usr=user_name, id=userid, tm=seenago
                        ),
                    )
                else:
                    send = await ctx.reply_animation(
                        data,
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n**ʀᴇᴀsᴏɴ:** {reas}\n\n").format(
                            usr=user_name, id=userid, tm=seenago, reas=reasonafk
                        ),
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await ctx.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n").format(
                            usr=user_name, id=userid, tm=seenago
                        ),
                    )
                else:
                    send = await ctx.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀꜱ ᴀᴡᴀʏ ꜰᴏʀ {tm}\n\n**ʀᴇᴀsᴏɴ:** {reas}\n\n").format(
                            usr=user_name, id=userid, tm=seenago, reas=reasonafk
                        ),
                    )
        except:
            msg += ("**{usr}** [`{id}`] ɪꜱ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ").format(usr=user_name, id=userid)

    if ctx.reply_to_message:
        try:
            replied_first_name = ctx.reply_to_message.from_user.mention
            replied_user_id = ctx.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time2((int(time.time() - timeafk)))
                    if afktype == "text":
                        msg += ("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                            usr=replied_first_name, id=replied_user_id, tm=seenago
                        )
                    if afktype == "text_reason":
                        msg += ("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                            usr=replied_first_name,
                            id=replied_user_id,
                            tm=seenago,
                            reas=reasonafk,
                        )
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            send = await ctx.reply_animation(
                                data,
                                caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                ),
                            )
                        else:
                            send = await ctx.reply_animation(
                                data,
                                caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                    reas=reasonafk,
                                ),
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            send = await ctx.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                ),
                            )
                        else:
                            send = await ctx.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                    usr=replied_first_name,
                                    id=replied_user_id,
                                    tm=seenago,
                                    reas=reasonafk,
                                ),
                            )
                except Exception:
                    msg += ("{usr} [`{id}`] ɪꜱ ᴀꜰᴋ !").format(
                        usr=replied_first_name, id=replied_user_id
                    )
        except:
            pass

    # If username or mentioned user is AFK
    if ctx.entities:
        entity = ctx.entities
        j = 0
        for _ in range(len(entity)):
            if (entity[j].type) == enums.MessageEntityType.MENTION:
                found = re.findall("@([_0-9a-zA-Z]+)", ctx.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time2((int(time.time() - timeafk)))
                        if afktype == "text":
                            msg += ("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                usr=user.first_name[:25], id=user.id, tm=seenago
                            )
                        if afktype == "text_reason":
                            msg += ("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                usr=user.first_name[:25],
                                id=user.id,
                                tm=seenago,
                                reas=reasonafk,
                            )
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_animation(
                                    data,
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                        usr=user.first_name[:25], id=user.id, tm=seenago
                                    ),
                                )
                            else:
                                send = await ctx.reply_animation(
                                    data,
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                        usr=user.first_name[:25],
                                        id=user.id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                        usr=user.first_name[:25], id=user.id, tm=seenago
                                    ),
                                )
                            else:
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                        usr=user.first_name[:25],
                                        id=user.id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                    except:
                        msg += ("{usr} [`{id}`] ɪꜱ ᴀꜰᴋ !").format(
                            usr=user.first_name[:25], id=user.id
                        )
            elif (entity[j].type) == enums.MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time2((int(time.time() - timeafk)))
                        if afktype == "text":
                            msg += ("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                usr=first_name[:25], id=user_id, tm=seenago
                            )
                        if afktype == "text_reason":
                            msg += ("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                usr=first_name[:25],
                                id=user_id,
                                tm=seenago,
                                reas=reasonafk,
                            )
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_animation(
                                    data,
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                        usr=first_name[:25], id=user_id, tm=seenago
                                    ),
                                )
                            else:
                                send = await ctx.reply_animation(
                                    data,
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                        usr=first_name[:25],
                                        id=user_id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n").format(
                                        usr=first_name[:25], id=user_id, tm=seenago
                                    ),
                                )
                            else:
                                send = await ctx.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=("**{usr}** [`{id}`] ɪꜱ ᴀꜰᴋ ꜱɪɴᴄᴇ {tm} ᴀɢᴏ.\n\n**ʀᴇᴀꜱᴏɴ :** {reas}\n\n").format(
                                        usr=first_name[:25],
                                        id=user_id,
                                        tm=seenago,
                                        reas=reasonafk,
                                    ),
                                )
                    except:
                        msg += ("{usr} [`{id}`] ɪꜱ ᴀꜰᴋ !").format(usr=first_name[:25], id=user_id)
            j += 1
    if msg != "":
        try:
            send = await ctx.reply_text(msg, disable_web_page_preview=True)
        except:
            pass
    try:
        await put_cleanmode(ctx.chat.id, send.id)
    except:
        pass










# of 210 no line
"""    
    if ctx.entities:
        possible = "test"
        message_text = ctx.text or ctx.caption
        for entity in ctx.entities:
            try:
                if (
                    entity.type == enums.MessageEntityType.BOT_COMMAND
                    and (message_text[0 : 0 + entity.length]).lower() in possible
                ):
                    return
            except UnicodeDecodeError:  # Some weird character make error
                return
"""
