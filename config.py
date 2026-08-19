import os

from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default=None, required: bool = False):
    value = os.getenv(name, default)

    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


BOT_TOKEN = get_env("BOT_TOKEN", required=True)

API_ID = int(get_env("API_ID", "0"))
API_HASH = get_env("API_HASH", "")

MONGO_URI = get_env("MONGO_URI", "")
DATABASE_NAME = get_env("DATABASE_NAME", "anime_info_bot")

OWNER_ID = int(get_env("OWNER_ID", "0"))

# AniList public API
ANILIST_API_URL = "https://graphql.anilist.co"