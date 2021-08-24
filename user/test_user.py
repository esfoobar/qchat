import pytest
from quart import current_app

from user.models import *


def user_dict():
    return dict(username="testuser", password="test123")


@pytest.mark.asyncio
async def test_initial_response(
    create_test_client,
):
    response = await create_test_client.get("/register")
    body = await response.get_data()
    assert "Registration" in str(body)


@pytest.mark.asyncio
async def test_succesful_registration(create_test_client, create_test_app):
    response = await create_test_client.post(
        "/register", form=user_dict(), follow_redirects=True
    )
    body = await response.get_data()
    assert "You have been registered" in str(body)

    # check that the user was created on the database itself
    async with create_test_app.app_context():
        user_document = await current_app.dbc.user.find_one(
            {"username": user_dict()["username"]}
        )
        username = user_document["username"]
        assert username == user_dict()["username"]


@pytest.mark.asyncio
async def test_missing_fields_registration(create_test_client):
    # no fields
    response = await create_test_client.post(
        "/register", form={"username": "", "password": ""}
    )
    body = await response.get_data()
    assert "Please enter username and password" in str(body)

    # missing password
    response = await create_test_client.post(
        "/register", form={"username": "testuser", "password": ""}
    )
    body = await response.get_data()
    assert "Please enter username and password" in str(body)

    # missing username
    response = await create_test_client.post(
        "/register", form={"username": "", "password": "test123"}
    )
    body = await response.get_data()
    assert "Please enter username and password" in str(body)


@pytest.mark.asyncio
async def test_existing_user_registration(create_test_client):
    # no fields
    response = await create_test_client.post("/register", form=user_dict())
    body = await response.get_data()
    assert "Username already exists" in str(body)


@pytest.mark.asyncio
async def test_succesful_login(create_test_client):
    response = await create_test_client.post(
        "/login", form=user_dict(), follow_redirects=True
    )
    body = await response.get_data()
    assert f"@{user_dict()['username']}" in str(body)

    # Check that the session is being set
    async with create_test_client.session_transaction() as sess:
        assert sess["username"] == user_dict()["username"]


@pytest.mark.asyncio
async def test_login_logout_login(create_test_client):
    # loging
    response = await create_test_client.post(
        "/login", form=user_dict(), follow_redirects=True
    )
    body = await response.get_data()

    # logout
    response = await create_test_client.get("/logout", follow_redirects=True)

    # login again
    response = await create_test_client.post(
        "/login", form=user_dict(), follow_redirects=True
    )
    body = await response.get_data()
    assert f"@{user_dict()['username']}" in str(body)


@pytest.mark.asyncio
async def test_user_not_found_login(create_test_client):
    # no fields
    response = await create_test_client.post(
        "/login", form={"username": "testuser2", "password": "test123"}
    )
    body = await response.get_data()
    assert "User not found" in str(body)


@pytest.mark.asyncio
async def test_wrong_password_login(create_test_client):
    # no fields
    response = await create_test_client.post(
        "/login", form={"username": "testuser", "password": "wrong123"}
    )
    body = await response.get_data()
    assert "User not found" in str(body)


@pytest.mark.asyncio
async def test_profile_edit(create_test_client):
    # login
    response = await create_test_client.post(
        "/login", form=user_dict(), follow_redirects=True
    )

    # no fields entered
    response = await create_test_client.post(
        "/profile/edit", form={"username": ""}, follow_redirects=True
    )
    body = await response.get_data()
    assert "Please enter username" in str(body)

    # collision with testuser2
    test_user_2 = user_dict()
    test_user_2["username"] = "testuser2"
    await create_test_client.post("/register", form=test_user_2)

    # try editing with testuser2
    response = await create_test_client.post(
        "/profile/edit", form={"username": "testuser2"}, follow_redirects=True
    )
    body = await response.get_data()
    assert "Username already exists" in str(body)

    # succesful edit
    response = await create_test_client.post(
        "/profile/edit",
        form={"username": "testuser_edited"},
        follow_redirects=True,
    )
    body = await response.get_data()
    assert "Profile edited" in str(body)
    assert "@testuser_edited" in str(body)

    # check session was changed
    async with create_test_client.session_transaction() as sess:
        assert sess["username"] == "testuser_edited"

    # password edit
    response = await create_test_client.post(
        "/profile/edit",
        form={"username": user_dict()["username"], "password": "new_password"},
        follow_redirects=True,
    )
    body = await response.get_data()
    assert "Profile edited" in str(body)

    # logout
    response = await create_test_client.get("/logout", follow_redirects=True)
    body = await response.get_data()
    assert "Login" in str(body)

    # login with old password
    response = await create_test_client.post(
        "/login", form=user_dict(), follow_redirects=True
    )
    body = await response.get_data()
    assert "User not found" in str(body)

    # login with new password
    response = await create_test_client.post(
        "/login",
        form={"username": user_dict()["username"], "password": "new_password"},
        follow_redirects=True,
    )
    body = await response.get_data()
    assert f"@{user_dict()['username']}" in str(body) in str(body)
