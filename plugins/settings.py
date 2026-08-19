from pyrogram import filters
from pyrogram.types import Message

from bot import app
from database import get_database


DEFAULT_SETTINGS = {
    "language": "en",
    "notifications": True,
}


async def get_user_settings(user_id: int) -> dict:
    db = get_database()

    if db is None:
        return DEFAULT_SETTINGS.copy()

    collection = db["user_settings"]

    settings = await collection.find_one(
        {
            "user_id": user_id,
        }
    )

    if not settings:
        settings = {
            "user_id": user_id,
            **DEFAULT_SETTINGS,
        }

        await collection.insert_one(settings)

    return {
        "language": settings.get(
            "language",
            "en",
        ),
        "notifications": settings.get(
            "notifications",
            True,
        ),
    }


async def update_user_setting(
    user_id: int,
    setting: str,
    value,
) -> bool:
    if setting not in DEFAULT_SETTINGS:
        return False

    db = get_database()

    if db is None:
        return False

    collection = db["user_settings"]

    await collection.update_one(
        {
            "user_id": user_id,
        },
        {
            "$set": {
                setting: value,
            }
        },
        upsert=True,
    )

    return True


@app.on_message(filters.command("settings"))
async def settings_command(
    _,
    message: Message,
):
    user = message.from_user

    if not user:
        return

    settings = await get_user_settings(
        user.id
    )

    notifications = (
        "Enabled"
        if settings["notifications"]
        else "Disabled"
    )

    await message.reply_text(
        "<b>⚙️ Your Settings</b>\n\n"
        f"🌐 Language: <code>{settings['language']}</code>\n"
        f"🔔 Notifications: <code>{notifications}</code>\n\n"
        "More settings will be available in future updates.\n\n"
        '<a href="https://t.me/Solurix_bots">'
        "Solurix Bots</a>",
        disable_web_page_preview=True,
    )