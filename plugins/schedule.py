import aiohttp
from datetime import datetime, timezone

from pyrogram import filters
from pyrogram.types import Message

from bot import app
from plugins.cache import get_cache, set_cache


ANILIST_API_URL = "https://graphql.anilist.co"


SCHEDULE_QUERY = """
query {
    Page(perPage: 15) {
        airingSchedules(
            airingAt_greater: 0
            sort: TIME
        ) {
            airingAt
            episode
            media {
                id
                title {
                    romaji
                    english
                }
            }
        }
    }
}
"""


def format_timestamp(timestamp: int) -> str:
    """Convert AniList timestamp to a readable UTC time."""

    try:
        date = datetime.fromtimestamp(
            timestamp,
            tz=timezone.utc,
        )

        return date.strftime(
            "%d %b %Y, %H:%M UTC"
        )

    except (TypeError, ValueError, OSError):
        return "Unknown time"


async def get_schedule() -> list[dict]:
    """Fetch upcoming anime episodes from AniList."""

    cache_key = "airing_schedule"

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
                    "query": SCHEDULE_QUERY,
                },
            ) as response:

                if response.status != 200:
                    return []

                result = await response.json()

    except aiohttp.ClientError:
        return []

    if result.get("errors"):
        return []

    schedules = (
        result.get("data", {})
        .get("Page", {})
        .get("airingSchedules", [])
    )

    set_cache(
        cache_key,
        schedules,
        ttl=300,
    )

    return schedules


@app.on_message(filters.command("schedule"))
async def schedule_command(
    _,
    message: Message,
):
    schedules = await get_schedule()

    if not schedules:
        await message.reply_text(
            "❌ Unable to fetch the anime schedule right now."
        )
        return

    lines = [
        "<b>📅 Upcoming Anime Episodes</b>",
        "",
    ]

    for item in schedules[:15]:
        media = item.get("media") or {}
        title_data = media.get("title") or {}

        title = (
            title_data.get("english")
            or title_data.get("romaji")
            or "Unknown Anime"
        )

        episode = item.get("episode")
        airing_at = item.get("airingAt")

        if episode:
            episode_text = f"Episode {episode}"
        else:
            episode_text = "Episode ?"

        time_text = format_timestamp(airing_at)

        lines.append(
            f"🎌 <b>{title}</b>\n"
            f"   🎬 {episode_text}\n"
            f"   🕐 {time_text}\n"
        )

    lines.append(
        "🌐 Powered by "
        '<a href="https://t.me/Solurix_bots">Solurix Bots</a>'
    )

    await message.reply_text(
        "\n".join(lines),
        disable_web_page_preview=True,
    )