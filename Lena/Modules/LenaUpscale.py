import os
import asyncio
import requests
from io import BytesIO
from Lena import LenaAi, app
from pyrogram import Client, filters, LOGGER
from pyrogram.types import Message

LENA_AI_API_KEY = LenaAi
LENA_AI_API_ENDPOINT = 'https://api.chatai.net/v1/upscaling'

async def upscaleImage(image_url):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': LENA_AI_API_KEY,
        }
        data = {
            'image_url': image_url,
            'scale_factor': 2,
        }

        response = await app.session.post(LENA_AI_API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()

        image_content = await response.read()
        return BytesIO(image_content)

    except requests.RequestException as e:
        LOGGER.info(f"Error During Image Upscaling : {str(e)}")
        return None

@app.on_message(filters.command("upscale"))
async def upscaleCommand(client: Client, message: Message):
    try:
        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1]

            file_path = await app.download_media(photo)
            upscaled_image = await upscaleImage(file_path)
            if upscaled_image:
                await message.reply_photo(
                    photo=upscaled_image,
                    caption="**LenaAi Upscale Done !**"
                )
            else:
                await message.reply("**Lena Error : During Image Upscaling.**")

    except Exception as e:
        LOGGER.info(f"Unexpected Error : {str(e)}")
