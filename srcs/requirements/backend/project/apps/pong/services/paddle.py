import logging
from .constants import (PADDLE_MAX_SPEED, PADDLE_ACCELERATION, PADDLE_DEACCELERATION)

logger = logging.getLogger('pong.paddle')


class Paddle:
    def __init__(self, position=50, boundary=100, width=2, height=6):
        """
        Paddle initialization with acceleration and deceleration.
        """
        self.position = position
        self.direction = 0
        self.speed = 0
        self.boundary = boundary
        self.width = width
        self.height = height

    def update_position(self):
        """
        Update paddle position based on direction, speed, and acceleration.
        """
        if self.direction != 0:
            self.speed += PADDLE_ACCELERATION * self.direction
            self.speed = max(-PADDLE_MAX_SPEED, min(self.speed, PADDLE_MAX_SPEED))
        else:
            if self.speed > 0:
                self.speed -= PADDLE_DEACCELERATION
                self.speed = max(0, self.speed)  # Prevent negative speed when decelerating
            elif self.speed < 0:
                self.speed += PADDLE_DEACCELERATION
                self.speed = min(0, self.speed)  # Prevent positive speed when decelerating
        self.position += self.speed

        # Clamp paddle position to stay within boundaries
        half_paddle_height = self.height / 2
        self.position = max(
            half_paddle_height,
            min(self.boundary - half_paddle_height, self.position)
        )

        return self.position

    def set_direction(self, direction):
        """
        Set paddle movement direction (-1 = up, 1 = down, 0 = stationary).
        """
        if direction in [-1, 0, 1]:
            self.direction = direction
