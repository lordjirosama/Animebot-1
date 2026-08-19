from pyrogram import filters
from pyrogram.types import Message

from bot import app


COMMANDS_TEXT = """
<b>🎌 Anime Info Bot</b>

<b>Available Commands</b>

🔹 /start — Start the bot
🔹 /help — Show help
🔹 /schedule — Upcoming anime episodes

<b>Search</b>

Just send an anime name directly.

<b>Example:</b>
<code>Naruto</code>
<code>One Piece</code>
<code>Solo Leveling</code>

🌐 <a href="https://t.me/Solurix_bots">Solurix Bots</a>
"""


@app.on_message(filters.command("help"))
async def help_command(_, message: Message):
    await message.reply_text(
        COMMANDS_TEXT,
        disable_web_page_preview=True,
    )