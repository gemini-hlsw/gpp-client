"""
A local GraphQL subscription server for offline tests.
"""

import json
from collections.abc import Callable

from websockets.asyncio.server import Server, serve


class SubscriptionServer:
    """
    A graphql-transport-ws server that answers each subscription with one event.

    The event's data is ``data`` itself, or ``data`` called with the
    subscribe payload.
    """

    def __init__(self, data: dict | Callable[[dict], dict]) -> None:
        self.data = data
        self.connections = 0
        self.subscribed: list[dict] = []

    async def _handle(self, websocket) -> None:
        self.connections += 1
        init = json.loads(await websocket.recv())
        assert init["type"] == "connection_init"
        await websocket.send(json.dumps({"type": "connection_ack"}))
        message = json.loads(await websocket.recv())
        assert message["type"] == "subscribe"
        self.subscribed.append(message["payload"])
        data = self.data(message["payload"]) if callable(self.data) else self.data
        await websocket.send(
            json.dumps({"id": message["id"], "type": "next", "payload": {"data": data}})
        )
        await websocket.send(json.dumps({"id": message["id"], "type": "complete"}))
        await websocket.wait_closed()

    def __call__(self):
        return serve(
            self._handle, "127.0.0.1", 0, subprotocols=["graphql-transport-ws"]
        )


def ws_url(server: Server) -> str:
    """
    Return the websocket URL a started server listens on.
    """
    host, port = server.sockets[0].getsockname()[:2]
    return f"ws://{host}:{port}/ws"
