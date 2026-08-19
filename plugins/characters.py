import aiohttp

from pyrogram import filters
from pyrogram.types import CallbackQuery

from bot import app
from plugins.cache import get_cache, make_key, set_cache


ANILIST_API_URL = "https://graphql.anilist.co"


CHARACTERS_QUERY = """
query ($id: Int) {
    Media(id: $id, type: ANIME) {
        title {
            romaji
            english
        }
        characters(perPage: 10, sort: [ROLE, RELEVANCE]) {
            edges {
                role
                node {
                    name {
                        full
                        native
                    }
                    image {
                        large
                        medium
                    }
                }
            }
        }
    }
}
"""


def get_character_text(anime_title: str, characters: list[dict]) -> str:
    lines = [
        f"<b>👥 Characters — {anime_title}</b>",
        "",
    ]

    if not characters:
        lines.append("❌ No character information found.")
        return "\n".join(lines)

    for index, character in enumerate(characters, start=1):
        name = character.get("name", {}).get("full")

        if not name:
            continue

        role = character.get("role", "UNKNOWN")
        role = role.title()

        lines.append(
            f"<b>{index}. {name}</b> — {role}"
        )

    return "\n".join(lines)


@app.on_callback_query(
    filters.regex(r"^anime_chars:(\d+)$")
)
async def characters_callback(_, query: CallbackQuery):
    anime_id = int(query.matches[0].group(1))

    await query.answer("👥 Loading characters...")

    cache_key = make_key("characters", anime_id)
    cached = get_cache(cache_key)

    if cached is None:
        try:
            timeout = aiohttp.ClientTimeout(total=15)

            async with aiohttp.ClientSession(
                timeout=timeout
            ) as session:

                async with session.post(
                    ANILIST_API_URL,
                    json={
                        "query": CHARACTERS_QUERY,
                        "variables": {
                            "id": anime_id,
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

        if result.get("errors"):
            await query.answer(
                "❌ Unable to get character information.",
                show_alert=True,
            )
            return

        media = (
            result.get("data", {})
            .get("Media")
        )

        if not media:
            await query.answer(
                "❌ Anime not found.",
                show_alert=True,
            )
            return

        title_data = media.get("title") or {}

        anime_title = (
            title_data.get("english")
            or title_data.get("romaji")
            or "Unknown Anime"
        )

        characters = []

        for edge in (
            media.get("characters", {})
            .get("edges", [])
        ):
            node = edge.get("node") or {}

            characters.append(
                {
                    "role": edge.get("role", "UNKNOWN"),
                    "name": node.get("name") or {},
                    "image": node.get("image") or {},
                }
            )

        cached = {
            "title": anime_title,
            "characters": characters,
        }

        set_cache(
            cache_key,
            cached,
        )

    text = get_character_text(
        cached["title"],
        cached["characters"],
    )

    await query.message.reply_text(
        text,
        disable_web_page_preview=True,
    )