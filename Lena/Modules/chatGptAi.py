import Config
import asyncio
import openai
from pyrogram import Client, types as TS
OPENAI = "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"

chatStr = ''

async def chatModel(prompt):
    global chatStr
    openai.api_key = OPENAI
    chatStr += f"Rayen: {prompt}\nLenaAi:"
    response = client.completions.create(
        model="davinci-002",
        prompt="",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    chatStr += f"{response['choices'][0]['text']}"
    return response['choices'][0]['text']

@app.on_message()
async def lenaAi(_:Client, message:TS.Message):
    try:
        reply = await chatModel(message.text)
        await message.reply(reply)
    except Exception as e:
        await message.reply(e)
