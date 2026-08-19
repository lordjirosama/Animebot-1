from pyrogram import filters
from pyrogram.types import Message

from bot import app


START_TEXT = """
<b>🎌 Anime Info Bot</b>

Welcome to <b>Solurix Bots</b>! 👋

Your simple anime information assistant.

🔎 <b>Search Anime</b>
Send me any anime name and I'll find its information from AniList.

You can get:
• 🖼️ Anime Poster
• 📖 Synopsis
• 🎬 Episodes & Duration
• ⭐ Score
• 🎭 Genres
• 📺 Status & Season
• 👥 Characters

<b>Example:</b>
<code>Naruto</code>
<code>One Piece</code>
<code>Solo Leveling</code>

Powered by <a href="https://t.me/Solurix_bots">Solurix Bots</a> 🌐
"""


@app.on_message(filters.command("start"))
async def start_command(_, message: Message):
    await message.reply_text(
        START_TEXT,
        disable_web_page_preview=True,
    )