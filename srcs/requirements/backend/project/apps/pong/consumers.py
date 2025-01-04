import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

# Set up a logger
logger = logging.getLogger('daphne')

class BallSimulator:
    def __init__(self, width=2, height=2):
        self.position = {"x": 50, "y": 50}
        self.velocity = {"x": 1, "y": 1}
        self.width = width
        self.height = height
        self.radius_x = self.width / 2
        self.radius_y = self.height / 2

    def update_ball(self):
        # Update position based on velocity
        self.position["x"] += self.velocity["x"]
        self.position["y"] += self.velocity["y"]

        logger.debug(f"self.radius_x {self.width}, self.radius_y {self.width}")
        self.radius_x = self.width / 2
        self.radius_y = self.height / 2
        logger.debug(f"self.radius_x {self.radius_x}, self.radius_y {self.radius_y}")

        # Right wall (considering the ball center and radius)
        if self.position["x"] - self.radius_x <= 0 or self.position["x"] + self.radius_x >= 100:
            logger.debug(f"self.position['x']: {self.position['x']}")
            logger.debug(f"self.position[x] + self.radius_x = {self.position['x'] + self.radius_x}")
            self.velocity["x"] *= -1  # Reverse the X velocity

        # Bottom wall (considering the ball center and radius)
        if self.position["y"] - self.radius_y <= 0 or self.position["y"] + self.radius_y >= 100:
            logger.debug(f"self.position['y']: {self.position['y']}")
            logger.debug(f"self.position[y] + self.radius_y = {self.position['y'] + self.radius_y}")
            self.velocity["y"] *= -1  # Reverse the Y velocity

        # Return updated position and velocity
        return {"position": self.position, "velocity": self.velocity}

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        self.ball_simulator = BallSimulator()
        await self.accept()
        logger.debug("> Pong WebSocket Connected")

        # Start sending updates every 0.1 second in the background
        asyncio.create_task(self.send_ball_updates())

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes.
        """
        logger.debug("> Pong WebSocket Disconnected")

    async def receive(self, text_data=None):
        """
        Called when the server receives data from the client.
        """
        logger.debug("> Pong WebSocket Data Received")
        logger.debug(f"text_data: {text_data}")
        try:
            data = json.loads(text_data)

            # Extract ball width and height from the received data
            width = data.get('width', 10)  # Default to 10 if not provided
            height = data.get('height', 10)  # Default to 10 if not provided
            logger.debug(f"Width: {width}, Height: {height}")

            # Update ball simulator dimensions if they are provided
            self.ball_simulator.width = width
            self.ball_simulator.height = height
            self.ball_simulator.radius_x = width / 2
            self.ball_simulator.radius_y = height / 2

            # Update the ball position and velocity
            updated_ball_state = self.ball_simulator.update_ball()

            # Send the updated ball state back to the client
            await self.send(text_data=json.dumps(updated_ball_state))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "error": "Invalid JSON"
            }))


    async def send_ball_updates(self):
        """
        Send updated ball position and velocity to the client every 0.1 seconds.
        """
        while True:
            updated_ball_state = self.ball_simulator.update_ball()
            await self.send(text_data=json.dumps(updated_ball_state))
            await asyncio.sleep(0.04)
