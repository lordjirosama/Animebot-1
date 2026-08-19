from utils import clean_html, truncate


def get_title(title: dict) -> str:
    """Return the best available anime title."""

    if not title:
        return "Unknown Title"

    return (
        title.get("english")
        or title.get("romaji")
        or title.get("native")
        or "Unknown Title"
    )


def parse_anime(anime: dict) -> dict:
    """Convert AniList anime data into a clean structure."""

    title_data = anime.get("title") or {}
    cover_data = anime.get("coverImage") or {}

    description = clean_html(anime.get("description"))

    return {
        "id": anime.get("id"),
        "title": get_title(title_data),
        "romaji_title": title_data.get("romaji"),
        "english_title": title_data.get("english"),
        "native_title": title_data.get("native"),
        "description": truncate(description, 1000),
        "episodes": anime.get("episodes"),
        "duration": anime.get("duration"),
        "status": anime.get("status"),
        "season": anime.get("season"),
        "season_year": anime.get("seasonYear"),
        "score": anime.get("averageScore"),
        "genres": anime.get("genres") or [],
        "format": anime.get("format"),
        "poster": (
            cover_data.get("extraLarge")
            or cover_data.get("large")
            or cover_data.get("medium")
        ),
        "banner": anime.get("bannerImage"),
        "url": anime.get("siteUrl"),
    }


def format_anime_info(anime: dict) -> str:
    """Create a Telegram-friendly anime information message."""

    title = anime.get("title") or "Unknown Title"
    description = anime.get("description") or "No description available."

    genres = anime.get("genres") or []
    genre_text = ", ".join(genres) if genres else "N/A"

    score = anime.get("score")
    score_text = f"{score}/100" if score is not None else "N/A"

    episodes = anime.get("episodes")
    episodes_text = str(episodes) if episodes is not None else "N/A"

    duration = anime.get("duration")
    duration_text = f"{duration} min/episode" if duration else "N/A"

    status = anime.get("status") or "N/A"
    anime_format = anime.get("format") or "N/A"

    season = anime.get("season")
    year = anime.get("season_year")

    if season and year:
        season_text = f"{season.title()} {year}"
    elif year:
        season_text = str(year)
    else:
        season_text = "N/A"

    return (
        f"<b>{title}</b>\n\n"
        f"<b>Format:</b> {anime_format}\n"
        f"<b>Status:</b> {status}\n"
        f"<b>Episodes:</b> {episodes_text}\n"
        f"<b>Duration:</b> {duration_text}\n"
        f"<b>Season:</b> {season_text}\n"
        f"<b>Score:</b> {score_text}\n"
        f"<b>Genres:</b> {genre_text}\n\n"
        f"<b>Synopsis:</b>\n{description}"
    )