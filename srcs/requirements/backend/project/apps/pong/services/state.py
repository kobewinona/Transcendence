import json
import logging

from .constants import GAME_STATUS_IDLE, GAME_COUNTDOWN_DURATION

logger = logging.getLogger("game_logs")


class GameState:
    def __init__(self):
        self._status = GAME_STATUS_IDLE
        self._countdown_value = 0

    # Status getters and setters
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        logger.info(f"✓ Game status successfully changed. New status: {value}")
        self._status = value

    # Countdown value getters and setters
    @property
    def countdown_value(self):
        return self._countdown_value

    @countdown_value.setter
    def countdown_value(self, value):
        if value < 0:
            raise ValueError("Countdown value cannot be negative")
        self._countdown_value = value

    # Serialize the current game state for sending to clients
    def to_dict(self):
        return {
            "status": self._status,
            "countdown_value": self._countdown_value,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    # Reset the game state to its initial values
    def reset(self):
        self._status = GAME_STATUS_IDLE
        self._countdown_value = GAME_COUNTDOWN_DURATION
