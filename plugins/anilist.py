import aiohttp


ANILIST_API_URL = "https://graphql.anilist.co"


ANIME_QUERY = """
query ($search: String) {
    Page(perPage: 10) {
        media(search: $search, type: ANIME) {
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
}
"""


async def search_anime(search: str) -> list[dict]:
    """Search anime on AniList."""

    if not search or not search.strip():
        return []

    variables = {
        "search": search.strip(),
    }

    timeout = aiohttp.ClientTimeout(total=15)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                ANILIST_API_URL,
                json={
                    "query": ANIME_QUERY,
                    "variables": variables,
                },
            ) as response:

                if response.status != 200:
                    return []

                result = await response.json()

    except (aiohttp.ClientError, aiohttp.ClientError):
        return []

    if "errors" in result:
        return []

    return result.get("data", {}).get("Page", {}).get("media", [])