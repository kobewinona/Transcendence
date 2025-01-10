import logging
from .constants import (BALL_OFF_BOUNDS_OFFSET,
                        BALL_DEFAULT_WIDTH,
                        BALL_DEFAULT_HEIGHT,
                        BALL_DEFAULT_POSITION_X,
                        BALL_DEFAULT_POSITION_Y,
                        BALL_MIN_VELOCITY_X,
                        BALL_MIN_VELOCITY_Y)

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

    def reset(self):
        self.position = {"x": BALL_DEFAULT_POSITION_X, "y": BALL_DEFAULT_POSITION_Y}
        self.velocity = {"x": BALL_MIN_VELOCITY_X, "y": BALL_MIN_VELOCITY_Y}
        self.is_out_of_bounds = False

    def update_radius(self):
        self.radius_x = self.width / 2
        self.radius_y = self.height / 2

    def update_ball(self, paddle_left, paddle_right):
        self.position["x"] += self.velocity["x"]
        self.position["y"] += self.velocity["y"]
        self.update_radius()

        # Ball boundaries
        ball_left = self.position["x"] - self.radius_x
        ball_right = self.position["x"] + self.radius_x
        ball_top = self.position["y"] - self.radius_y
        ball_bottom = self.position["y"] + self.radius_y
        paddle_left_lower_boundary = paddle_left.position - (paddle_left.height / 2)
        paddle_left_upper_boundary = paddle_left.position + (paddle_left.height / 2)
        paddle_right_lower_boundary = paddle_right.position - (paddle_right.height / 2)
        paddle_right_upper_boundary = paddle_right.position + (paddle_right.height / 2)

        if self.is_out_of_bounds and 0 <= self.position["x"] <= 100:
            self.is_out_of_bounds = False

        # Handle Paddles Collisions
        if not self.is_out_of_bounds:
            # Handle Left Paddle Collision
            if (ball_left <= paddle_left.width and
                    paddle_left_lower_boundary <= self.position["y"] <= paddle_left_upper_boundary):
                self.velocity["x"] *= -1
                self.position["x"] = paddle_left.width + self.radius_x  # Prevent ball from clipping through
                logger.debug("✅ Ball collided with LEFT paddle")

            # Handle Right Paddle Collision
            if (ball_right >= 100 - paddle_right.width and
                    paddle_right_lower_boundary <= self.position["y"] <= paddle_right_upper_boundary):
                self.velocity["x"] *= -1
                self.position["x"] = 100 - paddle_right.width - self.radius_x  # Prevent ball from clipping through
                logger.debug("✅ Ball collided with RIGHT paddle")

            if ball_left + self.width < paddle_left.width or ball_right + self.width >= 100 - paddle_right.width:
                self.is_out_of_bounds = True

        # Handle Top and Bottom Collisions
        if ball_top <= 0 or ball_bottom >= 100:
            self.velocity["y"] *= -1

        # Reset when ball goes out of boundaries
        if ((ball_left + self.width + BALL_OFF_BOUNDS_OFFSET) < 0 or
                (ball_right - self.width - BALL_OFF_BOUNDS_OFFSET) > 100):
            self.reset()

        return {
            "position": self.position,
            "velocity": self.velocity,
            "is_out_of_bounds": self.is_out_of_bounds
        }
