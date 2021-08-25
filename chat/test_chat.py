import pytest


def user_dict() -> dict:
    return dict(username="testuser", password="test123")


def chat_message() -> str:
    return "Hello World!"


@pytest.mark.asyncio
async def test_chat_page(
    create_test_client,
):
    # register user
    await create_test_client.post(
        "/register", form=user_dict(), follow_redirects=True
    )

    # login the user
    response = await create_test_client.post(
        "/login", form=user_dict(), follow_redirects=True
    )
    body = await response.get_data()
    assert "chat-message-input" in str(body)


@pytest.mark.asyncio
async def test_chat_send_message(
    create_test_client,
):
    # login the user
    await create_test_client.post(
        "/login", form=user_dict(), follow_redirects=True
    )

    # send a chat message
    async with create_test_client.websocket(
        "/message-ws?cursor_id=0"  # id=0 because it's the first ever message
    ) as test_websocket:
        # send data
        data = chat_message()
        await test_websocket.send(data)
        result = await test_websocket.receive()
        assert data in str(result)


@pytest.mark.asyncio
async def test_new_user_sees_previous_message(
    create_test_client,
):
    # register new user
    new_user_dict = user_dict()
    new_user_dict["username"] = "testuser2"
    await create_test_client.post(
        "/register", form=new_user_dict, follow_redirects=True
    )
    # login the user
    await create_test_client.post(
        "/login", form=new_user_dict, follow_redirects=True
    )

    # grab the cursor from content
    response = await create_test_client.get(
        "/",
    )
    body = await response.get_data()
    assert chat_message() in str(body)
