import pytest
from channels.testing import WebsocketCommunicator
from mysite.routing import application

from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth.models import User
from django.test.client import Client
from channels.db import database_sync_to_async
from chat.consumers import GROUP_NAME


@database_sync_to_async
def get_headers(name):
    user = User.objects.create_user(username=name)
    client = Client()
    client.force_login(user)
    scn = settings.SESSION_COOKIE_NAME
    return [(b'cookie', '{}={}'.format(scn, client.cookies[scn].value).encode())]


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_consumer():
    # 1. setup connections
    communicator = WebsocketCommunicator(application, "/ws/", headers=await get_headers(name="a"))
    connected, _ = await communicator.connect()
    assert connected

    comm_a = WebsocketCommunicator(application, "/ws/", headers=await get_headers(name="b"))
    connected, _ = await comm_a.connect()
    assert connected

    comm_b = WebsocketCommunicator(application, "/ws/", headers=await get_headers(name="c"))
    connected, _ = await comm_b.connect()
    assert connected

    # 3. subscribe to events
    subscribe = {"foo": "bar"}
    await communicator.send_json_to(subscribe)
    await comm_a.send_json_to(subscribe)
    await comm_b.send_json_to(subscribe)

    # 3. publish events
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        GROUP_NAME,
        {
            'type': 'broadcast_message',
        }
    )

    # 4. assert on received events
    expected_broadcast_msg = {"broadcast": "important update"}

    res = await communicator.receive_json_from()
    assert res == expected_broadcast_msg

    res = await comm_a.receive_json_from()
    assert res == expected_broadcast_msg

    res = await comm_b.receive_json_from()
    assert res == expected_broadcast_msg

    await communicator.disconnect()
    await comm_a.disconnect()
    await comm_b.disconnect()
