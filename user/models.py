from quart import current_app
from typing import Optional
import uuid
from passlib.hash import pbkdf2_sha256

from settings import IMAGES_URL


class User(object):
    def __init__(
        self, username: Optional[str] = None, password: Optional[str] = None
    ):
        self.id: str = ""  # set after record is written
        self.uid = ""
        self.username = username
        self.password = password
        self.image = ""
        self.images: dict = {}

    async def save(self):
        if self.uid == "":
            self.uid = str(uuid.uuid4())

        # check if this is a new password or password update
        original_user = await current_app.dbc.user.find_one(
            {"username": self.username}
        )
        if not original_user or original_user.password != self.password:
            self.password = pbkdf2_sha256.hash(self.password)

        # remove fields not used in collection
        del self.id

        # store on mongodb
        db_user = await current_app.dbc.user.insert_one(self.__dict__)

        # grab mongodb id
        self.id = str(db_user.inserted_id)

        return self

    @staticmethod
    async def login(username: str, password: str) -> Optional["User"]:
        user = await User().get_user_by_username(username=username)
        if not user:
            return None
        # check the password
        elif not pbkdf2_sha256.verify(password, user.password):
            return None
        return user

    async def get_user_by_username(self, username: str) -> Optional["User"]:
        user_document = await current_app.dbc.user.find_one(
            {"username": username}
        )
        if not user_document:
            return None
        else:
            self.uid = str(user_document["uid"])
            self.username = user_document["username"]
            self.password = user_document["password"]
            self.image = user_document["image"]
            self.images = {}

            image_dict = User._image_url_from_image_ts(self.uid, self.image)
            self.images["image_url_raw"] = image_dict["image_url_raw"]
            self.images["image_url_xlg"] = image_dict["image_url_xlg"]
            self.images["image_url_lg"] = image_dict["image_url_lg"]
            self.images["image_url_sm"] = image_dict["image_url_sm"]

            return self

    @staticmethod
    def _image_url_from_image_ts(user_uid: str, user_image: str) -> dict:
        # compute the image url
        image_dict: dict = {}
        if user_image:
            image_dict[
                "image_url_raw"
            ] = f"{IMAGES_URL}/user/{user_uid}.{user_image}.raw.png"
            image_dict[
                "image_url_xlg"
            ] = f"{IMAGES_URL}/user/{user_uid}.{user_image}.xlg.png"
            image_dict[
                "image_url_lg"
            ] = f"{IMAGES_URL}/user/{user_uid}.{user_image}.lg.png"
            image_dict[
                "image_url_sm"
            ] = f"{IMAGES_URL}/user/{user_uid}.{user_image}.sm.png"
        else:
            image_dict["image_url_raw"] = f"{IMAGES_URL}/user/profile.raw.png"
            image_dict["image_url_xlg"] = f"{IMAGES_URL}/user/profile.xlg.png"
            image_dict["image_url_lg"] = f"{IMAGES_URL}/user/profile.lg.png"
            image_dict["image_url_sm"] = f"{IMAGES_URL}/user/profile.sm.png"
        return image_dict
