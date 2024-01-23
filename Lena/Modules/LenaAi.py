"""
import openai
import asyncio
from Lena import app
from pyrogram.types import Message
from Lena.Modules.askGpt import LenaAi
from pyrogram import Client, filters
import requests

LENAGPT_API_KEY = LenaAi
LENAGPT_API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

@app.on_message(filters.command(["start"]))
async def startFunc(client: Client, message: Message):
    await message.reply("**Welcome ! Send me a message, and I'll generate a response using Lena GPT.**")
  
@app.on_message(filters.text)
async def LenaGPT(client: Client, message: Message):
    user_input = message.text
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LENAGPT_API_KEY}',
    }
    data = {
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': user_input}]
    }

    response = requests.post(LENAGPT_API_ENDPOINT, headers=headers, json=data)
    if response.status_code == 200:
        model_reply = response.json()['choices'][0]['message']['content']
        await message.reply_text(model_reply)
    else:
        await message.reply_text("**Error : Generating response from Lena GPT.**")




"""
import openai
import asyncio
import requests
from Lena import LenaAi, app
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message

LENA_GPT_API_KEY = LenaAi
LENA_GPT_API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

async def callApi(user_input):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LENA_GPT_API_KEY}',
    }
    data = {
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': user_input}]
    }

    async with ClientSession() as session:
        async with session.post(LENA_GPT_API_ENDPOINT, headers=headers, json=data) as response:
            return await response.json()

@app.on_message(filters.command(["start"]))
async def start_func(client: Client, message: Message):
    await message.reply("**Welcome! Send me a message, and I'll generate a response using Lena GPT.**")

@app.on_message(filters.text)
async def lena_gpt(client: Client, message: Message):
    user_input = message.text

    try:
        response_data = await callApi(user_input)

        if response_data.get('choices'):
            model_reply = response_data['choices'][0]['message']['content']
            await message.reply_text(model_reply)
        else:
            await message.reply_text("**Error: Generating response from Lena GPT.**")

    except Exception as e:
        await message.reply_text(f"**Error: {str(e)}**")
