from quart import current_app
from typing import Any, Tuple, Optional
import uuid
import time
from bson.objectid import ObjectId
from typing import Union, Any, List, Type
from collections import namedtuple

from user.models import User


class Message(object):
    def __init__(
        self, username: Optional[str] = None, body: Optional[str] = None
    ):
        self.id: str  # set after record is written
        self.uid: str
        self.username = username
        self.user: Any
        self.body = body
        self.timestamp: int

    def save(self):
        if not self.uid:
            self.uid = str(uuid.uuid4())

        if not self.timestamp:
            self.timestamp = int(time.time())

        # store on mongodb
        pass

    @classmethod
    async def get_last_messages(
        cls, number_of_messages: int = 50
    ) -> Tuple[List["Message"], int]:
        dbc = current_app.dbc
        cursor_id = 0
        chat_messages = []
        chat_count = await dbc.chat.count_documents({})

        if chat_count < number_of_messages:
            skip = 0
        else:
            skip = chat_count - number_of_messages

        async for db_message in dbc.chat.find({}).skip(skip):
            message = await dict_to_class(db_message)
            chat_messages.append(message)
            cursor_id = message.timestamp

        return (chat_messages, cursor_id)


async def dict_to_class(db_message: dict) -> "Message":
    message = Message()
    message.id = str(db_message["_id"])
    message.uid = db_message["uid"]
    message.username = db_message["username"]
    message.user = await User().get_user_by_username(
        username=db_message["username"]
    )
    message.body = db_message["body"]
    message.timestamp = db_message["timestamp"]
    return message
