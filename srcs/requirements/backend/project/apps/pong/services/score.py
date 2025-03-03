import logging

logger = logging.getLogger("game_logs")

# winner == 0 no winner yet
# winner == 1 left side wins
# winner == 2 right side wins


class Score:
    def __init__(self, end_score=11, is_deuce_on=True):
        self.end_score = end_score
        self.deuce_score = end_score - 1
        self.is_deuce_on = is_deuce_on
        self.left = 0
        self.is_left_advantage = False
        self.right = 0
        self.is_right_advantage = False
        self.is_deuce = False
        self.winner = 0

    def update_score(self, left, right):
        self.left += left
        self.right += right

        # Check for deuce activation
        if (
            self.is_deuce_on
            and self.left == self.deuce_score
            and self.right == self.deuce_score
        ):
            logger.debug(f"ⓘ Game is in deuce")
            self.is_deuce = True

        if self.is_deuce:
            if (
                not self.is_left_advantage
                and self.left == self.end_score
                and self.right == self.deuce_score
            ):
                self.is_left_advantage = True
                self.left -= 1

                if self.is_left_advantage and self.is_right_advantage:
                    self.is_left_advantage = False
                    self.is_right_advantage = False

                return
            elif (
                not self.is_right_advantage
                and self.right == self.end_score
                and self.left == self.deuce_score
            ):
                self.is_right_advantage = True
                self.right -= 1

                if self.is_left_advantage and self.is_right_advantage:
                    self.is_left_advantage = False
                    self.is_right_advantage = False

                return

            if self.left == self.end_score and self.is_left_advantage:
                self.winner = 1
            elif self.right == self.end_score and self.is_right_advantage:
                self.winner = 2
        else:
            # Regular win condition
            if self.left == self.end_score:
                self.winner = 1
            elif self.right == self.end_score:
                self.winner = 2

        logger.debug(f"ⓘ Score updated: left: {self.left}, right {self.right}")

    def get_score(self):
        return {
            "left": self.left,
            "right": self.right,
            "is_left_advantage": self.is_left_advantage,
            "is_right_advantage": self.is_right_advantage,
            "is_deuce": self.is_deuce,
            "winner": self.winner,
        }
