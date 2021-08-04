from quart import current_app
from typing import Tuple
import uuid
import time

from user.models import User


class Message(object):
    def __init__(self, user: User, body: str):
        self.uid: str = str(uuid.uuid4())
        self.user: User = user
        self.body: str = body
        self.timestamp: int = int(time.time())

    async def get_last_messages(
        cls, number_of_messages: int = 50
    ) -> Tuple[list, int]:
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

        return (chat_messages, cursor_id)
