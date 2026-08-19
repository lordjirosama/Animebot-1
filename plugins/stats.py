from pyrogram import filters
from pyrogram.types import Message

from bot import app
from config import OWNER_ID
from database import get_database


def is_owner(user_id: int) -> bool:
    return bool(
        OWNER_ID
        and user_id == OWNER_ID
    )


@app.on_message(filters.command("stats"))
async def stats_command(
    _,
    message: Message,
):
    user = message.from_user

    if not user or not is_owner(user.id):
        await message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    db = get_database()

    if db is None:
        await message.reply_text(
            "❌ MongoDB is not configured."
        )
        return

    users_collection = db["users"]

    total_users = await users_collection.count_documents({})

    active_users = await users_collection.count_documents(
        {
            "is_active": True,
        }
    )

    await message.reply_text(
        "<b>📊 Bot Statistics</b>\n\n"
        f"👤 Total Users: <code>{total_users}</code>\n"
        f"🟢 Active Users: <code>{active_users}</code>\n\n"
        '🌐 <a href="https://t.me/Solurix_bots">'
        "Solurix Bots</a>"
    )