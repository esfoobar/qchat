from motor.motor_asyncio import AsyncIOMotorClient
from quart import current_app


async def db_connection():
    mongodb_db = current_app.config["MONGODB_DB"]
    mongodb_host = current_app.config["MONGODB_HOST"]
    mongodb_port = int(current_app.config["MONGODB_PORT"])
    client = AsyncIOMotorClient(f"mongodb://{mongodb_host}:{mongodb_port}")
    database = client[mongodb_db]
    return database
