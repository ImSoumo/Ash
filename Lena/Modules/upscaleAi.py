import asyncio
from lexica import AsyncClient
from pyrogram import Client, filters
from pyrogram.types import Message
from Lena import app
import os

async def getFile(message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.document is False or message.reply_to_message.photo is False:
        return None
    if message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] or message.reply_to_message.photo:
        if message.reply_to_message.document and message.reply_to_message.document.file_size > 5242880:
            return 1
        image = await message.reply_to_message.download()
        return image
    else:
        return None

async def UpscaleImages(image: bytes) -> str:
    """
    Upscales an image and return with upscaled image path !
    """
    client = AsyncClient()
    content = await client.upscale(image)
    await client.close()
    upscaled_file_path = "upscaled.png"
    with open(upscaled_file_path, "wb") as output_file:
        output_file.write(content)
    return upscaled_file_path

@app.on_message(filters.command(["upscale"]))
async def upscaleImages(app: Client, message: Message):
    file = await getFile(message)
    if file == 1:
       return await message.reply("File size is too large !")
    if file is None:
       return await message.reply("**Reply to an image ?**")
    msg = await message.reply("**Wait a min...**")
    imageBytes = open(file,"rb").read()
    os.remove(file)
    upscaledImage = await UpscaleImages(imageBytes)
    try:
      await message.reply_document(open(upscaledImage,"rb"))
      await msg.delete()
      os.remove(upscaledImage)
    except Exception as e:
       await msg.edit(f"{e}")
