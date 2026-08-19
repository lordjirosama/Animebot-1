from pyrogram import filters
from pyrogram.types import CallbackQuery

from bot import app
from plugins.anilist import search_anime
from plugins.anime_parser import format_anime_info, parse_anime
from plugins.cache import get_cache, make_key, set_cache
from plugins.keyboards import anime_info_keyboard


@app.on_callback_query(
    filters.regex(r"^anime_info:(\d+)$")
)
async def anime_info_callback(_, query: CallbackQuery):
    anime_id = int(query.matches[0].group(1))

    await query.answer("🔎 Loading anime information...")

    cache_key = make_key("anime", anime_id)
    anime_data = get_cache(cache_key)

    if anime_data is None:
        # AniList search does not directly fetch by ID,
        # so we use a small GraphQL request below.
        import aiohttp

        graphql_query = """
        query ($id: Int) {
            Media(id: $id, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                description(asHtml: false)
                episodes
                duration
                status
                season
                seasonYear
                averageScore
                genres
                format
                coverImage {
                    extraLarge
                    large
                    medium
                }
                bannerImage
                siteUrl
            }
        }
        """

        try:
            timeout = aiohttp.ClientTimeout(total=15)

            async with aiohttp.ClientSession(
                timeout=timeout
            ) as session:

                async with session.post(
                    "https://graphql.anilist.co",
                    json={
                        "query": graphql_query,
                        "variables": {
                            "id": anime_id
                        },
                    },
                ) as response:

                    if response.status != 200:
                        await query.answer(
                            "❌ AniList request failed.",
                            show_alert=True,
                        )
                        return

                    result = await response.json()

        except aiohttp.ClientError:
            await query.answer(
                "❌ Unable to connect to AniList.",
                show_alert=True,
            )
            return

        anime_data = (
            result.get("data", {}).get("Media")
        )

        if not anime_data:
            await query.answer(
                "❌ Anime information not found.",
                show_alert=True,
            )
            return

        set_cache(
            cache_key,
            anime_data,
        )

    anime = parse_anime(anime_data)
    text = format_anime_info(anime)

    poster = anime.get("poster")

    keyboard = anime_info_keyboard(anime_id)

    try:
        if query.message.photo:
            await query.message.edit_caption(
                caption=text,
                reply_markup=keyboard,
            )
        else:
            if poster:
                await query.message.delete()

                await query.message.reply_photo(
                    photo=poster,
                    caption=text,
                    reply_markup=keyboard,
                )
            else:
                await query.message.edit_text(
                    text,
                    reply_markup=keyboard,
                )

    except Exception:
        try:
            await query.message.reply_text(
                text,
                reply_markup=keyboard,
            )
        except Exception:
            pass