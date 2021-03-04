from quart import (
    Blueprint,
    render_template,
    request,
    session,
    make_response,
    current_app,
    websocket,
)
from typing import Union, TYPE_CHECKING
import uuid
import asyncio
import arrow
import json
import logging

from user.decorators import login_required

# from post.models import (
#     get_post_parent_uid,
#     get_last_feed_id,
#     ActionType,
#     get_latest_posts,
#     get_post_comments,
#     get_post_likes,
#     get_post_uid_from_id,
# )
# from user.models import user_table, image_url_from_image_ts

if TYPE_CHECKING:
    from quart.wrappers.response import Response


home_app = Blueprint("home_app", __name__)


@home_app.route("/index2", methods=["GET"])
@login_required
async def init() -> str:
    return "Hello @" + session["username"]


@home_app.route("/")
async def index():
    return await render_template("index.html")


async def sending(dbc, session):
    while True:
        await asyncio.sleep(10)
        message = await dbc.chat.find_one({})
        print(message, session["username"])
        if message:
            await websocket.send(f"echo {message['body']}")
            await dbc.chat.delete_one({"uid": message["uid"]})


async def receiving(dbc, session):
    while True:
        data = await websocket.receive()
        message_document = {"body": data, "uid": str(uuid.uuid4())}
        await dbc.chat.insert_one(message_document)


@home_app.websocket("/ws")
async def ws():
    dbc = current_app.dbc
    producer = asyncio.create_task(sending(dbc, session))
    consumer = asyncio.create_task(receiving(dbc, session))
    await asyncio.gather(producer, consumer)
