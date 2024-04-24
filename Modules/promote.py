import os
import time
from Ash import app
from pyrogram import filters, enums, Client 
from pyrogram.enums import MessageEntityType, ChatMemberStatus
from pyrogram.types import ChatPrivileges, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.errors import BadRequest

async def pyro_user(message:Message, text:str) -> None:
    def check(text:str):
        try:
            int(text)
        except ValueError:
            return False
        return True
    text = text.strip()
    if check(text):
        return int(text)
    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == MessageEntityType.MENTION:
        return (await app.get_users(text)).id
    if entity.type == MessageEntityType.TEXT_MENTION:
        return entity.user.id
    return None

async def users_or_reasons(message: Message, sender_chat=False) -> None:
    user = None
    reason = None
    args = message.text.strip().split()
    replied = message.reply_to_message
    if replied:
        if not replied.from_user:
            if replied.sender_chat and replied.sender_chat != message.chat.id and sender_chat:
                sender = replied.sender_chat.id
            else:
                return None, None
        else:
            sender = replied.from_user.id
        if len(args) < 2:
            reason = None
        else:
            reason = message.text.split(None, 1)[1]
        return sender, reason
    if len(args) == 2:
        user = message.text.split(None, 1)[1]
        return await pyro_user(message, user), None
    if len(args) > 2:
        user, reason = message.text.split(None, 2)[1:]
        return await pyro_user(message, user), reason
    return user, reason


COMMAND_USERS = [ChatMemberStatus.ADMINISTRATOR]
DEMOTE_USER = ChatPrivileges(
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_video_chats=False
)

@app.on_message(filters.command("promote", ["!", "/", "?"]))                 
async def _promote_users(app, message: Message) -> None:
    checks = await users_or_reasons(message) 
    bot = await app.get_chat_member(message.chat.id, app.me.id)
    if not checks[0]:
        return await message.reply("ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ... !")
    memes = await app.get_chat_member(message.chat.id, checks[0])
    if memes.privileges:
        return await message.reply("ʙʀᴜʜ ᴛʜɪɴᴋ ᴀʙᴏᴜᴛ ɪᴛ ʜᴏᴡ ᴄᴀɴ ɪ ᴘʀᴏᴍᴏᴛᴇ ᴀɴ ᴀᴅᴍɪɴ.")
    mention = (await app.get_users(checks[0])).mention
    KEYBOARDS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Fᴜʟʟ Pʀᴏᴍᴏᴛᴇ", callback_data=f"mpromote_{message.from_user.id}_{checks[0]}")
            ],
            [
                InlineKeyboardButton("Dᴇᴍᴏᴛᴇ", callback_data=f"demote_{message.from_user.id}_{checks[0]}"),
                InlineKeyboardButton("Cʟᴏsᴇ", callback_data=f"puserclose_{message.from_user.id}")
            ]
        ]
    )   
    PROMOTE_USER = ChatPrivileges(
        can_change_info=False,
        can_invite_users=bot.privileges.can_invite_users,
        can_delete_messages=bot.privileges.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.privileges.can_manage_chat,
        can_manage_video_chats=bot.privileges.can_manage_video_chats,
    )         
    PROMOTE_MESSAGE = f"**Sᴜᴄᴄᴇssғᴜʟʟʏ Pʀᴏᴍᴏᴛᴇᴅ {mention} Iɴ {message.chat.title} !**"
    try:
        await app.promote_chat_member(message.chat.id, checks[0], PROMOTE_USER)           
        if checks[1] != None:
            await app.set_administrator_title(message.chat.id, checks[0], checks[1])
        return await message.reply_photo(
            photo="AgACAgUAAx0CW40BMwABATcgZijiuJ1lmBg6jLtmOCIkhsnzPDoAAvG_MRsHoklVFa1gVCktLncACAEAAwIAA3kABx4E",
            caption=PROMOTE_MESSAGE,
            reply_markup=KEYBOARDS
        )    
    except BadRequest as exc:
        return await message.reply(f"Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ Wʜɪʟᴇ Pʀᴏᴍᴏᴛɪɴɢ : {exc.message}")
    except Exception as exs:
        return await message.reply_text(f"Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ Wʜɪʟᴇ Pʀᴏᴍᴏᴛɪɴɢ : {exs}"})

@app.on_callback_query(filters.regex(pattern=r"demote_(.*)"))
async def demote_perses(app:Client, query:CallbackQuery) -> None:
    user = query.from_user
    chat = query.message.chat
    newers = query.data.split("_")
    if int(newers[1]) == user.id:
        mention = (await app.get_users(newers[1])).mention
        await app.promote_chat_member(chat.id, int(newers[2]), DEMOTE_USER)
        await query.message.edit_caption(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇᴍᴏᴛᴇᴅ Tʜᴇ Usᴇʀ {mention}.")
    else:
        await app.answer_callback_query(query.id, "Yᴏᴜ Dɪᴅɴ'ᴛ Pʀᴏᴍᴏᴛᴇᴅ Tʜᴀᴛ Usᴇʀ !")

@app.on_callback_query(filters.regex(pattern=r"mpromote_(.*)"))
async def promote_perses(app:Client, query:CallbackQuery) -> None:
    user = query.from_user
    chat = query.message.chat
    bot = await app.get_chat_member(chat.id, app.me.id)
    FULL_PROMOTE_USER = ChatPrivileges(
        can_change_info=bot.privileges.can_change_info,
        can_invite_users=bot.privileges.can_invite_users,
        can_delete_messages=bot.privileges.can_delete_messages,
        can_restrict_members=bot.privileges.can_restrict_members,
        can_pin_messages=bot.privileges.can_pin_messages,
        can_promote_members=bot.privileges.can_promote_members,
        can_manage_chat=bot.privileges.can_manage_chat,
        can_manage_video_chats=bot.privileges.can_manage_video_chats,
    )
    newers = query.data.split("_")
    if int(newers[1]) == user.id:
        mention = (await app.get_users(newers[1])).mention
        await app.promote_chat_member(chat.id, int(newers[2]), FULL_PROMOTE_USER)
        await query.message.edit_caption(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Fᴜʟʟ Pʀᴏᴍᴏᴛᴇᴅ Tʜᴇ Usᴇʀ {mention}.")
    else:
        await app.answer_callback_query(query.id, "Yᴏᴜ Dɪᴅɴ'ᴛ Pʀᴏᴍᴏᴛᴇᴅ Tʜᴀᴛ Usᴇʀ !")

@pgram.on_message(command(commands=("demote")))
async def _demote_user(app, message:Message) -> None:
    if len(message.command) == 1:
        return await message.reply("sʏɴᴛᴀx: ɢɪᴠᴇ ᴍᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ ᴛᴏ ᴅᴇᴍᴏᴛᴇ")
    user = message.command[1]
    xxx = await app.get_chat_member(message.chat.id, user)
    if not xxx.privileges:    
        return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ɪsɴ'ᴛ ᴀɴ ᴀᴅᴍɪɴ ᴀɴʏᴡᴀʏ!")
    mention = xxx.user.mention
    try: 
        await app.promote_chat_member(message.chat.id, xxx.user.id, DEMOTE_USER)
        await message.reply_text(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇᴍᴏᴛᴇᴅ {mention} !")
    except BadRequest as exc:
        return await message.reply(f"ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇᴍᴏᴛɪɴɢ : {exc.message}")           

KEYBOARDS_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏsᴇ",callback_data="admin_close")]])
        
@app.on_chat_member_updated()
async def _members_actions(app, message:Message) -> None:
    chat = message.chat
    old_user = message.old_chat_member
    new_user = message.new_chat_member
    try:
        if old_user.status == ChatMemberStatus.ADMINISTRATOR:
            if new_user.status == ChatMemberStatus.MEMBER:
                await app.send_message(
                    chat_id=chat.id,
                    text=f"#ᴅᴇᴍᴏᴛᴇᴅ_ᴜsᴇʀ\n» ᴀ ɴᴇᴡ ᴄʜᴀᴛ ᴀᴄᴛɪᴠɪᴛʏ ʜᴀᴘᴘᴇɴᴇᴅ {message.from_user.mention} ᴅᴇᴍᴏᴛᴇᴅ {new_user.user.mention} !",
                    reply_markup=KEYBOARDS_BUTTON
                )
        if old_user.status != ChatMemberStatus.ADMINISTRATOR and new_user.status == ChatMemberStatus.ADMINISTRATOR:  
            if not new_user.custom_title:      
                await app.send_message(
                    chat_id=chat.id,
                    text=f"#ᴘʀᴏᴍᴏᴛᴇᴅ_ᴜsᴇʀ\n» ᴀ ɴᴇᴡ ᴄʜᴀᴛ ᴀᴄᴛɪᴠɪᴛʏ ʜᴀᴘᴘᴇɴᴇᴅ {message.from_user.mention} ᴘʀᴏᴍᴏᴛᴇᴅ {new_user.user.mention} !",
                    reply_markup=KEYBOARDS_BUTTON
                )         
            if new_user.custom_title:
                await app.send_message(
                    chat_id=chat.id,
                    f"#ᴘʀᴏᴍᴏᴛᴇᴅ_ᴜsᴇʀ\n» ᴀ ɴᴇᴡ ᴄʜᴀᴛ ᴀᴄᴛɪᴠɪᴛʏ ʜᴀᴘᴘᴇɴᴇᴅ {message.from_user.mention} ᴘʀᴏᴍᴏᴛᴇᴅ {new_user.user.mention} ᴡɪᴛʜ ᴛɪᴛʟᴇ {new_user.custom_title} !",
                    reply_markup=KEYBOARDS_BUTTON
                )
    except Exception:
        pass
