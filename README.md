# django-channels-bug-repo

> test repo to demo possible django-channels-bug


## reproduction

```
poetry install

poetry run pytest mysite

# the test should error but the bug can be a bit flakey so you may need to run it twice.
```

```
❯ poetry run pytest mysite
======================================= test session starts ==============================================================================================
platform darwin -- Python 3.7.3, pytest-5.1.1, py-1.8.0, pluggy-0.12.0
Django settings: mysite.settings (from ini file)
rootdir: /Users/steve/Downloads/channels_tut, inifile: tox.ini
plugins: django-3.5.1, asyncio-0.10.0
collected 1 item

mysite/chat/test_consumers.py F                                                                                                                                                                          [100%]

FAILURES ===================================================================================================
test_consumer _________________________________________________________________________________________________

self = <channels.testing.websocket.WebsocketCommunicator object at 0x10a32dda0>, timeout = 1

    async def receive_output(self, timeout=1):
        """
        Receives a single message from the application, with optional timeout.
        """
        # Make sure there's not an exception to raise from the task
        if self.future.done():
            self.future.result()
        # Wait and receive the message
        try:
            async with async_timeout(timeout):
>               return await self.output_queue.get()

.venv/lib/python3.7/site-packages/asgiref/testing.py:75:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <Queue at 0x10a43e0f0 maxsize=0 tasks=1>

    async def get(self):
        """Remove and return an item from the queue.

        If queue is empty, wait until an item is available.
        """
        while self.empty():
            getter = self._loop.create_future()
            self._getters.append(getter)
            try:
>               await getter
E               concurrent.futures._base.CancelledError

/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/queues.py:159: CancelledError

During handling of the above exception, another exception occurred:

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

>       res = await communicator.receive_json_from()

mysite/chat/test_consumers.py:56:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
.venv/lib/python3.7/site-packages/channels/testing/websocket.py:93: in receive_json_from
    payload = await self.receive_from(timeout)
.venv/lib/python3.7/site-packages/channels/testing/websocket.py:72: in receive_from
    response = await self.receive_output(timeout)
.venv/lib/python3.7/site-packages/asgiref/testing.py:86: in receive_output
    raise e
.venv/lib/python3.7/site-packages/asgiref/testing.py:75: in receive_output
    return await self.output_queue.get()
.venv/lib/python3.7/site-packages/asgiref/timeout.py:68: in __aexit__
    self._do_exit(exc_type)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <asgiref.timeout.timeout object at 0x10a5c3e80>, exc_type = <class 'concurrent.futures._base.CancelledError'>

    def _do_exit(self, exc_type: Type[BaseException]) -> None:
        if exc_type is asyncio.CancelledError and self._cancelled:
            self._cancel_handler = None
            self._task = None
>           raise asyncio.TimeoutError
E           concurrent.futures._base.TimeoutError

.venv/lib/python3.7/site-packages/asgiref/timeout.py:105: TimeoutError
1 failed in 1.81s ===============================================================================================
Task was destroyed but it is pending!
task: <Task pending coro=<double_to_single_callable.<locals>.new_application() running at /Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/asgiref/compatibility.py:34> wait_for=<Future cancelled>>
Exception ignored in: <coroutine object double_to_single_callable.<locals>.new_application at 0x10a3057c8>
Traceback (most recent call last):
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/asgiref/compatibility.py", line 34, in new_application
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/sessions.py", line 183, in __call__
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/middleware.py", line 41, in coroutine_call
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/consumer.py", line 59, in __call__
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/utils.py", line 57, in await_many_dispatch
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/base_events.py", line 688, in call_soon
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/base_events.py", line 480, in _check_closed
RuntimeError: Event loop is closed
Task was destroyed but it is pending!
task: <Task pending coro=<Queue.get() running at /usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/queues.py:159> wait_for=<Future cancelled> cb=[_wait.<locals>._on_completion() at /usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/tasks.py:440]>
Task was destroyed but it is pending!
task: <Task pending coro=<double_to_single_callable.<locals>.new_application() running at /Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/asgiref/compatibility.py:34> wait_for=<Future cancelled>>
Exception ignored in: <coroutine object double_to_single_callable.<locals>.new_application at 0x10a3176c8>
Traceback (most recent call last):
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/asgiref/compatibility.py", line 34, in new_application
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/sessions.py", line 183, in __call__
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/middleware.py", line 41, in coroutine_call
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/consumer.py", line 59, in __call__
  File "/Users/steve/Downloads/channels_tut/.venv/lib/python3.7/site-packages/channels/utils.py", line 57, in await_many_dispatch
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/base_events.py", line 688, in call_soon
  File "/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/base_events.py", line 480, in _check_closed
RuntimeError: Event loop is closed
Task was destroyed but it is pending!
task: <Task pending coro=<Queue.get() running at /usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/queues.py:159> wait_for=<Future cancelled> cb=[_wait.<locals>._on_completion() at /usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/tasks.py:440]>
```
