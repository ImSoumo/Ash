import asyncio
import os
from datetime import datetime, timedelta
from logging import getLogger
from typing import Union

import emoji
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    PeerIdInvalid,
    UserIsBlocked,
)
from pyrogram.types import Message

from Ash.AFK_db import is_cleanmode_on
from Ash import app, cleanmode

LOGGER = getLogger(__name__)
BANNED = {}

loop = asyncio.get_event_loop()


async def put_cleanmode(chat_id, message_id):
    if chat_id not in cleanmode:
        cleanmode[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=1),
    }
    cleanmode[chat_id].append(put)


async def auto_clean():
    while not await asyncio.sleep(30):
        try:
            for chat_id in cleanmode:
                if not await is_cleanmode_on(chat_id):
                    continue
                for x in cleanmode[chat_id]:
                    if datetime.now() <= x["timer_after"]:
                        continue
                    try:
                        await app.delete_messages(chat_id, x["msg_id"])
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except:
                        continue
        except:
            continue
