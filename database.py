from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URI, DATABASE_NAME


_client = None
_db = None


async def init_database():
    global _client, _db

    if not MONGO_URI:
        print("[INFO] MongoDB is disabled.")
        return

    _client = AsyncIOMotorClient(MONGO_URI)
    _db = _client[DATABASE_NAME]

    # Check MongoDB connection
    await _client.admin.command("ping")

    print("[INFO] MongoDB connected successfully.")


def get_database():
    return _db


async def close_database():
    global _client, _db

    if _client is not None:
        _client.close()

    _client = None
    _db = None

    print("[INFO] MongoDB connection closed.")