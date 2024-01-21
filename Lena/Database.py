from Lena import db

restart = db.restart

async def startStage(chat_id: int, message_id: int):
    await restart.update_one(
        {"something": "something"},
        {
            "$set": {
                "chat_id": chat_id,
                "message_id": message_id,
            }
        },
        upsert=True,
    )

async def cleanStage() -> dict:
    data = await restart.find_one({"something": "something"})
    if not data:
        return {}
    await restart.delete_one({"something": "something"})
    return {
        "chat_id": data["chat_id"],
        "message_id": data["message_id"],
    }
