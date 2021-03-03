from quart import (
    Blueprint,
    render_template,
    request,
    session,
    make_response,
    current_app,
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


@home_app.route("/", methods=["GET"])
@login_required
async def init() -> str:
    return "Hello @" + session["username"]
