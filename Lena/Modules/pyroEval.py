import io
from re import sub
import sys
import traceback
from typing import Union, List
from Lena import app, SUDOERS
from pyrogram.types import Message
from pyrogram.errors import RPCError
import subprocess
from datetime import datetime
from pyrogram import filters, enums

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

def commandpro(commands: Union[str, List[str]]):
    return filters.command(commands,"")


@app.on_message(filters.command("py") & filters.user(SUDOERS))
@app.on_edited_message(filters.command("py") & filters.user(SUDOERS))
async def eval(client, message: Message):
    if len(message.text.split()) < 2:
        return await message.reply_text("**ɪɴᴘᴜᴛ ɴᴏᴛ ғᴏᴜɴᴅ ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴏᴅᴇ ᴛᴏ ᴇxᴄᴜᴛᴇ ᴛʜɪs !**")
    
    cmd = message.text.split(maxsplit=1)[1]     
    status_message = await message.reply_text("**Processing...**")    
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "**Success**"
    end = datetime.now()
    ping = (end-start).microseconds / 1000
    final_output = "<b>ɪɴᴘᴜᴛ :</b>"
    final_output += f"<pre language='python'>{cmd}</pre>\n\n"
    final_output += "**ᴏᴜᴛᴘᴜᴛ :**\n"
    final_output += f"<code>{evaluation.strip()}</code> \n\n"
    final_output += f"<b>ᴛɪᴍᴇ ᴛᴀᴋᴇɴ :</b> <code>{ping}</code><b>ᴍs</b>"
    if len(final_output) > 9600000096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await status_message.edit_text(final_output)
