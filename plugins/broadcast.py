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


@app.on_message(filters.command("broadcast"))
async def broadcast_command(
    _,
    message: Message,
):
    user = message.from_user

    if not user or not is_owner(user.id):
        await message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    if len(message.command) < 2:
        await message.reply_text(
            "Usage:\n"
            "<code>/broadcast Your message here</code>"
        )
        return

    text = message.text.split(
        " ",
        1,
    )[1].strip()

    if not text:
        await message.reply_text(
            "❌ Broadcast message cannot be empty."
        )
        return

    db = get_database()

    if db is None:
        await message.reply_text(
            "❌ MongoDB is not configured."
        )
        return

    users_collection = db["users"]

    users = await users_collection.find(
        {},
        {
            "_id": 0,
            "user_id": 1,
        },
    ).to_list(length=None)

    if not users:
        await message.reply_text(
            "❌ No users found."
        )
        return

    sent = 0
    failed = 0

    status_message = await message.reply_text(
        "📢 <b>Broadcast started...</b>"
    )

    for user_data in users:
        user_id = user_data.get("user_id")

        if not user_id:
            continue

        try:
            await app.send_message(
                chat_id=user_id,
                text=text,
            )
            sent += 1

        except Exception:
            failed += 1

    await status_message.edit_text(
        "<b>📢 Broadcast completed</b>\n\n"
        f"✅ Sent: <code>{sent}</code>\n"
        f"❌ Failed: <code>{failed}</code>"
    )