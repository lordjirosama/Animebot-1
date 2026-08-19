import time
from typing import Any, Optional


_CACHE: dict[str, tuple[float, Any]] = {}

DEFAULT_TTL = 600


def _cleanup() -> None:
    """Remove expired cache entries."""

    now = time.time()

    expired_keys = [
        key
        for key, (expires_at, _) in _CACHE.items()
        if expires_at <= now
    ]

    for key in expired_keys:
        _CACHE.pop(key, None)


def make_key(prefix: str, value: Any) -> str:
    """Create a normalized cache key."""

    normalized = str(value).strip().lower()
    return f"{prefix}:{normalized}"


def set_cache(
    key: str,
    value: Any,
    ttl: int = DEFAULT_TTL,
) -> None:
    """Store a value in cache."""

    if ttl <= 0:
        return

    _cleanup()

    _CACHE[key] = (
        time.time() + ttl,
        value,
    )


def get_cache(key: str) -> Optional[Any]:
    """Return cached value if it has not expired."""

    _cleanup()

    item = _CACHE.get(key)

    if item is None:
        return None

    expires_at, value = item

    if expires_at <= time.time():
        _CACHE.pop(key, None)
        return None

    return value


def delete_cache(key: str) -> None:
    """Delete one cached value."""

    _CACHE.pop(key, None)


def clear_cache() -> None:
    """Clear the complete cache."""

    _CACHE.clear()