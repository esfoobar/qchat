import pytest
import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# This needs to go above the create_app import
load_dotenv(".quartenv")

from application import create_app

# We need our own module-level event_loop
# since pytest's is a function-level fixture
@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.fixture(scope="module")
async def create_db(event_loop):
    mongodb_db = os.environ["MONGODB_DB"] + "_test"
    mongodb_host = os.environ["MONGODB_HOST"]
    mongodb_port = int(os.environ["MONGODB_PORT"])

    # TESTING flag disables error catching during request handling,
    # so that you get better error reports when performing test requests
    # against the application.
    yield {
        "MONGODB_DB": mongodb_db,
        "TESTING": True,
    }

    client = AsyncIOMotorClient(f"mongodb://{mongodb_host}:{mongodb_port}")
    await client.drop_database(mongodb_db)


@pytest.fixture(scope="module")
async def create_test_app(create_db):
    app = create_app(**create_db)
    async with app.test_app():
        yield app


@pytest.fixture
def create_test_client(create_test_app):
    return create_test_app.test_client()
