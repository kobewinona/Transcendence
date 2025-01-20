import logging
import math
import asyncio
from .constants import (PADDLE_BOUNDARY_GRACE_OFFSET,
                        BALL_OFF_BOUNDS_OFFSET,
                        BALL_DEFAULT_WIDTH,
                        BALL_DEFAULT_HEIGHT,
                        BALL_DEFAULT_POSITION_X,
                        BALL_DEFAULT_POSITION_Y,
                        BALL_MIN_VELOCITY_X,
                        BALL_VELOCITY_X_INCREMENT,
                        BALL_MIN_VELOCITY_Y,
                        BALL_MAX_VELOCITY_CHANGE_ON_HIT,
                        MAX_CURVE_ANGLE)

logger = logging.getLogger('pong.ball')


class Ball:
    def __init__(self, width=BALL_DEFAULT_WIDTH, height=BALL_DEFAULT_HEIGHT):
        self.position = {"x": BALL_DEFAULT_POSITION_X, "y": BALL_DEFAULT_POSITION_Y}
        self.velocity = {"x": BALL_MIN_VELOCITY_X, "y": BALL_MIN_VELOCITY_Y}
        self.width = width
        self.height = height
        self.radius_x = width / 2
        self.radius_y = height / 2
        self.is_out_of_bounds = False
        self.curve = 0
        self.bouncedOffSurface = 0

    def reset(self):
        self.position = {"x": BALL_DEFAULT_POSITION_X, "y": BALL_DEFAULT_POSITION_Y}
        self.velocity = {"x": BALL_MIN_VELOCITY_X, "y": BALL_MIN_VELOCITY_Y}
        self.is_out_of_bounds = False
        self.curve = 0

    def update_radius(self):
        self.radius_x = self.width / 2
        self.radius_y = self.height / 2

    def calculate_velocity_adjustment(self, paddle_position, paddle_height):
        relative_hit_position = (self.position["y"] - paddle_position) / (paddle_height / 2)
        return abs(BALL_MAX_VELOCITY_CHANGE_ON_HIT * max(-1, min(1, relative_hit_position)))

    def apply_curve(self):
        if self.curve != 0:
            self.curve = max(-MAX_CURVE_ANGLE, min(MAX_CURVE_ANGLE, self.curve))
            curve_radians = math.radians(self.curve)
            current_speed = math.sqrt(self.velocity["x"]**2 + self.velocity["y"]**2)
            angle = math.atan2(self.velocity["y"], self.velocity["x"]) + curve_radians

            self.velocity["x"] = current_speed * math.cos(angle)
            self.velocity["y"] = current_speed * math.sin(angle)

            # Gradually reduce curve effect
            self.curve *= 0.98
            if abs(self.curve) < 0.05:
                self.curve = 0

    async def update_ball(self, paddle_left, paddle_right):
        self.apply_curve()
        self.position["x"] += self.velocity["x"]
        self.position["y"] += self.velocity["y"]
        self.update_radius()

        # Ball boundaries
        ball_left = self.position["x"] - self.radius_x
        ball_right = self.position["x"] + self.radius_x
        ball_top = self.position["y"] - self.radius_y
        ball_bottom = self.position["y"] + self.radius_y
        paddle_left_lower_boundary = paddle_left.position - (paddle_left.height / 2) - PADDLE_BOUNDARY_GRACE_OFFSET
        paddle_left_upper_boundary = paddle_left.position + (paddle_left.height / 2) + PADDLE_BOUNDARY_GRACE_OFFSET
        paddle_right_lower_boundary = paddle_right.position - (paddle_right.height / 2) - PADDLE_BOUNDARY_GRACE_OFFSET
        paddle_right_upper_boundary = paddle_right.position + (paddle_right.height / 2) + PADDLE_BOUNDARY_GRACE_OFFSET

        if self.is_out_of_bounds and 0 <= self.position["x"] <= 100:
            self.is_out_of_bounds = False

        # Handle Paddles Collisions
        if not self.is_out_of_bounds:
            # Handle Left Paddle Collision
            if (ball_left + 2 <= paddle_left.width and
                    paddle_left_lower_boundary <= self.position["y"] <= paddle_left_upper_boundary):
                speed_adjustment = paddle_left.speed / 10
                self.velocity["x"] -= BALL_VELOCITY_X_INCREMENT + speed_adjustment
                self.velocity["x"] *= -1
                self.position["x"] = paddle_left.width + self.radius_x  # Prevent ball from clipping through
                self.velocity["y"] += self.calculate_velocity_adjustment(paddle_right.position, paddle_right.height)
                self.bouncedOffSurface = 4
                await asyncio.sleep(0.04)
                self.curve += paddle_left.speed * 3
                logger.debug("✅ Ball collided with LEFT paddle")

            # Handle Right Paddle Collision
            if (ball_right - 2 >= 100 - paddle_right.width and
                    paddle_right_lower_boundary <= self.position["y"] <= paddle_right_upper_boundary):
                speed_adjustment = paddle_left.speed / 10
                self.velocity["x"] += BALL_VELOCITY_X_INCREMENT + speed_adjustment
                self.velocity["x"] *= -1
                self.position["x"] = 100 - paddle_right.width - self.radius_x  # Prevent ball from clipping through
                self.velocity["y"] += self.calculate_velocity_adjustment(paddle_right.position, paddle_right.height)
                self.bouncedOffSurface = 2
                await asyncio.sleep(0.04)
                self.curve -= paddle_right.speed * 3
                logger.debug("✅ Ball collided with RIGHT paddle")

            if ball_left + self.width < paddle_left.width or ball_right + self.width >= 100 - paddle_right.width:
                self.is_out_of_bounds = True

        # Handle Top and Bottom Collisions
        if ball_top + 0.5 <= 0 or ball_bottom - 0.5 >= 100:
            self.bouncedOffSurface = 1 if ball_top <= 0 else 3
            self.velocity["y"] *= -1

        # Reset when ball goes out of boundaries
        if ((ball_left + self.width + BALL_OFF_BOUNDS_OFFSET) < 0 or
                (ball_right - self.width - BALL_OFF_BOUNDS_OFFSET) > 100):
            self.reset()

        return {
            "position": self.position,
            "velocity": self.velocity,
            "is_out_of_bounds": self.is_out_of_bounds,
            "curve": self.curve,
            "bounced_off_surface": self.bouncedOffSurface
        }
