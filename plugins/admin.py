from pyrogram import filters
from pyrogram.types import Message

from bot import app
from config import OWNER_ID


def is_owner(user_id: int) -> bool:
    return bool(
        OWNER_ID
        and user_id == OWNER_ID
    )


@app.on_message(
    filters.command("admin")
)
async def admin_command(
    _,
    message: Message,
):
    user = message.from_user

    if not user or not is_owner(user.id):
        await message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    await message.reply_text(
        "<b>👑 Admin Panel</b>\n\n"
        "Welcome, Owner.\n\n"
        "Admin features will be added here."
    )