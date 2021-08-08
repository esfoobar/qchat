from quart import (
    Blueprint,
    render_template,
    session,
    current_app,
    websocket,
)
import asyncio
import json

from user.decorators import login_required
from user.models import User
from .models import Message

chat_app = Blueprint("chat_app", __name__)


@chat_app.route("/")
@login_required
async def index() -> str:
    number_of_messages = 50

    (chat_messages, cursor_id) = await Message.get_last_messages(
        number_of_messages
    )

    return await render_template(
        "chat/index.html", chat_messages=chat_messages, cursor_id=cursor_id
    )


async def sending(dbc, session, cursor_id):
    while True:
        message = await Message.get_first_message_after_cursor(cursor_id)
        if message:
            # convert user to dict
            message.user = message.user.__dict__
            await websocket.send(json.dumps(message.__dict__))
            cursor_id = message.timestamp
        await asyncio.sleep(1)


async def receiving(dbc, session):
    while True:
        data = await websocket.receive()
        message_document = {
            "username": session.get("username"),
            "body": data,
        }
        await Message(**message_document).save()


@chat_app.websocket("/ws")
@login_required
async def ws():
    dbc = current_app.dbc
    cursor_id = int(websocket.args.get("cursor_id"))
    producer = asyncio.create_task(sending(dbc, session, cursor_id))
    consumer = asyncio.create_task(receiving(dbc, session))
    await asyncio.gather(producer, consumer)
