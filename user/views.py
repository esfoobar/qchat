from quart import (
    Blueprint,
    current_app,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    current_app,
    abort,
)

import uuid
from typing import Union, TYPE_CHECKING
import os
from werkzeug.utils import secure_filename

if TYPE_CHECKING:
    from quart.wrappers.response import Response

from user.models import User
from user.decorators import login_required
from settings import UPLOAD_FOLDER
from utilities.imaging import thumbnail_process

user_app = Blueprint("user_app", __name__)


@user_app.route("/register", methods=["GET", "POST"])
async def register() -> Union[str, "Response"]:
    error: str = ""
    username: str = ""
    password: str = ""
    csrf_token: uuid.UUID = uuid.uuid4()

    if request.method == "GET":
        session["csrf_token"] = str(csrf_token)

    if request.method == "POST":
        form: dict = await request.form
        username = form.get("username", "")
        password = form.get("password", "")

        if not username or not password:
            error = "Please enter username and password"

        if (
            session.get("csrf_token") != form.get("csrf_token")
            and not current_app.testing
        ):
            error = "Invalid POST contents"

        # check if the user exists
        if not error:
            user = await User().get_user(username=username)
            if user and user.uid:
                error = "Username already exists"

        # register the user
        if not error:
            if not current_app.testing:
                del session["csrf_token"]

            # Save the user
            user = await User(
                username=username,
                password=password,
            ).save()

            await flash("You have been registered, please login")
            return redirect(url_for(".login"))
        else:
            session["csrf_token"] = str(csrf_token)

    return await render_template(
        "user/register.html",
        error=error,
        username=username,
        csrf_token=csrf_token,
    )


@user_app.route("/login", methods=["GET", "POST"])
async def login() -> Union[str, "Response"]:
    error: str = ""
    username: str = ""
    password: str = ""
    csrf_token: uuid.UUID = uuid.uuid4()

    if request.method == "GET":
        session["csrf_token"] = str(csrf_token)
        if request.args.get("next"):
            session["next"] = request.args.get("next")

    if request.method == "POST":
        form: dict = await request.form
        username = form.get("username", "")
        password = form.get("password", "")

        if not username or not password:
            error = "Please enter username and password"

        if (
            session.get("csrf_token") != form.get("csrf_token")
            and not current_app.testing
        ):
            error = "Invalid POST contents"

        # check if the user exists
        user = await User().login(username=username, password=password)
        if not user:
            error = "User not found"

        if user and not error:
            # login the user
            if not current_app.testing:
                del session["csrf_token"]

            session["user_uid"] = user.uid
            session["username"] = user.username

            if "next" in session:
                next = session["next"]
                session.pop("next")
                return redirect(next)
            else:
                return redirect(url_for("chat_app.index"))

        else:
            session["csrf_token"] = str(csrf_token)

    return await render_template(
        "user/login.html", error=error, username=username, csrf_token=csrf_token
    )


@user_app.route("/logout", methods=["GET"])
async def logout() -> "Response":
    del session["user_uid"]
    del session["username"]
    return redirect(url_for(".login"))


@user_app.route("/profile/edit", methods=["GET", "POST"])
@login_required
async def profile_edit() -> Union[str, "Response"]:
    error: str = ""
    csrf_token: uuid.UUID = uuid.uuid4()

    # grab the user's details
    profile_user = await User().get_user(username=session["username"])

    if request.method == "GET":
        session["csrf_token"] = str(csrf_token)

    if request.method == "POST":
        form: dict = await request.form
        form_username = form.get("username", "")
        form_password = form.get("password", "")

        if not form_username:
            error = "Please enter username"

        if (
            session.get("csrf_token") != form.get("csrf_token")
            and not current_app.testing
        ):
            error = "Invalid POST contents"

        # check if the username exists if username changed
        if not error and session["username"] != form_username:
            user = await User().get_user(username=form_username)

            if user and user.uid:
                error = "Username already exists"

        # update password
        if profile_user and not error and form_password:
            profile_user.password = form_password

        # image upload (skip if testing)
        changed_image: bool = False
        if profile_user and not current_app.testing:
            files = await request.files
            profile_image = files.get("profile_image")

            # if there's a profile_image, new file was uploaded
            if profile_image and profile_image.filename:
                filename = (
                    str(uuid.uuid4()) + "-" + secure_filename(profile_image.filename)
                )
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                await profile_image.save(file_path)
                image_uid = thumbnail_process(file_path, "user", str(profile_user.uid))
                changed_image = True

        # edit the profile
        if profile_user and not error:
            if not current_app.testing:
                del session["csrf_token"]

            profile_user.username = form_username

            if changed_image:
                profile_user.image = image_uid

            # update the user
            await profile_user.save()

            # update session with new username
            session["username"] = form_username

            # update session
            await flash("Profile edited")
            return redirect(url_for(".profile", username=profile_user.username))
        else:
            session["csrf_token"] = str(csrf_token)

    return await render_template(
        "user/profile_edit.html",
        error=error,
        profile_user=profile_user,
        csrf_token=csrf_token,
    )


@user_app.route("/user/<username>")
@login_required
async def profile(username) -> Union[str, "Response"]:
    # fetch the user
    user = await User().get_user(username=username)

    # user not found
    if not user:
        abort(404)

    return await render_template("user/profile.html", user=user)


@user_app.route("/user/list")
@login_required
async def user_list() -> Union[str, "Response"]:
    user_collection = current_app.dbc.user  # type: ignore

    async for user in user_collection.find({}):
        print(user)

    return "user list"
