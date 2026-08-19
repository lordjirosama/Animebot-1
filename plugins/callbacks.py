from pyrogram import filters
from pyrogram.types import CallbackQuery

from bot import app


@app.on_callback_query(
    filters.regex(r"^back_to_search$")
)
async def back_to_search(_, query: CallbackQuery):
    await query.answer()

    await query.message.reply_text(
        "🔎 <b>Search Anime</b>\n\n"
        "Send me an anime name to search again.\n\n"
        "🌐 <a href=\"https://t.me/Solurix_bots\">"
        "Solurix Bots</a>",
        disable_web_page_preview=True,
    )