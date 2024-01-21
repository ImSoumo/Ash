import os
import datetime
from Lena import app, BOT_NAME
from pyrogram import filters , Client 
from telegraph import upload_file
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from telegraph import Telegraph

telegraph = Telegraph()
new_user = telegraph.create_account(short_name="LenaAi")
auth_url = new_user["auth_url"]

@Guardian.on_message(filters.command(["tgm","tgt"]))
async def upload_media_text_to_telegraph(app, message):
    replied = message.reply_to_message          
    if message.command[0] == "tgm":        
        if not replied:
            await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ.")
            return 
    
        elif replied.media:
            start = datetime.now()
            text = await message.reply("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ....")
            media = await replied.download()
            end = datetime.now()
            time = (end - start).seconds
            await text.edit_text(text=f"ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ {time} sᴇᴄᴏɴᴅs. ɴᴏᴡ ᴜᴘʟᴏᴀᴅɪɴɢ....", disable_web_page_preview=True)
            try:
                downloaded_file = upload_file(media)
            except Exception as error:
                LOG.print(f"[bold red]{error}")
                await text.edit(text=f"ᴇʀʀᴏʀ :- {error}", disable_web_page_preview=True)       
                return 

            try:
                os.remove(media)
            except Exception as error:
                LOG.print(f"[bold red]{error}")
                return   
            
            await text.edit(
        
        text=f"""
๏ **ᴅᴏɴᴇ !**
๏ **ʟɪɴᴋ :** `https://graph.org{downloaded_file[0]}`
๏ **ʀᴇϙᴜᴇsᴛᴇᴅ ʙʏ :** {message.from_user.mention}
๏ **ᴛɪᴍᴇ ᴛᴀᴋᴇɴ :** {time} **sᴇᴄᴏɴᴅs**                
        """,        
        reply_markup=InlineKeyboardMarkup( [
            [
            InlineKeyboardButton(text="๏ ʙʀᴏᴡsᴇ ๏", url=f"https://graph.org{downloaded_file[0]}"),
            ],
            [
            InlineKeyboardButton(text="๏ ᴄʟᴏsᴇ ๏", callback_data="close")
            ],
          ]
        )
      )

            
        else:
            await message.reply_text("ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛ ᴍᴇᴅɪᴀ!")
            return 

    if message.command[0] == "tgt":        
        if not replied:
            await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ  ᴛᴇʟᴇɢʀᴀᴘʜ")
            return 
    
        elif replied.text:
            text = await message.reply("ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ....")
            response = telegraph.create_page(title=BOT_NAME,html_content=(replied.text.html).replace("\n", "<br>"),author_name=str(message.from_user.first_name),author_url = f'https://telegram.dog/{message.from_user.username}' if message.from_user.id else None)
            await message.reply_text(
        text=f'''
๏ **ᴅᴏɴᴇ !**
๏ **ʟɪɴᴋ:** `https://telegra.ph/{response["path"]}`
๏ **ʀᴇϙᴜᴇsᴛᴇᴅ ʙʏ :** {message.from_user.mention}
        ''',
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [
            [
            InlineKeyboardButton(text="๏ ʙʀᴏᴡsᴇ ๏", url=f'https://telegra.ph/{response["path"]}'),
            ],
            [
            InlineKeyboardButton(text="๏ ᴄʟᴏsᴇ ๏", callback_data="close")
            ],
          ]
        )
      )
        else:
            await message.reply_text("ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛ ᴛᴇxᴛ!!")
            return                  
