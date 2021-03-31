from typing import NoReturn
from quart import Blueprint, render_template, session, current_app, websocket, request
import uuid
import asyncio
import time

from user.decorators import login_required


home_app = Blueprint("home_app", __name__)


@home_app.route("/index2", methods=["GET"])
@login_required
async def init() -> str:
    return "Hello @" + session["username"]


@home_app.route("/")
@login_required
async def index() -> str:
    dbc = current_app.dbc
    cursor_id = 0
    chat_messages = []
    async for message in dbc.chat.find({}).sort("timestamp", 1).limit(10):
        chat_messages.append(message)
        cursor_id = message["timestamp"]
    return await render_template(
        "index.html", chat_messages=chat_messages, cursor_id=cursor_id
    )


async def sending(dbc, session, cursor_id):
    print("initial cursor_id:", cursor_id)
    while True:
        message = await dbc.chat.find_one({"timestamp": {"$gt": cursor_id}})
        if message:
            await websocket.send(f"@{message['username']} {message['body']}")
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


@home_app.websocket("/ws")
@login_required
async def ws():
    dbc = current_app.dbc
    cursor_id = int(websocket.args.get("cursor_id"))
    print("initial cursor_id:", cursor_id)
    producer = asyncio.create_task(sending(dbc, session, cursor_id))
    consumer = asyncio.create_task(receiving(dbc, session))
    await asyncio.gather(producer, consumer)
