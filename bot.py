import asyncio
import logging

from pyrogram import Client

from config import API_HASH, API_ID, BOT_TOKEN
from database import close_database, init_database


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

LOGGER = logging.getLogger(__name__)


app = Client(
    "anime_info_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


async def main():
    LOGGER.info("Starting Anime Info Bot...")

    await init_database()

    await app.start()

    me = await app.get_me()
    LOGGER.info("Bot started successfully: @%s", me.username)

    try:
        await asyncio.Event().wait()
    finally:
        await app.stop()
        await close_database()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped.")