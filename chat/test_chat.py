import pytest


def user_dict():
    return dict(username="testuser", password="test123")


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
        data = "Hello World!"
        await test_websocket.send(data)
        result = await test_websocket.receive()
        assert data in str(result)
