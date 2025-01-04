import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        await self.accept()
        print("Pong WebSocket Connected")

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes.
        """
        print("Pong WebSocket Disconnected")

    async def receive(self, text_data):
        """
        Called when the server receives data from the client.
        """
        try:
            data = json.loads(text_data)
            print("Received data from client:", data)

            # Echo the JSON data back to the client
            await self.send(text_data=json.dumps({
                "position": data.get("position", {"x": 0, "y": 0}),
                "velocity": data.get("velocity", {"x": 0, "y": 0})
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "error": "Invalid JSON"
            }))
