import html
import re
from typing import Optional


def escape_html(text: Optional[str]) -> str:
    """Safely escape text before sending it as Telegram HTML."""
    if not text:
        return ""

    return html.escape(str(text), quote=False)


def clean_html(text: Optional[str]) -> str:
    """Remove HTML tags and normalize whitespace."""
    if not text:
        return ""

    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def truncate(text: str, limit: int = 500) -> str:
    """Limit text length without cutting unnecessarily."""
    if not text:
        return ""

    text = str(text).strip()

    if len(text) <= limit:
        return text

    return text[: limit - 3].rstrip() + "..."


def safe_int(value, default: int = 0) -> int:
    """Safely convert a value to integer."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default