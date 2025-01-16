import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import (Paddle,
                       Ball,
                       PADDLE_DEACCELERATION,
                       GAME_STATE_UPDATE_INTERVAL,
                       BALL_DEFAULT_WIDTH,
                       BALL_DEFAULT_HEIGHT,
                       PADDLE_DEFAULT_WIDTH,
                       PADDLE_DEFAULT_HEIGHT)
import logging

logger = logging.getLogger('pong.consumer')


class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ball = None
        self.paddle_left = None
        self.paddle_right = None
        self.dimensions_set = False
        self.game_update_task = None
        self.paddle_update_task = None

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        self.ball = Ball()
        self.paddle_left = Paddle()
        self.paddle_right = Paddle()
        await self.accept()
        logger.debug("> Pong WebSocket Connected")

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes.
        """
        if self.game_update_task:
            self.game_update_task.cancel()
        logger.debug("> Pong WebSocket Disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        """
        Called when the server receives data from the client.
        """
        try:
            data = json.loads(text_data)

            if data.get("type") == "init":
                # Handle ball dimensions (when sent by the client)
                ball_width = data.get('ballWidth', BALL_DEFAULT_WIDTH)
                ball_height = data.get('ballHeight', BALL_DEFAULT_HEIGHT)
                self.ball.width = ball_width
                self.ball.height = ball_height
                self.ball.update_radius()

                if not self.dimensions_set:
                    self.dimensions_set = True
                    try:
                        self.game_update_task = asyncio.create_task(self.game_update_loop())
                        logger.debug("✅ Game update loop started successfully")
                    except Exception as e:
                        logger.error(f"❌ Failed to start game_update_loop: {e}")

            if data.get("type") == "restart":
                # Cancel the current game update task
                if self.game_update_task:
                    self.game_update_task.cancel()
                await asyncio.sleep(0.2)

                self.ball.reset()
                self.paddle_left.reset()
                self.paddle_right.reset()

                try:
                    self.game_update_task = asyncio.create_task(self.game_update_loop())
                    logger.debug("✅ Game update loop restarted after reset")
                except Exception as e:
                    logger.error(f"❌ Failed to restart game_update_loop: {e}")

            if data.get("type") == "paddle":
                direction = data.get("direction", 0)
                side = data.get("side")

                if side and side == "left":
                    self.paddle_left.set_direction(direction)
                    logger.debug(f"⬅️ Left paddle direction set: {direction}")
                elif side and side == "right":
                    self.paddle_right.set_direction(direction)
                    logger.debug(f"➡️ Right paddle direction set: {direction}")

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))

    async def game_update_loop(self):
        """
        Main game loop for sending ball and paddle updates to the client.
        """
        try:
            while True:
                self.paddle_left.update_position()
                self.paddle_right.update_position()

                # Build payload with ball and paddle states
                payload = {
                    "ball": self.ball.update_ball(self.paddle_left, self.paddle_right),
                    "paddles": {
                        "left": {
                            "width": self.paddle_left.width,
                            "height": self.paddle_left.height,
                            "y": self.paddle_left.position,
                            "speed": self.paddle_left.speed,
                            "deacceleration": PADDLE_DEACCELERATION,
                        },
                        "right": {
                            "width": self.paddle_right.width,
                            "height": self.paddle_right.height,
                            "y": self.paddle_right.position,
                            "speed": self.paddle_right.speed,
                            "deacceleration": PADDLE_DEACCELERATION,
                        },
                    }
                }

                await self.send(text_data=json.dumps(payload))
                await asyncio.sleep(GAME_STATE_UPDATE_INTERVAL)

        except asyncio.CancelledError:
            logger.info("🛑 Game update loop cancelled.")
        except Exception as e:
            logger.error(f"❌ Error in game update loop: {e}")
