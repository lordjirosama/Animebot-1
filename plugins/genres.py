import aiohttp

from pyrogram import filters
from pyrogram.types import CallbackQuery

from bot import app
from plugins.cache import get_cache, make_key, set_cache
from plugins.keyboards import anime_result_keyboard
from plugins.anime_parser import get_title


ANILIST_API_URL = "https://graphql.anilist.co"


GENRE_QUERY = """
query ($genre: String) {
    Page(perPage: 10) {
        media(
            genre: $genre
            type: ANIME
            sort: POPULARITY_DESC
        ) {
            id
            title {
                romaji
                english
                native
            }
            coverImage {
                large
                medium
            }
        }
    }
}
"""


async def get_anime_by_genre(genre: str) -> list[dict]:
    """Fetch popular anime from AniList by genre."""

    cache_key = make_key("genre", genre)
    cached = get_cache(cache_key)

    if cached is not None:
        return cached

    try:
        timeout = aiohttp.ClientTimeout(total=15)

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.post(
                ANILIST_API_URL,
                json={
                    "query": GENRE_QUERY,
                    "variables": {
                        "genre": genre,
                    },
                },
            ) as response:

                if response.status != 200:
                    return []

                result = await response.json()

    except aiohttp.ClientError:
        return []

    if result.get("errors"):
        return []

    results = (
        result.get("data", {})
        .get("Page", {})
        .get("media", [])
    )

    set_cache(cache_key, results)

    return results


@app.on_callback_query(
    filters.regex(r"^genre:(.+)$")
)
async def genre_callback(_, query: CallbackQuery):
    genre = query.matches[0].group(1).strip()

    await query.answer(
        f"🔎 Searching {genre} anime..."
    )

    results = await get_anime_by_genre(genre)

    if not results:
        await query.message.reply_text(
            f"❌ No anime found for genre: <b>{genre}</b>"
        )
        return

    await query.message.reply_text(
        f"<b>🎭 {genre} Anime</b>\n\n"
        f"Here are some popular anime in this genre:"
    )

    for anime in results[:10]:
        anime_id = anime.get("id")

        if not anime_id:
            continue

        title = get_title(
            anime.get("title") or {}
        )

        cover = anime.get("coverImage") or {}

        poster = (
            cover.get("large")
            or cover.get("medium")
        )

        text = (
            f"<b>🎌 {title}</b>\n\n"
            "Tap <b>Full Info</b> for complete details."
        )

        keyboard = anime_result_keyboard(anime_id)

        if poster:
            try:
                await query.message.reply_photo(
                    photo=poster,
                    caption=text,
                    reply_markup=keyboard,
                )
                continue
            except Exception:
                pass

        await query.message.reply_text(
            text,
            reply_markup=keyboard,
        )