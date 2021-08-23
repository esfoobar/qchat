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
from .models import ChannelUser, Message

chat_app = Blueprint("chat_app", __name__)


@chat_app.route("/")
@login_required
async def index() -> str:
    number_of_messages = 50

    (chat_messages, cursor_id) = await Message.get_last_messages(
        number_of_messages
    )

    channel_users = await ChannelUser().get_channel_users()

    return await render_template(
        "chat/index.html",
        chat_messages=chat_messages,
        channel_users=channel_users,
        cursor_id=cursor_id,
    )


async def message_sending(dbc, session, cursor_id):
    while True:
        message = await Message.get_first_message_after_cursor(cursor_id)
        if message:
            await websocket.send(json.dumps(message.to_dict()))
            cursor_id = message.timestamp
        await asyncio.sleep(1)


async def message_receiving(dbc, session):
    while True:
        data = await websocket.receive()
        message_document = {
            "user_uid": session.get("user_uid"),
            "body": data,
        }
        await Message(**message_document).save()


@chat_app.websocket("/message-ws")
@login_required
async def message_ws():
    dbc = current_app.dbc
    cursor_id = int(websocket.args.get("cursor_id"))
    await ChannelUser(user_uid=session["user_uid"]).save()
    try:
        producer = asyncio.create_task(message_sending(dbc, session, cursor_id))
        consumer = asyncio.create_task(message_receiving(dbc, session))
        await asyncio.gather(producer, consumer)
    except asyncio.CancelledError:
        await ChannelUser(user_uid=session["user_uid"]).delete()
        raise


async def channel_updates(dbc):
    while True:
        channel_users = await ChannelUser().get_channel_users()
        if channel_users:
            await websocket.send(json.dumps({"users": channel_users}))
        await asyncio.sleep(10)


@chat_app.websocket("/channel-ws")
@login_required
async def channel_ws():
    dbc = current_app.dbc
    try:
        producer = asyncio.create_task(channel_updates(dbc))
        await asyncio.gather(producer)
    except asyncio.CancelledError:
        raise
