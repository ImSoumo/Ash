import os
import time
import asyncio
import subprocess
from os import execvp
from Lena import app, SUDOERS
from sys import executable
from Lena.Database import startStage
from pyrogram import filters, Client
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import Message

async def restart(message: Message):
    if message:
        await startStage(message.chat.id, message.id)
    execvp(executable, [executable, "-m", "wbb"])

@app.on_message(filters.command("update") & SUDOERS)
async def updateRestart(app: Client, message: Message):
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date." in str(out):
            return await message.reply("**Branch Already Updated !**")
        await message.reply(f"`{out}`")
    except Exception as e:
        return await message.reply(str(e))
    message = await message.reply_text(
        "**Updated With Default Branch Restarting Now...**"
    )
    await restart(message)

@app.on_message(filters.command("restart") & SUDOERS)
async def restartBot(app: Client, message: Message):
    message = await message.reply(
        "**Restarting...**"
    )
    await restart(message)
