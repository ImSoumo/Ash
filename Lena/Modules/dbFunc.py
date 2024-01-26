from Lena import app, SUDOERS
from pyrogram import Client, filters, types as T
from Lena.Modules.LenaRankings import rankdb, ranser

@app.on_message(filters.command("reset_rank") & SUDOERS)
async def resetRankings(_, message: T.Message):
    msg = await message.reply("**Pʀᴏᴄᴇssɪɴɢ...**")
    await rankdb.delete_many({})
    await ranser.delete_many({})
    await msg.edit("**Oᴋ Dᴏɴᴇ !**")
                                
