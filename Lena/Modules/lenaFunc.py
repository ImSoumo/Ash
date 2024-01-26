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

@app.on_message(filters.command("restart") & SUDOERS)
async def restartBot(app: Client, message: Message):
    message = await message.reply(
        "**Restarting...**"
    )
    await restart(message)
