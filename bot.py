import asyncio
import importlib
import logging
import pkgutil

from pyrogram import Client

import plugins
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


def load_plugins():
    """Automatically load every Python module inside plugins/."""

    loaded = 0
    failed = 0

    for module_info in pkgutil.iter_modules(
        plugins.__path__
    ):
        module_name = module_info.name

        if module_name.startswith("_"):
            continue

        full_name = f"plugins.{module_name}"

        try:
            importlib.import_module(full_name)

            LOGGER.info(
                "Plugin loaded: %s",
                full_name,
            )

            loaded += 1

        except Exception:
            LOGGER.exception(
                "Failed to load plugin: %s",
                full_name,
            )

            failed += 1

    LOGGER.info(
        "Plugins loaded: %s | Failed: %s",
        loaded,
        failed,
    )

    if failed:
        LOGGER.warning(
            "Some plugins failed to load. "
            "Check the logs above."
        )


async def main():
    LOGGER.info("Starting Anime Info Bot...")

    # Connect to database
    await init_database()

    # Load all plugins before starting the client
    load_plugins()

    # Start Telegram client
    await app.start()

    me = await app.get_me()

    LOGGER.info(
        "Bot started successfully: @%s",
        me.username or "unknown",
    )

    try:
        await asyncio.Event().wait()

    finally:
        LOGGER.info("Stopping Anime Info Bot...")

        await app.stop()
        await close_database()


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        LOGGER.info("Bot stopped by user.")