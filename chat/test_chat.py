import pytest


def user_dict():
    return dict(username="testuser", password="test123")


@pytest.mark.asyncio
async def test_chat_page(
    create_test_client,
):
    # register user
    response = await create_test_client.post(
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
    async with create_test_client.websocket("/message-ws") as test_websocket:
        # login the user
        response = await create_test_client.post(
            "/login", form=user_dict(), follow_redirects=True
        )
        body = await response.get_data()

        # send data
        data = "Hello World!"
        await test_websocket.send(data)
        result = await test_websocket.receive()
        pass
