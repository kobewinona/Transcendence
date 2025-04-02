import asyncio
import json
import logging
import struct

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .services import (
    GameState,
    Ball,
    Paddle,
    Score,
    GAME_STATUS_INIT,
    GAME_STATUS_IDLE,
    GAME_STATUS_IN_PROGRESS,
    GAME_STATUS_ENDED,
    GAME_STATUS_PAUSED,
    GAME_ERROR_MESSAGE_TYPE,
    GAME_STATE_UPDATE_INTERVAL,
    BALL_DEFAULT_WIDTH,
    BALL_DEFAULT_HEIGHT,
)

logger = logging.getLogger("game_logs")


class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = None
        self.game_mode = None
        self.ball = None
        self.paddles = {}
        self.score = None
        self.are_dimensions_set = False
        self.game_update_task = None
        self.paddle_update_task = None
        self.pause_event = asyncio.Event()
        self.pause_event.set()
        self.tournament_id = None
        self.players = {}
        self.is_tournament_updated = False

    async def connect(self):
        self.game_state = GameState()
        self.ball = Ball()
        await self.accept()
        await self.set_game_status(GAME_STATUS_IDLE)
        logger.info("✓ Pong WebSocket Connected")

    async def disconnect(self, close_code):
        if self.game_update_task:
            self.game_update_task.cancel()
            await self.set_game_status(GAME_STATUS_ENDED)
        logger.debug("ⓘ Pong WebSocket Disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "update_dimensions":
                await self.handle_update_dimensions(data)

            elif action == "start":
                self.pause_event.set()
                await self.handle_start(data)

            elif action == "pause":
                self.pause_event.clear()
                await self.set_game_status(GAME_STATUS_PAUSED)

            elif action == "resume":
                self.pause_event.set()
                await self.set_game_status(GAME_STATUS_IN_PROGRESS)

            elif action == "stop":
                self.pause_event.set()
                await self.handle_stop()

            elif action == "update_paddle":
                await self.handle_paddle(data)

            else:
                await self.send(text_data=json.dumps({"error": "Unknown action"}))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))

    async def update_tournament(self):
        from project.apps.tournaments.services import update_bracket

        score = self.score.get_score()
        winner = score.get("winner")
        winner_name = self.players[winner][0]

        await sync_to_async(update_bracket)(
            self.tournament_id,
            winner_name,
            {"left": score.get("left"), "right": score.get("right")},
        )

    async def handle_update_dimensions(self, data):
        self.ball.set_ball_dimensions(
            data.get("ball_width", BALL_DEFAULT_WIDTH),
            data.get("ball_height", BALL_DEFAULT_HEIGHT),
        )

        if not self.are_dimensions_set:
            self.are_dimensions_set = True
            logger.info("✓ Dimensions set successfully")
            await self.send_game_state()

    async def handle_start(self, data):
        logger.debug(f"ⓘ Game Settings: {data}")

        await self.set_game_status(GAME_STATUS_INIT)

        self.players = {1: [], 2: []}
        self.tournament_id = None
        self.is_tournament_updated = False

        settings = data.get("data", {})

        self.game_mode = settings.get("mode")
        self.tournament_id = settings.get("tournament_id", None)

        controllers = settings.get("controllers", [])
        if not controllers:
            logger.error("✕ Cannot start game: No controllers found in settings!")
            await self.set_game_status(GAME_STATUS_IDLE)
            await self.send(
                text_data=json.dumps(
                    {"error": "Cannot start game: No controllers found in settings!"}
                )
            )
            return

        game = settings.get("game")
        try:
            if game:
                end_score = game.get("end_score")
                is_deuce_on = game.get("is_deuce_on")

                logger.debug(f"Parsed end_score={end_score}, is_deuce_on={is_deuce_on}")

                self.score = Score(end_score=end_score, is_deuce_on=is_deuce_on == 2)
                logger.debug("✓ Score successfully set")

        except Exception as e:
            logger.error(f"✕ Failed to initialize Score: {e}")
            await self.set_game_status(GAME_STATUS_IDLE)
            await self.send(
                text_data=json.dumps({"error": "Failed to initialize Score"})
            )
            return

        gameplay = settings.get("gameplay")
        try:
            if gameplay:
                ball_speed = gameplay.get("ball_speed")
                self.ball.set_ball_speed(ball_speed)
                max_ball_curve = gameplay.get("max_ball_curve")
                self.ball.set_ball_max_curve_angle(max_ball_curve)
        except Exception as e:
            logger.error(f"✕ Failed to apply gameplay settings: {e}")
            await self.set_game_status(GAME_STATUS_IDLE)
            await self.send(
                text_data=json.dumps({"error": "Invalid gameplay settings"})
            )
            return

        self.paddles = {}
        try:
            self.paddles = {}
            for ctrl in controllers:
                paddle_name = ctrl["name"]
                paddle_side = ctrl["side"]
                if paddle_side == "left":
                    self.players[1].append(paddle_name)
                else:
                    self.players[2].append(paddle_name)
                self.paddles[paddle_name] = Paddle(name=paddle_name, side=paddle_side)
                logger.info(f"✓ Created paddle: {paddle_name}")
        except Exception as e:
            logger.error(f"✕ Failed to create paddles: {e}")
            await self.set_game_status(GAME_STATUS_IDLE)
            await self.send(text_data=json.dumps({"error": "Failed to create paddles"}))
            return

        try:
            if self.game_update_task:
                self.ball.reset(self.game_mode)
                for paddle in self.paddles.values():
                    paddle.reset()
                self.game_update_task.cancel()
                logger.info(
                    "✓ Game update loop canceled as part of initializing a new loop process"
                )
                await self.set_game_status(GAME_STATUS_ENDED)
        except Exception as e:
            logger.error(f"✕ Failed during game reset: {e}")
            await self.set_game_status(GAME_STATUS_IDLE)
            await self.send(
                text_data=json.dumps({"error": "Failed to reset previous game"})
            )
            return

        try:
            self.game_update_task = asyncio.create_task(self.game_update_loop())
            await self.set_game_status(GAME_STATUS_IN_PROGRESS)
            logger.info("✓ Game update loop started")
        except Exception as e:
            logger.error(f"✕ Failed to start new game update loop: {e}")
            await self.set_game_status(GAME_STATUS_IDLE)
            await self.send(
                text_data=json.dumps({"error": "Failed to start game loop"})
            )

    async def handle_paddle(self, data):
        paddle_name = data.get("name")
        direction = data.get("direction", 0)

        if paddle_name in self.paddles:
            self.paddles[paddle_name].set_direction(direction)

    async def handle_stop(self):
        if self.game_update_task:
            self.game_update_task.cancel()

        self.score = None

        await self.set_game_status(GAME_STATUS_ENDED)
        await self.set_game_status(GAME_STATUS_IDLE)

    async def set_game_status(self, status):
        self.game_state.status = status
        await self.send_game_state()

    async def send_game_error(self, message=""):
        message_bytes = message.encode("utf-8")
        message_length = len(message_bytes)

        payload = struct.pack(
            f"<B I {message_length}s",
            GAME_ERROR_MESSAGE_TYPE,
            message_length,
            message_bytes,
        )

        await self.send(bytes_data=payload)

    async def send_game_state(self):
        score_data = self.score.get_score() if self.score else {}

        payload = {
            "type": "game_state",
            "status": self.game_state.status,
            "leftScore": score_data.get("left", 0),
            "rightScore": score_data.get("right", 0),
            "isDeuce": score_data.get("is_deuce", False),
            "isLeftAdvantage": score_data.get("is_left_advantage", False),
            "isRightAdvantage": score_data.get("is_right_advantage", False),
            "winner": score_data.get("winner", 0),
        }

        await self.send(text_data=json.dumps(payload))

    async def game_update_loop(self):
        try:
            while True:
                if self.score:
                    winner = self.score.get_score().get("winner")
                    if (
                        (winner == 1 or winner == 2)
                        and self.tournament_id
                        and not self.is_tournament_updated
                    ):
                        await self.update_tournament()
                        self.is_tournament_updated = True

                await self.pause_event.wait()

                for paddle in self.paddles.values():
                    paddle.update_position()

                updated_ball = await self.ball.update_ball(
                    self.game_mode,
                    self.paddles.values(),
                    self.score,
                    self.send_game_state,
                )

                payload_format = "<f f f f B f B" + (" f f f f" * len(self.paddles))
                payload_values = [
                    updated_ball["position"]["x"],  # (4 bytes)
                    updated_ball["position"]["y"],  # (4 bytes)
                    updated_ball["velocity"]["x"],  # (4 bytes)
                    updated_ball["velocity"]["y"],  # (4 bytes)
                    int(updated_ball["is_out_of_bounds"]),  # (1 byte)
                    updated_ball["curve"],  # (4 bytes)
                    updated_ball["bounced_off_surface"],  # (1 byte)
                ]

                offset = struct.calcsize("<f f f f B f B")  # Calculate base size
                for paddle in self.paddles.values():
                    payload_values.extend(
                        [
                            paddle.width,  # (4 bytes)
                            paddle.height,  # (4 bytes)
                            paddle.position,  # (4 bytes)
                            paddle.speed,  # (4 bytes)
                        ]
                    )
                    offset += struct.calcsize("<f f f f")

                payload = struct.pack(payload_format, *payload_values)
                await self.send(bytes_data=payload)
                await asyncio.sleep(GAME_STATE_UPDATE_INTERVAL)

        except asyncio.CancelledError:
            logger.info("✓ Game update loop cancelled.")
        except Exception as e:
            logger.error(f"✕ Error in game update loop: {e}")
