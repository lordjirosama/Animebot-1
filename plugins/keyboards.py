from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def anime_result_keyboard(anilist_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📖 Full Info",
                    callback_data=f"anime_info:{anilist_id}",
                ),
                InlineKeyboardButton(
                    "👥 Characters",
                    callback_data=f"anime_chars:{anilist_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔗 AniList",
                    url=f"https://anilist.co/anime/{anilist_id}",
                )
            ],
        ]
    )


def anime_info_keyboard(anilist_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👥 Characters",
                    callback_data=f"anime_chars:{anilist_id}",
                ),
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data=f"anime_info:{anilist_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔗 Open AniList",
                    url=f"https://anilist.co/anime/{anilist_id}",
                )
            ],
        ]
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="back_to_search",
                )
            ]
        ]
    )