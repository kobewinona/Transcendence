import json
import logging
import random
import uuid
from typing import Optional

from django.conf import settings
from django.db import models

logger = logging.getLogger("tournaments_logs")


class Tournament(models.Model):
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name: models.CharField = models.CharField(max_length=100)
    host: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    players: models.JSONField = models.JSONField(default=list)
    brackets: models.JSONField = models.JSONField(default=dict)
    game: models.JSONField = models.JSONField(default=dict)
    gameplay: models.JSONField = models.JSONField(default=dict)

    status: models.CharField = models.CharField(
        max_length=20,
        choices=[
            ("in_progress", "In Progress"),
            ("finished", "Finished"),
            ("abandoned", "Abandoned"),
        ],
        default="in_progress",
    )

    winner: Optional[models.CharField] = models.CharField(
        max_length=100, null=True, blank=True
    )
    notified: models.BooleanField = models.BooleanField(default=False)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"

    def generate_brackets(self):
        players_list = self.players.copy()
        auto_advance_ai_winners = []

        random.shuffle(players_list)

        num_players = len(players_list)
        if num_players < 2:
            raise ValueError(
                "At least two players are required to create a tournament."
            )

        brackets = {}

        # Assign stages
        num_rounds = num_players // 2
        stage_names = ["Final"]

        i = 2
        while i <= num_rounds:
            stage_names.insert(0, f"1/{i}")
            i *= 2

        # Assign stage players
        stage_index = 0
        num_matches = num_players // 2
        current_round = players_list

        while num_matches >= 1:
            stage = stage_names[stage_index]
            brackets[stage] = []

            next_round = []
            for i in range(0, len(current_round), 2):
                left_player = current_round[i]
                right_player = (
                    current_round[i + 1] if i + 1 < len(current_round) else None
                )

                match = {
                    "left": left_player,
                    "right": right_player,
                    "winner": None,
                    "score": {"left": 0, "right": 0},
                }

                if (
                    left_player
                    and right_player
                    and left_player["controlled_by"]
                    == right_player["controlled_by"]
                    == "ai"
                ):
                    end_score = self.game.get("end_score", 6)

                    winner = random.choice(["left", "right"])
                    loser = "right" if winner == "left" else "left"

                    match["winner"] = match[winner]
                    match["score"][winner] = end_score
                    match["score"][loser] = random.randint(0, end_score - 1)

                    logger.debug(f"ⓘ Early win for ai: {match['winner']['name']}")
                    auto_advance_ai_winners.append(
                        {
                            "winner_name": match[winner]["name"],
                            "score_data": match["score"],
                        }
                    )

                brackets[stage].append(match)
                next_round.append(None)

            current_round = next_round
            num_matches //= 2
            stage_index += 1

        self.brackets = json.loads(json.dumps(brackets))
        self.save()

        for data in auto_advance_ai_winners:
            self.update_bracket(
                tournament_id=self.id,
                winner_name=data["winner_name"],
                score_data=data["score_data"],
            )

    def update_bracket(self, tournament_id, winner_name, score_data):
        logger.info(
            f"ⓘ UPDATING BRACKET | winner_name: {winner_name}: score_data: {score_data}"
        )
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            logger.error(f"Tournament {tournament_id} not found.")
            return False

        brackets = tournament.brackets
        updated_brackets = brackets.copy()
        next_ai_winner = None

        def stage_sort_key(stage):
            if stage == "Final":
                return float("inf")
            try:
                num, denom = map(int, stage.split("/"))
                return num / denom
            except Exception:
                return float("inf")

        sorted_stage_names = sorted(brackets.keys(), key=stage_sort_key)

        winner_stage = None
        winner_stage_index = None
        winner_match_index = None
        winner_side = None

        # Find latest stage where winner is present
        for stage_index, stage_name in enumerate(sorted_stage_names):
            matches = brackets.get(stage_name, [])
            logger.debug(f"ⓘ Stage {stage_name} Matches: {matches}")
            for idx, match in enumerate(matches):
                left = match.get("left")
                right = match.get("right")

                if left and left.get("name") == winner_name:
                    winner_stage = stage_name
                    winner_stage_index = stage_index
                    winner_match_index = idx
                    winner_side = "left"
                elif right and right.get("name") == winner_name:
                    winner_stage = stage_name
                    winner_stage_index = stage_index
                    winner_match_index = idx
                    winner_side = "right"

        # Now update only if we found something
        if winner_stage is not None:
            logger.debug(
                f"✓ Found latest winner '{winner_name}' in stage '{winner_stage}', match index {winner_match_index}, side: {winner_side}"
            )

            updated_brackets = brackets.copy()
            updated_match = updated_brackets[winner_stage][winner_match_index]
            updated_match["winner"] = winner_name
            updated_match["score"] = score_data

            logger.debug(f"✓ Updated match with winner and score: {updated_match}")

        logger.debug(f"updated_brackets: {updated_brackets}")
        logger.debug(
            f"winner_stage: {winner_stage}, winner_stage_index: {winner_stage_index}, next stage index: {winner_stage_index + 1}"
        )

        if winner_stage == "Final":
            tournament.winner = winner_name
            tournament.status = "finished"
        else:
            logger.debug("adding winner to the next stage...")
            matches = brackets.get(sorted_stage_names[winner_stage_index + 1], [])
            logger.debug(f"next stage matches: {matches}")

            # Find available slots (only one side is empty)
            available_slots = []
            for i, match in enumerate(matches):
                if match.get("left") is None:
                    available_slots.append((i, "left"))
                if match.get("right") is None:
                    available_slots.append((i, "right"))

            if available_slots:
                selected_index, side = random.choice(available_slots)
                logger.debug(
                    f"✓ Selected random match stage: {winner_stage_index + 1}, index: {selected_index}, side: {side}, match: {updated_brackets[sorted_stage_names[winner_stage_index + 1]][selected_index]}"
                )
                winner_player = updated_brackets[winner_stage][winner_match_index][
                    winner_side
                ]
                updated_brackets[sorted_stage_names[winner_stage_index + 1]][
                    selected_index
                ][side] = winner_player
                logger.debug("✓ Winner inserted into next stage")

                opponent_side = "right" if side == "left" else "left"
                opponent = updated_brackets[sorted_stage_names[winner_stage_index + 1]][
                    selected_index
                ][opponent_side]

                if (
                    opponent
                    and opponent.get("controlled_by") == "ai"
                    and winner_player.get("controlled_by") == "ai"
                ):
                    logger.debug(
                        "AI vs AI detected in next stage, resolving automatically..."
                    )

                    end_score = tournament.game.get("end_score", 6)
                    winner_side = random.choice([side, opponent_side])
                    loser_side = opponent_side if winner_side == side else side
                    next_match = updated_brackets[
                        sorted_stage_names[winner_stage_index + 1]
                    ][selected_index]
                    actual_winner = next_match[winner_side]

                    new_score_data = {side: 0, opponent_side: 0}
                    new_score_data[winner_side] = end_score
                    new_score_data[loser_side] = random.randint(0, end_score - 1)

                    next_ai_winner = {
                        "winner_name": actual_winner.get("name"),
                        "score_data": new_score_data,
                    }
            else:
                logger.warning("⚠️ No available slots in next stage to insert winner")

        tournament.brackets = updated_brackets
        tournament.save()
        logger.info(f"✓ UPDATED BRACKETS: {updated_brackets}")

        logger.debug(f"next ai winner needs updating: {next_ai_winner}")
        if next_ai_winner:
            self.update_bracket(
                tournament_id=tournament.id,
                winner_name=next_ai_winner["winner_name"],
                score_data=next_ai_winner["score_data"],
            )
