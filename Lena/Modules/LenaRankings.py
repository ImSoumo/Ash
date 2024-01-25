import time
import asyncio
from Lena import app, db
from datetime import date
from pyrogram import Client, filters, types as T
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# | Rankings DB Functions
rankdb = db.rank

async def increaseCount(chat, user):
    user = str(user)
    today = str(date.today())
    user_db = await rankdb.find_one({"chat": chat})

    if not user_db:
        user_db = {}
    elif not user_db.get(today):
        user_db = {}
    else:
        user_db = user_db[today]

    if user in user_db:
        user_db[user] += 1
    else:
        user_db[user] = 1
    await rankdb.update_one({"chat": chat}, {"$set": {today: user_db}}, upsert=True)

#| Rankings DB Get User Name Function
name_cache = {}

async def getName(app, id):
    global name_cache

    if id in name_cache:
        return name_cache[id]
    else:
        try:
            i = await app.get_users(id)
            i = f'{(i.mention)}'
            name_cache[id] = i
            return i
        except:
            return id
#| End Rankings DB Functions

@app.on_message(
    ~filters.bot
    & ~filters.forwarded
    & filters.group
    & ~filters.via_bot
    & ~filters.service
)
async def incUser(_, message: T.Message):
    if message.text:
        if (
            message.text.strip() == "/rankings@LenaAiBot"
            or message.text.strip() == "/rankings"
        ):
            return await showTopToday(_, message)

    chat = message.chat.id
    user = message.from_user.id
    await increaseCount(chat, user)
    print(chat, user, "Increased !")


async def showTopToday(_, message: T.Message):
    print("Today's Top In", message.chat.id)
    chat = await rankdb.find_one({"chat": message.chat.id})
    today = str(date.today())

    if not chat:
        return await message.reply_photo(
            photo="https://telegra.ph//file/3f12d7ceb3aaa0eec6999.jpg",
            caption="**ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !**"
        )
    if not chat.get(today):
        return await message.reply_photo(
            photo="https://telegra.ph//file/3f12d7ceb3aaa0eec6999.jpg",
            caption="**ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛᴏᴅᴀʏ !**"
        )
    txt = "**🔰 Tᴏᴅᴀʏ's Tᴏᴘ Rᴀɴᴋɪɴɢs :**\n\n"

    pos = 1
    for i, k in sorted(chat[today].items(), key=lambda x: x[1], reverse=True)[:10]:
        i = await getName(app, i)
        txt += f"**{pos}. {i}** · `{k}`\n"
        pos += 1
    total = sum(chat[today].values())
    txt += f"\n**✉️ Tᴏᴅᴀʏ's Mᴇssᴀɢᴇs :** `{total}`"
    
    await message.reply_photo(
        photo="https://telegra.ph/file/55d2355063707105d71ca.jpg",
        caption=txt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Oᴠᴇʀᴀʟʟ Rᴀɴᴋɪɴɢs", callback_data="overAll_")
                ],
                [
                    InlineKeyboardButton("Rᴇғʀᴇsʜ", callback_data="overFresh_"),
                    InlineKeyboardButton("Cʟᴏsᴇ", callback_data="closeRank_")
                ]
            ]
        ),
    )

cooldowns = {}
COOLDOWN_DURATION = 20

@app.on_callback_query()
async def callbackOverall(app, query: CallbackQuery):
    user_id = query.from_user.id
    
    if user_id in cooldowns and time.time() - cooldowns[user_id] < COOLDOWN_DURATION:
        remaining_time = int(COOLDOWN_DURATION - (time.time() - cooldowns[user_id]))
        await app.answer_callback_query(
            query.id,
            f"Wᴀɪᴛ {remaining_time} Sᴇᴄᴏɴᴅs Cᴏᴏʟᴅᴏᴡɴ Rᴇᴍᴀɪɴɪɴɢ ! Dᴏɴ'ᴛ sᴘᴀᴍ."
        )
        return
    else:
        cooldowns[user_id] = time.time()
        if query.data =="overAll_":
            print("Overall Top In", query.message.chat.id)
            chat = await rankdb.find_one({"chat": query.message.chat.id})

            if not chat:
                return await query.answer("ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)

            await query.answer("Pʀᴏᴄᴇssɪɴɢ... Pʟᴇᴀsᴇ Wᴀɪᴛ")
            txt = "**🔰 Oᴠᴇʀᴀʟʟ Tᴏᴘ Rᴀɴᴋɪɴɢs :**\n\n"

            overall_dict = {}
            total = 0
            for i, k in chat.items():
                if i == "chat" or i == "_id":
                    continue

                for j, l in k.items():
                    if j not in overall_dict:
                        overall_dict[j] = l
                    else:
                        overall_dict[j] += l
                total += sum(k.values())
            pos = 1
            for i, k in sorted(overall_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
                i = await getName(app, i)
                txt += f"**{pos}. {i}** · `{k}`\n"
                pos += 1
            txt += f"\n**✉️ Tᴏᴛᴀʟ Mᴇssᴀɢᴇs :** `{total}`"

            await query.message.edit_caption(
                txt,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Tᴏᴅᴀʏ's Rᴀɴᴋɪɴɢs", callback_data="today_")
                        ],
                        [
                            InlineKeyboardButton("Rᴇғʀᴇsʜ", callback_data="todayFresh_"),
                            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="closeRank_")
                        ]
                    ]
                )
            )
          
        elif query.data =="today_":
            print("Today Top In", query.message.chat.id)
            chat = await rankdb.find_one({"chat": query.message.chat.id})
            today = str(date.today())

            if not chat:
                return await query.answer("ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)

            if not chat.get(today):
                return await query.answer("ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛᴏᴅᴀʏ !", show_alert=True)
              
            await query.answer("Pʀᴏᴄᴇssɪɴɢ... Pʟᴇᴀsᴇ Wᴀɪᴛ")
            txt = "**🔰 Tᴏᴅᴀʏ's Tᴏᴘ Rᴀɴᴋɪɴɢs :**\n\n"

            pos = 1
            for i, k in sorted(chat[today].items(), key=lambda x: x[1], reverse=True)[:10]:
                i = await getName(app, i)
                txt += f"**{pos}. {i}** · `{k}`\n"
                pos += 1
            total = sum(chat[today].values())
            txt += f"\n**✉️ Tᴏᴅᴀʏ's Mᴇssᴀɢᴇs :** `{total}`"

            await query.message.edit_caption(
                txt,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Oᴠᴇʀᴀʟʟ Rᴀɴᴋɪɴɢs", callback_data="overAll_")
                        ],
                        [
                            InlineKeyboardButton("Rᴇғʀᴇsʜ", callback_data="overFresh_"),
                            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="closeRank_")
                        ]
                    ]
                )
            )

        elif query.data =="overFresh_":
            print("Refreshed Overall Top In", query.message.chat.id)
            chat = await rankdb.find_one({"chat": query.message.chat.id})

            if not chat:
                return await query.answer("ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)

            msg = await query.message.edit_caption("**Rʀᴇғʀᴇsʜɪɴɢ...**")
            await query.answer("Rʀᴇғʀᴇsʜɪɴɢ... Pʟᴇᴀsᴇ Wᴀɪᴛ")
            txt = "**🔰 Rᴇғʀᴇsʜᴇᴅ Oᴠᴇʀᴀʟʟ Tᴏᴘ Rᴀɴᴋɪɴɢs :**\n\n"

            overall_dict = {}
            total = 0
            for i, k in chat.items():
                if i == "chat" or i == "_id":
                    continue

                for j, l in k.items():
                    if j not in overall_dict:
                        overall_dict[j] = l
                    else:
                        overall_dict[j] += l
                total += sum(k.values())
            pos = 1
            for i, k in sorted(overall_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
                i = await getName(app, i)
                txt += f"**{pos}. {i}** · `{k}`\n"
                pos += 1
            txt += f"\n**✉️ Tᴏᴛᴀʟ Mᴇssᴀɢᴇs :** `{total}`"

            await msg.edit_text(
                txt,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Tᴏᴅᴀʏ's Rᴀɴᴋɪɴɢs", callback_data="today_")
                        ],
                        [
                            InlineKeyboardButton("Rᴇғʀᴇsʜ", callback_data="todayFresh_"),
                            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="closeRank_")
                        ]
                    ]
                )
            )

        elif query.data =="todayFresh_":
            print("Today Top In", query.message.chat.id)
            chat = await rankdb.find_one({"chat": query.message.chat.id})
            today = str(date.today())

            if not chat:
                return await query.answer("ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)

            if not chat.get(today):
                return await query.answer("ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛᴏᴅᴀʏ !", show_alert=True)

            msg = await query.message.edit_caption("**Rʀᴇғʀᴇsʜɪɴɢ...**")
            await query.answer("Rʀᴇғʀᴇsʜɪɴɢ... Pʟᴇᴀsᴇ Wᴀɪᴛ")
            txt = "**🔰 Rᴇғʀᴇsʜᴇᴅ Tᴏᴅᴀʏ's Tᴏᴘ Rᴀɴᴋɪɴɢs :**\n\n"

            pos = 1
            for i, k in sorted(chat[today].items(), key=lambda x: x[1], reverse=True)[:10]:
                i = await getName(app, i)
                txt += f"**{pos}. {i}** · `{k}`\n"
                pos += 1
            total = sum(chat[today].values())
            txt += f"\n**✉️ Tᴏᴅᴀʏ's Mᴇssᴀɢᴇs :** `{total}`"

            await msg.edit_text(
                txt,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Oᴠᴇʀᴀʟʟ Rᴀɴᴋɪɴɢs", callback_data="overAll_")
                        ],
                        [
                            InlineKeyboardButton("Rᴇғʀᴇsʜ", callback_data="overFresh_"),
                            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="closeRank_")
                        ]
                    ]
                )
            )
        
        elif query.data =="closeRank_":
            await query.edit_caption("**Cʟᴏsᴇᴅ Cʜᴀᴛ Rᴀɴᴋɪɴɢs !**")
