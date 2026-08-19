from pyrogram import filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot import app
from plugins.anilist import search_anime
from plugins.anime_parser import get_title


@app.on_inline_query()
async def inline_anime_search(_, inline_query: InlineQuery):
    query = (inline_query.query or "").strip()

    if len(query) < 2:
        await inline_query.answer(
            results=[],
            cache_time=1,
            switch_pm_text="Search for an anime",
            switch_pm_parameter="start",
        )
        return

    results = await search_anime(query)

    inline_results = []

    for anime in results[:10]:
        anime_id = anime.get("id")

        if not anime_id:
            continue

        title = get_title(
            anime.get("title") or {}
        )

        description = (
            anime.get("description")
            or "No description available."
        )

        description = (
            description
            .replace("<br>", " ")
            .replace("\n", " ")
        )

        if len(description) > 150:
            description = description[:147] + "..."

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔗 Open AniList",
                        url=(
                            f"https://anilist.co/anime/"
                            f"{anime_id}"
                        ),
                    )
                ]
            ]
        )

        text = (
            f"<b>🎌 {title}</b>\n\n"
            f"{description}\n\n"
            "🌐 <a href=\"https://t.me/Solurix_bots\">"
            "Solurix Bots</a>"
        )

        inline_results.append(
            InlineQueryResultArticle(
                id=str(anime_id),
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    text
                ),
                reply_markup=keyboard,
            )
        )

    await inline_query.answer(
        results=inline_results,
        cache_time=30,
        is_personal=True,
    )