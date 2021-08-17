from quart import current_app
from typing import Any, Tuple, Optional
import uuid
import time
from typing import Any, List, Optional

from user.models import User


class Message(object):
    def __init__(
        self, user_uid: Optional[str] = None, body: Optional[str] = None
    ):
        self.id: str = ""  # set after record is written
        self.uid: str = ""
        self.user_uid: str = user_uid
        self.user: Any = None  # User object
        self.body = body
        self.timestamp: int = 0

    async def save(self) -> "Message":
        if self.uid == "":
            self.uid = str(uuid.uuid4())

        if self.timestamp == 0:
            self.timestamp = int(time.time())

        # remove fields not used in collection
        del self.id
        del self.user

        # store on mongodb
        db_message = await current_app.dbc.chat.insert_one(self.__dict__)

        # reload properties
        self.id = str(db_message.inserted_id)
        self.user = await User().get_user(user_uid=self.user_uid)

        return self

    @classmethod
    async def get_last_messages(
        cls, number_of_messages: int = 50
    ) -> Tuple[List["Message"], int]:
        cursor_id = 0
        chat_messages = []

        chat_count = await current_app.dbc.chat.count_documents({})

        if chat_count < number_of_messages:
            skip = 0
        else:
            skip = chat_count - number_of_messages

        async for db_message in current_app.dbc.chat.find({}).skip(skip):
            message = await Message.dict_to_class(db_message)
            chat_messages.append(message)
            cursor_id = message.timestamp

        return (chat_messages, cursor_id)

    @classmethod
    async def get_first_message_after_cursor(
        cls, cursor_id: int
    ) -> Optional["Message"]:
        db_message = await current_app.dbc.chat.find_one(
            {"timestamp": {"$gt": cursor_id}}
        )
        if db_message:
            return await Message.dict_to_class(db_message)
        else:
            return None

    @staticmethod
    async def dict_to_class(db_message: dict) -> "Message":
        message = Message()
        message.id = str(db_message["_id"])
        message.uid = db_message["uid"]
        message.user_uid = db_message["user_uid"]
        message.user = await User().get_user(user_uid=db_message["user_uid"])
        message.body = db_message["body"]
        message.timestamp = db_message["timestamp"]
        return message

    def to_dict(self) -> dict:
        # convert user to dict
        self.user = self.user.__dict__
        return self.__dict__
