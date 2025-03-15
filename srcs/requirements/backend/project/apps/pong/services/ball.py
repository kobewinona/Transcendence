import asyncio
import logging
import math
import random

from .constants import (
    DEMO_GAME_MODE,
    PADDLE_BOUNDARY_GRACE_OFFSET,
    BALL_OFF_BOUNDS_OFFSET,
    BALL_DEFAULT_WIDTH,
    BALL_DEFAULT_HEIGHT,
    BALL_DEFAULT_POSITION_X,
    BALL_DEFAULT_POSITION_Y,
    BALL_MIN_VELOCITY_X,
    BALL_VELOCITY_X_INCREMENT,
    BALL_MIN_VELOCITY_Y,
    BALL_SPEED_MULTIPLIERS,
    BALL_MAX_VELOCITY_CHANGE_ON_HIT,
    MAX_CURVE_ANGLE,
    MAX_CURVE_ANGLE_OPTIONS,
    PAUSE_ON_RESET,
)

logger = logging.getLogger("game_logs")


class Ball:
    def __init__(self, width=BALL_DEFAULT_WIDTH, height=BALL_DEFAULT_HEIGHT):
        self.position = {"x": BALL_DEFAULT_POSITION_X, "y": BALL_DEFAULT_POSITION_Y}
        self.velocity = {"x": BALL_MIN_VELOCITY_X, "y": BALL_MIN_VELOCITY_Y}
        self.width = width
        self.height = height
        self.radius_x = width / 4
        self.radius_y = height / 4
        self.is_out_of_bounds = False
        self.curve = 0
        self.bouncedOffSurface = 0
        self.pause_timer = 0
        self.max_curve_angle = MAX_CURVE_ANGLE
        self.min_velocity_x = BALL_MIN_VELOCITY_X
        self.min_velocity_y = BALL_MIN_VELOCITY_Y

    def get_current_ball_state(self):
        return {
            "position": self.position,
            "velocity": self.velocity,
            "is_out_of_bounds": self.is_out_of_bounds,
            "curve": self.curve,
            "bounced_off_surface": self.bouncedOffSurface,
        }

    def reset(self, game_mode):
        self.position = {"x": BALL_DEFAULT_POSITION_X, "y": BALL_DEFAULT_POSITION_Y}
        self.velocity = {
            "x": self.min_velocity_x * random.choice([-1, 1]),
            "y": self.min_velocity_y,
        }
        self.is_out_of_bounds = False
        self.curve = 0
        self.bouncedOffSurface = 0
        if game_mode != DEMO_GAME_MODE:
            self.pause_timer = PAUSE_ON_RESET * 60
        return self.get_current_ball_state()

    def set_ball_speed(self, speed):
        speed_multiplier = BALL_SPEED_MULTIPLIERS.get(speed, 1.0)
        self.min_velocity_x = BALL_MIN_VELOCITY_X * speed_multiplier
        self.min_velocity_y = BALL_MIN_VELOCITY_Y * speed_multiplier

    def set_ball_max_curve_angle(self, max_ball_curve):
        self.max_curve_angle = MAX_CURVE_ANGLE_OPTIONS.get(
            max_ball_curve, MAX_CURVE_ANGLE
        )

    def set_ball_dimensions(self, width, height):
        self.width = width
        self.height = height
        self.radius_x = width / 4
        self.radius_y = height / 4
        logger.info(
            f"✓ Ball dimensions set successfully: "
            f"width {self.width}, height {self.height}, "
            f"radius_x {self.radius_x}, radius_y {self.radius_y}"
        )

    def calculate_velocity_adjustment(self, paddle_position, paddle_height):
        relative_hit_position = (self.position["y"] - paddle_position) / (
            paddle_height / 2
        )
        return abs(
            BALL_MAX_VELOCITY_CHANGE_ON_HIT * max(-1, min(1, relative_hit_position))
        )

    def apply_curve(self):
        if self.curve != 0:
            self.curve = max(
                -self.max_curve_angle, min(self.max_curve_angle, self.curve)
            )
            curve_radians = math.radians(self.curve)
            current_speed = math.sqrt(self.velocity["x"] ** 2 + self.velocity["y"] ** 2)
            angle = math.atan2(self.velocity["y"], self.velocity["x"]) + curve_radians

            self.velocity["x"] = current_speed * math.cos(angle)
            self.velocity["y"] = current_speed * math.sin(angle)

            # Gradually reduce curve effect
            self.curve *= 0.98
            if abs(self.curve) < 0.05:
                self.curve = 0

    async def update_ball(self, game_mode, paddles, score, send_game_state):
        if self.pause_timer > 0:
            self.pause_timer -= 1
            return self.get_current_ball_state()

        winner = 0

        if score:
            winner = score.get_score().get("winner")

        if winner == 1 or winner == 2:
            return self.reset(game_mode)

        self.apply_curve()
        self.position["x"] += self.velocity["x"]
        self.position["y"] += self.velocity["y"]

        # Ball boundaries
        ball_left = self.position["x"] - self.radius_x
        ball_right = self.position["x"] + self.radius_x
        ball_top = self.position["y"] - self.radius_y
        ball_bottom = self.position["y"] + self.radius_y

        for paddle in paddles:
            paddle_lower_boundary = (
                paddle.position - (paddle.height / 2) - PADDLE_BOUNDARY_GRACE_OFFSET
            )
            paddle_upper_boundary = (
                paddle.position + (paddle.height / 2) + PADDLE_BOUNDARY_GRACE_OFFSET
            )

            if self.is_out_of_bounds and ball_left > 0 and ball_right < 100:
                self.is_out_of_bounds = False
                logger.debug(
                    f"ⓘ Ball is set to be in bounds: "
                    f"ball_left { ball_left }, ball_left + width { ball_left + self.width }, "
                    f"ball_right { ball_right }, ball_right + width { ball_right + self.width }, "
                )

            # Handle Paddles Collisions
            if not self.is_out_of_bounds:
                # Handle Left Paddle Collision
                if paddle.side == "left":
                    if (
                        self.position["x"] <= paddle.width
                        and paddle_lower_boundary
                        <= self.position["y"]
                        <= paddle_upper_boundary
                    ):

                        logger.debug(
                            f"ⓘ Ball collided with LEFT paddle: ball_left { ball_left } position_x { self.position['x'] }"
                        )

                        self.velocity["x"] -= (
                            BALL_VELOCITY_X_INCREMENT + paddle.speed / 10
                        )
                        self.velocity["x"] *= -1
                        self.position["x"] = (
                            paddle.width + self.radius_x
                        )  # Prevent ball from clipping through
                        self.velocity["y"] += self.calculate_velocity_adjustment(
                            paddle.position, paddle.height
                        )
                        self.bouncedOffSurface = 4
                        self.curve += paddle.speed * 3
                        await asyncio.sleep(0.04)
                        return self.get_current_ball_state()

                # Handle Right Paddle Collision
                if paddle.side == "right":
                    if (
                        self.position["x"] >= 100 - paddle.width
                        and paddle_lower_boundary
                        <= self.position["y"]
                        <= paddle_upper_boundary
                    ):
                        logger.debug(
                            f"ⓘ Ball collided with RIGHT paddle: ball_right { ball_right } position_x { self.position['x'] }"
                        )

                        self.velocity["x"] += (
                            BALL_VELOCITY_X_INCREMENT + paddle.speed / 10
                        )
                        self.velocity["x"] *= -1
                        self.position["x"] = (
                            100 - paddle.width - self.radius_x
                        )  # Prevent ball from clipping through
                        self.velocity["y"] += self.calculate_velocity_adjustment(
                            paddle.position, paddle.height
                        )
                        self.bouncedOffSurface = 2
                        self.curve -= paddle.speed * 3
                        await asyncio.sleep(0.04)
                        return self.get_current_ball_state()

                if ball_left <= 0 or ball_right >= 100:
                    if score:
                        score.update_score(
                            1 - (ball_left <= 0), 1 - (ball_right >= 100)
                        )
                    await send_game_state(f"Game score updated")

                    logger.debug(
                        f"ⓘ Ball is set to be out of bounds: "
                        f"ball_left { ball_left }, ball_left + width { ball_left + self.width }, "
                        f"ball_right { ball_right }, ball_right + width { ball_right + self.width }, "
                    )
                    self.is_out_of_bounds = True

        # Handle Top and Bottom Collisions
        if ball_top <= 0 or ball_bottom >= 100:
            self.velocity["y"] *= -1

            if ball_top <= 0:
                self.position["y"] = 0 + self.radius_y
                self.bouncedOffSurface = 1
            else:
                self.position["y"] = 100 - self.radius_y
                self.bouncedOffSurface = 3

        # Reset when ball goes out of boundaries
        if (ball_left + self.width + BALL_OFF_BOUNDS_OFFSET) < 0 or (
            ball_right - self.width - BALL_OFF_BOUNDS_OFFSET
        ) > 100:
            return self.reset(game_mode)

        return self.get_current_ball_state()
