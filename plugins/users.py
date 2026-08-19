from datetime import datetime, timezone

from pyrogram import filters
from pyrogram.types import Message

from bot import app
from database import get_database


def get_user_data(message: Message) -> dict | None:
    user = message.from_user

    if not user:
        return None

    return {
        "user_id": user.id,
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "username": user.username or "",
        "is_active": True,
        "updated_at": datetime.now(timezone.utc),
    }


async def register_user(message: Message) -> None:
    data = get_user_data(message)

    if not data:
        return

    db = get_database()

    if db is None:
        return

    users_collection = db["users"]

    await users_collection.update_one(
        {
            "user_id": data["user_id"],
        },
        {
            "$set": data,
            "$setOnInsert": {
                "created_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )


@app.on_message(
    filters.private
    & ~filters.service
)
async def track_user(_, message: Message):
    await register_user(message)