from typing import NoReturn
from quart import (
    Blueprint,
    render_template,
    session,
    current_app,
    websocket,
)
import uuid
import asyncio
import time
import json

from user.decorators import login_required
from user.models import User

chat_app = Blueprint("chat_app", __name__)


@chat_app.route("/")
@login_required
async def index() -> str:
    number_of_messages = 50
    dbc = current_app.dbc
    cursor_id = 0
    chat_messages = []
    chat_count = await dbc.chat.count_documents({})

    if chat_count < number_of_messages:
        skip = 0
    else:
        skip = chat_count - number_of_messages

    async for message in dbc.chat.find({}).skip(skip):
        message = await User().attach_profile_image(message)
        chat_messages.append(message)
        cursor_id = message["timestamp"]

    return await render_template(
        "index.html", chat_messages=chat_messages, cursor_id=cursor_id
    )


async def sending(dbc, session, cursor_id):
    while True:
        message = await dbc.chat.find_one({"timestamp": {"$gt": cursor_id}})
        if message:
            message = await User().attach_profile_image(message)
            message["_id"] = str(message["_id"])
            await websocket.send(json.dumps(message))
            cursor_id = message["timestamp"]
        await asyncio.sleep(1)


async def receiving(dbc, session):
    while True:
        data = await websocket.receive()
        message_document = {
            "uid": str(uuid.uuid4()),
            "username": session.get("username"),
            "body": data,
            "timestamp": int(time.time()),
        }
        await dbc.chat.insert_one(message_document)


@chat_app.websocket("/ws")
@login_required
async def ws():
    dbc = current_app.dbc
    cursor_id = int(websocket.args.get("cursor_id"))
    producer = asyncio.create_task(sending(dbc, session, cursor_id))
    consumer = asyncio.create_task(receiving(dbc, session))
    await asyncio.gather(producer, consumer)
