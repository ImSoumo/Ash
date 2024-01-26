import random
import asyncio
import datetime
from pymongo import MongoClient
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
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
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
      x= await canPlay(BET_DICT[user.id],15)
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
      return await message.reply("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴇᴜʀᴏ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴇᴜʀᴏ 💷**".format(coins)) 
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
      return await message.reply("**❌ ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ** {}!\n**• ʏᴏᴜ ʟᴏsᴛ** `{}` **ᴇᴜʀᴏ 💷**\n**• ᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ** : `{}` **ᴇᴜʀᴏ 💷**".format(rnd, _bet, _wallet))
  else:
      _wallet = coins + _bet
      await game.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      return await message.reply("**❤️‍🔥 ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ** {}!\n**• ʏᴏᴜ ᴡᴏɴ** `{}` **ᴇᴜʀᴏ 💷**\n**• ᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ** : `{}` **ᴇᴜʀᴏ 💷**".format(rnd, _bet, _wallet)) 
     

@Guardian.on_message(filters.command("dart"))
async def dartFunc(_:Client, message: T.Message):
  chat = message.chat
  user = message.from_user
  if not await isPlayer(user.id):
      return await message.reply("**ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ʏᴇᴛ !**")
  if user.id not in DART_DICT.keys():
      DART_DICT[user.id] = None     
  if DART_DICT[user.id]:
      x= await canPlay(DART_DICT[user.id],15)
      if int(x) != 0:
        return await message.reply(f"**ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴅᴀʀᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ :** `{getReadableTime(x)}`.")
  if len(message.command) < 2:
      return await message.reply("**ᴏᴋ ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.**")
  _bet = message.command[1]
  coins = await userEuro(user.id)
  if _bet == '*':
      _bet = coins
  elif not _bet.isdigit():
       return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="**ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?**")
  _bet = int(_bet)
  if _bet == 0:
      return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="**ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ᴄᴏɪɴs ? ʟᴏʟ!**") 
  elif _bet > coins:
      return await message.reply("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴇᴜʀᴏ 💷 ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ :** `{}` **ᴄᴏɪɴs**".format(coins))
  m = await client.send_dice(chat_id,'🎯')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  DART_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ** `{0:,}` **ᴄᴏɪɴs**\n• **ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ** ✑ `{1:,}` **ᴄᴏɪɴs**".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("**✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ** `{0:,}` **ᴄᴏɪɴs**\n• **ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ** ✑ `{1:,}`**ᴄᴏɪɴs.**".format(to_bet,new_wallet))
     
      
@Guardian.on_message(filters.command("bowl", COMMAND_HANDLER))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username) 
  if user.id not in BOWL_DICT.keys():
      BOWL_DICT[user.id] = None     
  if BOWL_DICT[user.id]:
      x= await can_play(BOWL_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply_photo(photo=random.choice(PLAY_IMG), caption=f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ʙᴏᴡʟ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ᴏᴋ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ᴄᴏɪɴs ? ʟᴏʟ!") 
  elif to_bet > coins:
      return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴄᴏɪɴs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴄᴏɪɴs".format(coins))
  m = await client.send_dice(chat_id,'🎳')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  BOWL_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ `{0:,}` ᴄᴏɪɴs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴄᴏɪɴs".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ `{0:,}` ᴄᴏɪɴs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴄᴏɪɴs.".format(to_bet,new_wallet))
  

@Guardian.on_message(filters.command("basket", COMMAND_HANDLER))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username)  
  if user.id not in BASKET_DICT.keys():
      BASKET_DICT[user.id] = None     
  if BASKET_DICT[user.id]:
      x= await can_play(BASKET_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply_photo(photo=random.choice(PLAY_IMG), caption=f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ʙᴀsᴋᴇᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ᴏᴋ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ᴄᴏɪɴs ? ʟᴏʟ!") 
  elif to_bet > coins:
      return await message.reply_photo(photo=random.choice(PLAY_IMG), caption=_["minigames4"].format(coins))
  m = await client.send_dice(chat_id,'🏀')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  BASKET_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴄᴏɪɴs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴄᴏɪɴs".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit_caption("✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ `{0:,}` ᴄᴏɪɴs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴄᴏɪɴs.".format(to_bet,new_wallet))

                                                                                                        
    
    
regex_upvote = r"^((?i)\+|\+\+|\+1|thx|thanx|thanks|pro|cool|good|pro|pero|op|nice|noice|best|uwu|owo|right|correct|peru|piro|👍|\+100)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|baka|idiot|chutiya|nub|noob|wrong|incorrect|chaprii|chapri|weak|\-100)$"

@Guardian.on_message(
  filters.text
  & filters.group
  & filters.incoming
  & filters.reply
  & filters.regex(regex_upvote)
  & ~filters.via_bot
  & ~filters.bot,
  group=4,
)
async def upvote(client,message):
    if not message.reply_to_message.from_user:
        return
    user = message.reply_to_message.from_user
    if user.id == BOT_ID:
        return
    if not await is_player(user.id):
        await create_account(user.id,user.username)
    if user.id == message.from_user.id:
        return
    coins = await user_wallet(user.id)
    new = coins + 200
    await gamesdb.update_one({"user_id": user.id}, {'$set':{'coins' : new}})
    await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ᴀᴅᴅᴇᴅ `200` ᴄᴏɪɴs ᴛᴏ {0} ᴡᴀʟʟᴇᴛ.\n• ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴄᴏɪɴs".format(user.mention,new))
    

@Guardian.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.me
    & ~filters.bot,
    group=3,  
)
async def downvote(client,message,_):
    if not message.reply_to_message.from_user:
        return
    user = message.reply_to_message.from_user
    if user.id == BOT_ID:
        return
    if not await is_player(user.id):
        await create_account(user.id)
    if user.id == message.from_user.id:
        return
    coins = await user_wallet(user.id,user.username)
    if coins <= 0:
        return
    else:
        new = coins - 200
    await gamesdb.update_one({"user_id": user.id}, {'$set':{'coins' : new}})
    await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ᴛᴏᴏᴋ `200` ᴄᴏɪɴs ғʀᴏᴍ {𝟶} ᴡᴀʟʟᴇᴛ.\n• ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{𝟷:,}` ᴄᴏɪɴs".format(user.mention,new))
    
    
    

@Guardian.on_message(filters.command("pay", COMMAND_HANDLER) & filters.group)
async def _pay(client,message):
    if not message.reply_to_message:
        return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ")
    to_user =  message.reply_to_message.from_user
    from_user = message.from_user
    if to_user.id == from_user.id:
        if message.from_user.id not in SUPREME_USERS:
            return
    if not await is_player(to_user.id):
        await create_account(to_user.id,to_user.username)
    if not await is_player(from_user.id):
        await create_account(from_user.id,from_user.username)
    if len(message.command) < 2:
        return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ᴜsᴀɢᴇ : /pay `100`")
    amount = message.command[1]
    to_pay =  message.command[1].lower()
    tcoins = await user_wallet(to_user.id)
    fcoins = await user_wallet(from_user.id)
    if amount == '*':
        if message.from_user.id not in SUPREME_USERS:
            amount = fcoins
    elif not amount.isdigit():
       return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
    amount = int(amount)
    if amount == 0:
        return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴡᴀɴɴᴀ 𝟶 ᴄᴏɪɴs ʟᴏʟ!") 
    elif amount > fcoins:
        if message.from_user.id not in SUPREME_USERS:
            return await message.reply_photo(photo=random.choice(PLAY_IMG), caption="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴄᴏɪɴs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴄᴏɪɴs".format(fcoins))
    if message.from_user.id not in SUPREME_USERS:
        await gamesdb.update_one({'user_id' : to_user.id},{'$set' : {'coins' : tcoins + amount }})
        await gamesdb.update_one({'user_id' : from_user.id},{'$set' : {'coins' : fcoins - amount }})
    else:
        await gamesdb.update_one({'user_id' : to_user.id},{'$set' : {'coins' : tcoins + amount }})
    await message.reply_photo(photo=random.choice(PLAY_IMG), caption="sᴜᴄᴄᴇss! {0} ᴘᴀɪᴅ {1:,} ᴄᴏɪɴs ᴛᴏ {2}.".format(from_user.mention,amount,to_user.mention))


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
    if user.id not in SUDOERS:
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
