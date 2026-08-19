from pyrogram import filters
from pyrogram.types import Message

from bot import app
from plugins.anilist import search_anime
from plugins.cache import get_cache, make_key, set_cache
from plugins.keyboards import anime_result_keyboard
from plugins.anime_parser import get_title


@app.on_message(
    filters.text
    & ~filters.command(
        [
            "start",
        ]
    )
)
async def anime_search(_, message: Message):
    query = (message.text or "").strip()

    if not query:
        return

    if len(query) < 2:
        await message.reply_text(
            "❌ Please enter at least 2 characters."
        )
        return

    if len(query) > 100:
        await message.reply_text(
            "❌ Search query is too long."
        )
        return

    searching_message = await message.reply_text(
        "🔎 <b>Searching AniList...</b>"
    )

    cache_key = make_key("search", query)
    results = get_cache(cache_key)

    if results is None:
        results = await search_anime(query)
        set_cache(cache_key, results)

    if not results:
        await searching_message.edit_text(
            "❌ <b>No anime found.</b>\n\n"
            "Try another anime name."
        )
        return

    await searching_message.delete()

    for anime in results[:10]:
        anime_id = anime.get("id")

        if not anime_id:
            continue

        title = get_title(anime.get("title") or {})

        cover_image = anime.get("coverImage") or {}
        poster = (
            cover_image.get("large")
            or cover_image.get("medium")
        )

        text = f"<b>🎌 {title}</b>\n\n"
        text += "Tap <b>Full Info</b> to see complete information."

        keyboard = anime_result_keyboard(anime_id)

        if poster:
            try:
                await message.reply_photo(
                    photo=poster,
                    caption=text,
                    reply_markup=keyboard,
                )
                continue
            except Exception:
                pass

        await message.reply_text(
            text,
            reply_markup=keyboard,
        )