from quart import current_app

from settings import IMAGES_URL


class User:
    def __init__(self, username: str = None, password: str = None):
        self.uid = ""
        self.username = username
        self.password = password
        self.image = ""
        self.images: dict = {}

    @classmethod
    async def get_user_by_username(cls, username: str):
        user_document = await current_app.dbc.user.find_one(
            {"username": username}
        )
        if not user_document:
            return None
        else:
            cls.uid = str(user_document["uid"])
            cls.username = user_document["username"]
            cls.password = user_document["password"]
            cls.image = user_document["image"]
            cls.images = {}

            image_dict = cls._image_url_from_image_ts(cls.uid, cls.image)
            cls.images["image_url_raw"] = image_dict["image_url_raw"]
            cls.images["image_url_xlg"] = image_dict["image_url_xlg"]
            cls.images["image_url_lg"] = image_dict["image_url_lg"]
            cls.images["image_url_sm"] = image_dict["image_url_sm"]

            return cls

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

    @staticmethod
    async def attach_profile_image(message: dict) -> dict:
        return message
