from pyrogram import filters, types as t, errors, Client
import requests
from urllib.parse import urlsplit
import traceback
import random
import datetime
import os
import io
from Lena import app
from pyrogram.types import Message

async def SearchImages(query,search_engine) -> dict:
    response = requests.post(f"https://api.qewertyy.me/image-search/{search_engine}?query={query}&page=0")
    output = response.json()
    return output

def cleanUrl(url):
    newUrl = urlsplit(url)
    return f"{newUrl.scheme}://{newUrl.netloc}{newUrl.path}"

def getImageContent(url):
    """Get Image Content"""
    try:
        response = requests.get(cleanUrl(url))
        if response.status_code != 200:
            return None
        imageType = response.headers['content-type'].split("/")[1]
        if imageType == "gif":
            return None
        return response.content
    except (TimeoutError, requests.ReadTimeout,requests.Timeout,requests.ConnectTimeout):
        return None

@app.on_message(filters.command(["image"]))
async def searchImages(app: Client, m: Message):
    try:
        reply = await m.reply_text("`Searching...`")
        prompt = None
	if m.text is None:
            prompt = None
	if " " in m.text:
            try:
                prompt = m.text.split(None, 1)[1]
            except IndexError:
                prompt = None
	else:
            prompt = None
        if prompt is None:
            return await reply.edit("What do you want to search ?")
        output = await SearchImages(prompt,"google")
        if output['code'] != 2:
            return await reply.edit("Ran into an error.")
        images = output['content']
        if len(images) == 0:
            return await reply.edit("No images found.")
        images = random.choices(images,k=8 if len(images) > 8 else len(images))
        media = []
        for image in images:
            content = getImageContent(image['imageUrl'])
            if content is None:
                images.remove(image)
                continue
            else:
                media.append(t.InputMediaPhoto(io.BytesIO(content)))
        await m.reply_media_group(
            media,
            quote=True
            )
        await reply.delete()
    except (errors.ExternalUrlInvalid, errors.WebpageCurlFailed,errors.WebpageMediaEmpty) as e:
        print(e)
        return await reply.edit("Ran into an error.")
    except Exception as e:
        traceback.print_exc()
        return await reply.edit("Ran into an error.")
