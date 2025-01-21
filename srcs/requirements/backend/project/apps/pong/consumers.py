import json
import struct
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import (GameState,
                       Ball,
                       Paddle,
                       GAME_STATUS_IN_PROGRESS,
                       GAME_STATUS_ENDED,
                       PADDLE_DEACCELERATION,
                       GAME_STATE_UPDATE_INTERVAL,
                       BALL_DEFAULT_WIDTH,
                       BALL_DEFAULT_HEIGHT)
import logging

logger = logging.getLogger('pong.consumer')


class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = None
        self.ball = None
        self.paddle_left = None
        self.paddle_right = None
        self.are_dimensions_set = False
        self.game_update_task = None
        self.paddle_update_task = None

    async def connect(self):
        self.game_state = GameState()
        self.ball = Ball()
        self.paddle_left = Paddle()
        self.paddle_right = Paddle()
        await self.accept()
        logger.debug("Pong WebSocket Connected")

    async def disconnect(self, close_code):
        if self.game_update_task:
            self.game_update_task.cancel()
        logger.debug("Pong WebSocket Disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "update_dimensions":
                await self.handle_update_dimensions(data)

            elif action == "start":
                await self.handle_start()

            elif action == "restart":
                await self.handle_start()

            elif action == "stop":
                await self.handle_stop()

            elif action == "update_paddle":
                await self.handle_paddle(data)

            else:
                await self.send(text_data=json.dumps({"error": "Unknown action"}))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))

    async def handle_update_dimensions(self, data):
        logger.debug(f"Updating dimensions... { data }")

        self.ball.width = data.get('ball_width', BALL_DEFAULT_WIDTH)
        self.ball.height = data.get('ball_height', BALL_DEFAULT_HEIGHT)
        self.ball.update_radius()

        if not self.are_dimensions_set:
            self.are_dimensions_set = True
            logger.debug("Dimensions set successfully")
            await self.send_game_state("Dimensions initialized")

    async def handle_start(self):
        if self.game_update_task:
            self.game_update_task.cancel()
            await self.set_game_status(GAME_STATUS_ENDED)

        try:
            self.game_update_task = asyncio.create_task(self.game_update_loop())
            await self.set_game_status(GAME_STATUS_IN_PROGRESS)
            logger.debug("✅ Game update loop restarted after reset")
        except Exception as e:
            logger.error(f"❌ Failed to restart game_update_loop: {e}")

    async def handle_paddle(self, data):
        direction = data.get("direction", 0)
        side = data.get("side")

        if side == "left":
            self.paddle_left.set_direction(direction)
            logger.debug(f"⬅️ Left paddle direction set: {direction}")
        elif side == "right":
            self.paddle_right.set_direction(direction)
            logger.debug(f"➡️ Right paddle direction set: {direction}")

    async def handle_stop(self):
        if self.game_update_task:
            self.game_update_task.cancel()
        await self.set_game_status(GAME_STATUS_ENDED)

    async def set_game_status(self, status):
        self.game_state.status = status
        logger.debug(f"Game state updated to {status}")
        await self.send_game_state(f"Game status updated to {status}")

    async def send_game_state(self, message):
        payload = struct.pack(
            '<B i i',
            1,  # message_type
            self.game_state.status,
            self.game_state.countdown_value,
            # self.game_state.score.left,
            # self.game_state.score.right,
            # self.game_state.tie_breaker
        )

        await self.send(bytes_data=payload)

    async def game_update_loop(self):
        try:
            while True:
                self.paddle_left.update_position()
                self.paddle_right.update_position()
                updated_ball = await self.ball.update_ball(self.paddle_left, self.paddle_right)

                payload = struct.pack(
                    '<B f f f f B f B f f f f f f f f',
                    2,  # message_type
                    updated_ball["position"]["x"],
                    updated_ball["position"]["y"],
                    updated_ball["velocity"]["x"],
                    updated_ball["velocity"]["y"],
                    int(updated_ball["is_out_of_bounds"]),
                    updated_ball["curve"],
                    updated_ball["bounced_off_surface"],
                    self.paddle_left.width,
                    self.paddle_left.height,
                    self.paddle_left.position,
                    self.paddle_left.speed,
                    self.paddle_right.width,
                    self.paddle_right.height,
                    self.paddle_right.position,
                    self.paddle_right.speed,
                )

                await self.send(bytes_data=payload)
                await asyncio.sleep(GAME_STATE_UPDATE_INTERVAL)

        except asyncio.CancelledError:
            logger.info("🛑 Game update loop cancelled.")
        except Exception as e:
            logger.error(f"❌ Error in game update loop: {e}")
