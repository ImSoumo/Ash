import random
import asyncio
import pymongo
import datetime
from pymongo import MongoClient
from Config import SUDO_USERS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Lena import app, BOT_ID, SUDOERS, db
from pyrogram import Client, filters, types as T

def getReadableTime(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅᴀʏs"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

#| Game DB Codes Functions 
game = db.game

async def createAccount(user, name):
  Func = {
  'user_id' : user,
    '_user': name,
    'euro' : 5000,
  }
  return game.insert_one(Func)

async def isPlayer(user):
  return bool(await game.find_one({"user_id" : user}))
  
async def userEuro(user_id):
    Player = await game.find_one({"user_id" : user_id})
    if not Player:
        return 0
    return Player['euro']
#| Game DB Codes Functions End !

BET_DICT = {}
DART_DICT = {}
BOWL_DICT = {}
BASKET_DICT = {}

async def getUserWon(emoji,value):
    if emoji in ['🎯','🎳']:
        if value >= 4:
            u_won = True
        else:
            u_won = False
    elif emoji in ['🏀','⚽'] :
        if value >= 3:
            u_won = True
        else:
            u_won = False
    return u_won

async def canPlay(tame, tru):
  current_time = datetime.datetime.now()
  time_since_last_collection = current_time - datetime.datetime.fromtimestamp(tame)
  x = tru - time_since_last_collection.total_seconds()
  if str(x).startswith('-'):
      return 0
  return x

@app.on_message(filters.command("bet"))
async def betFunc(_:Client, message: T.Message):
  chat = message.chat
  user = message.from_user
  if not await isPlayer(user.id):
     return await message.reply("**ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**")
  if user.id not in BET_DICT.keys():
      BET_DICT[user.id] = None     
  if BET_DICT[user.id]:
      x = await canPlay(BET_DICT[user.id],15)
      print(x)
      if int(x) != 0:
        return await message.reply(f"**ʏᴏᴜ ᴄᴀɴ ʙᴇᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ {getReadableTime(x)}.**")     
  possible = ['h','heads','tails','t','head','tail']
  if len(message.command) < 3:
      return await message.reply("**Usᴀɢᴇ : /ʙᴇᴛ [ᴀᴍᴏᴜɴᴛ] [ʜᴇᴀᴅs/ᴛᴀɪʟs]**")
  _bet = message.command[1]
  comnd = message.command[2].lower()
  coins = await userEuro(user.id)
  if _bet == '*':
      _bet = coins
  elif not _bet.isdigit():
       return await message.reply("**ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ ?**")
  _bet = int(_bet)
  if to_bet == 0:
      return await message.reply("**ʜᴀɪɴ ? ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ᴇᴜʀᴏ !**") 
  elif _bet > coins:
      return await message.reply("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴇᴜʀᴏ 💷 ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷**".format(coins)) 
  rand = random.choice(['heads','tails'])
  if comnd not in possible:
      return await message.reply("**ʏᴏᴜ sʜᴏᴜʟᴅ ᴛʀʏ ʜᴇᴀᴅs ᴏʀ ᴇɪᴛʜᴇʀ ᴛᴀɪʟs.**")
  if comnd in ['h','head','heads']:
      if rand == 'heads':
          _won = True         
      else:
          _won = False
  if comnd in ['t','tail','tails']:
      if rand == 'tails':
          _won = True
      else:
          _won = False
  BET_DICT[user.id] = datetime.datetime.now().timestamp()
  if not _won:
      _wallet = coins - _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'euro' : _wallet}})
      return await message.reply("**❌ ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ {} ʏᴏᴜ ʟᴏsᴛ** `{}` **ᴇᴜʀᴏ 💷 !**\n**• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷**".format(rnd, _bet, _wallet))
  else:
      _wallet = coins + _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      return await message.reply("**❤️‍🔥 ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ {} ʏᴏᴜ ᴡᴏɴ** `{}` **ᴇᴜʀᴏ 💷 !**\n**• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷.**".format(rnd, _bet, _wallet)) 
     

@app.on_message(filters.command("dart"))
async def dartFunc(_:Client, message: T.Message):
  chat = message.chat
  user = message.from_user
  if not await isPlayer(user.id):
      return await message.reply("**ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**")
  if user.id not in DART_DICT.keys():
      DART_DICT[user.id] = None     
  if DART_DICT[user.id]:
      x = await canPlay(DART_DICT[user.id],15)
      if int(x) != 0:
        return await message.reply(f"**ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴅᴀʀᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ :** `{getReadableTime(x)}`.")
  if len(message.command) < 2:
      return await message.reply("**ᴏᴋ ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.**")
  _bet = message.command[1]
  coins = await userEuro(user.id)
  if _bet == '*':
      _bet = coins
  elif not _bet.isdigit():
       return await message.reply("**ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ ?**")
  _bet = int(_bet)
  if _bet == 0:
      return await message.reply("**ʜᴀɪɴ ? ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ᴇᴜʀᴏ !**") 
  elif _bet > coins:
      return await message.reply("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴇᴜʀᴏ 💷 ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷.**".format(coins))
  m = await client.send_dice(chat_id,'🎯')
  msg = await message.reply('....')
  _won = await getUserWon(m.dice.emoji, m.dice.value)
  DART_DICT[user.id] = datetime.datetime.now().timestamp()
  if not _won:
      _wallet = coins - _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'euro' : _wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**❌ sᴀᴅ ᴛᴏ sᴀʏ ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ** `{}` **ᴇᴜʀᴏ 💷**\n**• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷.**".format(_bet, _wallet))
  else:
      _wallet = coins + _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'euro' : _wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**❤️‍🔥 ᴡᴏᴡ ! ʏᴏᴜ ᴡᴏɴ** `{}` **ᴇᴜʀᴏ 💷**\n• **ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}`**ᴇᴜʀᴏ 💷.**".format(_bet, _wallet))
     
      
@app.on_message(filters.command("bowl"))
async def bowlFunc(_:Client, message: T.Message):
  chat = message.chat
  user = message.from_user
  if not await isPlayer(user.id):
      return await message.reply("**ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**") 
  if user.id not in BOWL_DICT.keys():
      BOWL_DICT[user.id] = None     
  if BOWL_DICT[user.id]:
      x = await canPlay(BOWL_DICT[user.id],15)
      if int(x) != 0:
        return await message.reply(f"**ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ʙᴏᴡʟ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ :** `{get_readable_time(x)}`.")
  if len(message.command) < 2:
      return await message.reply("**ᴏᴋ ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.**")
  _bet = message.command[1]
  coins = await userEuro(user.id)
  if _bet == '*':
      _bet = coins
  elif not _bet.isdigit():
       return await message.reply("**ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ ?**")
  _bet = int(_bet)
  if _bet == 0:
      return await message.reply("**ʜᴀɪɴ ? ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ᴇᴜʀᴏ !**") 
  elif _bet > coins:
      return await message.reply("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴇᴜʀᴏ 💷 ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷.**".format(coins))
  m = await client.send_dice(chat_id,'🎳')
  msg = await message.reply('....')
  _won = await getUserWon(m.dice.emoji, m.dice.value)
  BOWL_DICT[user.id] = datetime.datetime.now().timestamp()
  if not _won:
      _wallet = coins - _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'euro' : _wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**❌ sᴀᴅ ᴛᴏ sᴀʏ ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ** `{}` **ᴇᴜʀᴏ 💷**\n**• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷.**".format(_bet, _wallet))
  else:
      _wallet = coins + _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'euro' : _wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**❤️‍🔥 ᴡᴏᴡ ! ʏᴏᴜ ᴡᴏɴ** `{}` **ᴇᴜʀᴏ 💷**\n• **ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}`**ᴇᴜʀᴏ 💷.**".format(_bet, _wallet))
  

@app.on_message(filters.command("basket"))
async def basketFunc(_:Client, message: T.Message):
  chat = message.chat
  user = message.from_user
  if not await isPlayer(user.id):
      return await message.reply("**ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**")
  if user.id not in BASKET_DICT.keys():
      BASKET_DICT[user.id] = None     
  if BASKET_DICT[user.id]:
      x = await canPlay(BASKET_DICT[user.id],15)
      if int(x) != 0:
        return await message.reply(f"**ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ʙᴀsᴋᴇᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ :** `{get_readable_time(x)}`.**")
  if len(message.command) < 2:
      return await message.reply("**ᴏᴋ ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.**")
  _bet = message.command[1]
  coins = await userEuro(user.id)
  if _bet == '*':
      _bet = coins
  elif not _bet.isdigit():
       return await message.reply("**ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ ?**")
  _bet = int(_bet)
  if _bet == 0:
      return await message.reply("**ʜᴀɪɴ ? ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ᴇᴜʀᴏ !**") 
  elif _bet > coins:
      return await message.reply("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴇᴜʀᴏ 💷 ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷.**".format(coins))
  m = await client.send_dice(chat_id,'🏀')
  msg = await message.reply('....')
  _won = await getUserWon(m.dice.emoji, m.dice.value)
  BASKET_DICT[user.id] = datetime.datetime.now().timestamp()
  if not _won:
      _wallet = coins - _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'euro' : _wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**❌ sᴀᴅ ᴛᴏ sᴀʏ ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ** `{}` **ᴇᴜʀᴏ 💷**\n**• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷.**".format(_bet, _wallet))
  else:
      _wallet = coins + _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'euro' : _wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**❤️‍🔥 ᴡᴏᴡ ! ʏᴏᴜ ᴡᴏɴ** `{}` **ᴇᴜʀᴏ 💷**\n• **ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ :** `{}`**ᴇᴜʀᴏ 💷.**".format(_bet, _wallet))

                                                                                                            
upvote = r"^((?i)\+|\+\+|\+1|thx|thanx|thanks|pro|cool|good|pro|pero|op|nice|noice|best|uwu|owo|right|correct|peru|piro|👍|\+100)$"
downvote = r"^(\-|\-\-|\-1|👎|noob|baka|idiot|chutiya|nub|noob|wrong|incorrect|chaprii|chapri|weak|\-100)$"

@app.on_message(
  filters.text
  & filters.group
  & filters.incoming
  & filters.reply
  & filters.regex(upvote)
  & ~filters.via_bot
  & ~filters.bot,
  group= 5,
)
async def upvoteFunc(_:Client, message:T.Mesage):
    if not message.reply_to_message.from_user:
        return
    user = message.reply_to_message.from_user
    if user.id == BOT_ID:
        return
    if not await isPlayer(user.id):
        await createAccount(user.id, user.username)
    if user.id == message.from_user.id:
        return
    coins = await userEuro(user.id)
    _new = coins + 150
    await game.update_one({"user_id": user.id}, {'$set':{'euro' : _new}})
    await message.reply("**ᴀᴅᴅᴇᴅ** `150` **ᴇᴜʀᴏ 💷 ᴛᴏ {} ᴡᴀʟʟᴇᴛ.**".format(user.mention))
    
@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(downvote)
    & ~filters.via_bot
    & ~filters.me
    & ~filters.bot,
    group=3,  
)
async def downvoteFunc(_:Client, message:T.Message):
    if not message.reply_to_message.from_user:
        return
    user = message.reply_to_message.from_user
    if user.id == BOT_ID:
        return
    if not await isPlayer(user.id):
        await createAccount(user.id)
    if user.id == message.from_user.id:
        return
    coins = await userEuro(user.id)
    _new = coins - 250
    await game.update_one({"user_id": user.id}, {'$set':{'euro' : _new}})
    await message.reply("**ᴛᴏᴏᴋ** `250` **ᴇᴜʀᴏ 💷 ғʀᴏᴍ {} ᴡᴀʟʟᴇᴛ.**".format(user.mention))
    
    
@app.on_message(filters.command("pay") & filters.group)
async def payFunc(_:Client, message: T.Message):
    if not message.reply_to_message:
        return await message.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ !**")
    _user =  message.reply_to_message.from_user
    _from = message.from_user
    if _user.id == _from.id:
        if message.from_user.id not in SUDO_USERS:
            return
    if not await isPlayer(_user.id):
        return await message.reply("**ʀᴇᴄɪᴠᴇʀ ᴅᴏᴇꜱɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʙᴏᴛ ʏᴇᴛ !")
    if not await is_player(_from.id):
        return return await message.reply("**ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**")
    if len(message.command) < 2:
        return await message.reply("**Usᴀɢᴇ : /ᴘᴀʏ** `100`")
    amount = message.command[1]
    _pay =  message.command[1].lower()
    tcoins = await userEuro(_user.id)
    fcoins = await userEuro(_from.id)
    if amount == '*':
        if message.from_user.id not in SUDO_USERS:
            amount = fcoins
    elif not amount.isdigit():
       return await message.reply("**ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ ?**")
    amount = int(amount)
    if amount == 0:
        return await message.reply("**ʏᴏᴜ ᴄᴀɴ'ᴛ ᴘᴀʏ** `0` **ᴇᴜʀᴏ 💷 !**") 
    elif amount > fcoins:
        if message.from_user.id not in SUDO_USERS:
            return await message.reply("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴇᴜʀᴏ 💷 !**")
    if message.from_user.id not in SUDO_USERS:
        await game.update_one({'user_id' : _user.id},{'$set' : {'euro' : tcoins + amount }})
        await game.update_one({'user_id' : _from.id},{'$set' : {'euro' : fcoins - amount }})
    else:
        await game.update_one({'user_id' : _user.id},{'$set' : {'euro' : tcoins + amount }})
    await message.reply("**sᴜᴄᴄᴇss ! {} ᴘᴀɪᴅ** `{}` **ᴇᴜʀᴏ 💷 ᴛᴏ {}.**".format(_from.mention, amount, _user.mention))


@app.on_message(filters.command("gtop"))
async def topUsers(_:Client, message: T.Message): 
    x = game.find().sort("euro", pymongo.DESCENDING)
    msg = "**✨ ɢʟᴏʙᴀʟ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ ᴏꜰ ᴇᴜʀᴏ 💷 :\n\n"
    counter = 1
    for i in await x.to_list(length=None):
        if counter == 26:
            break
        if i["euro"] == 0:
            pass
        else:
            user = i["user_id"]
            sugg = i["_user"]
            link = f"[{sugg}](tg://user?id={user})"
            if not sugg:
                _check = i["user_id"]
                try:
                    link = (await app.get_chat(_check)).mention
                except Exception as e:
                    link = _check
            
            euro = i["euro"]
            if counter == 1:
               msg += f"{counter:2d}.** {link}** : `{euro}`\n"
                
            else:
                msg += f"{counter:2d}.** {link}** : `{euro}`\n"
            counter += 1
    await message.reply(msg, disable_web_page_preview=True)
    
@app.on_message(filters.command("wallet"))
async def userBalance(_:Client, message: T.Message):
    user = message.from_user
    if not await isPlayer(user.id):
        return await message.reply("**ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**")
    check = await userEuro(user.id)
    await message.reply("**ᴄᴜʀʀᴇɴᴛ ᴇᴜʀᴏ 💷 ᴡᴀʟʟᴇᴛ ᴏꜰ ᴜꜱᴇʀ {} :** `{}` ".format(user.mention, check))

@app.on_message(filters.command("add_euro"))
async def addFuncs(_: Client, message: T.Message):
    user = message.from_user
    if user.id not in SUDO_USERS:
        return await message.reply("**ɴᴏᴛ ᴀᴜᴛʜᴏʀɪꜱᴇᴅ !**")
    if not message.reply_to_message:
        return await message.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ !**")
    if not message.reply_to_message.from_user:
        return await message.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ !**")
    _user = message.reply_to_message.from_user
    if not await isPlayer(_user.id):
        return await message.reply("**ᴜꜱᴇʀ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**")
    if len(message.command) < 2:
        return await message.reply("**ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟᴜᴇ ᴛᴏ ᴀᴅᴅ ᴇᴜʀᴏ 💷 ᴛᴏ ᴜꜱᴇʀ...**")
    _euro = message.command[1]
    if not _euro.isdigit():
        return await message.reply("**ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴠᴀʟᴜᴇ ɪs ɴᴏᴛ ᴀ ɪɴᴛᴇɢᴇʀ...**")
    _euro = int(await userEuro(_user.id) + int(_euro)
    await game.update_one({'user_id' : _user.id},{'$set' : {'euro' : _euro }})
    return await message.reply(f"**ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴇᴜʀᴏ 💷 ᴛo ᴜsᴇʀ {_user.mention} !**")
