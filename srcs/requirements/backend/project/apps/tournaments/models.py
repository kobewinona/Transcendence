import json
import logging
import random
from django.conf import settings
import uuid
from typing import Optional


from django.contrib.auth import get_user_model
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

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"

    def generate_brackets(self):
        players_list = self.players.copy()

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

                brackets[stage].append(match)
                next_round.append(None)

            current_round = next_round
            num_matches //= 2
            stage_index += 1

        self.brackets = json.loads(json.dumps(brackets))
        self.save()

    def update_bracket(self, tournament_id, winner_name, score_data):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            logger.error(f"Tournament {tournament_id} not found.")
            return False

        brackets = tournament.brackets
        updated_brackets = brackets.copy()

        def stage_sort_key(stage):
            if stage == "Final":
                return float("inf")
            try:
                num, denom = map(int, stage.split("/"))
                return num / denom
            except Exception:
                return float("inf")

        sorted_stage_names = sorted(brackets.keys(), key=stage_sort_key)
        logger.debug(f"sorted_stage_names: { sorted_stage_names }")

        winner_stage = None
        winner_stage_index = None
        winner_match_index = None
        winner_side = None

        # Find latest stage where winner is present
        for stage_index, stage_name in enumerate(sorted_stage_names):
            matches = brackets.get(stage_name, [])
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

            logger.debug(f"✔ Updated match with winner and score: {updated_match}")

        logger.debug(f"updated_brackets: { updated_brackets }")
        logger.debug(f"winner_stage: { winner_stage }")
        logger.debug(f"winner_stage_index: { winner_stage_index }")
        logger.debug(f"next stage index: { winner_stage_index + 1 }")

        if winner_stage == "Final":
            tournament.winner = winner_name
            tournament.status = "finished"
        else:
            logger.debug("adding winner to the next stage...")
            matches = brackets.get(sorted_stage_names[winner_stage_index + 1], [])
            logger.debug(f"next stage matches: { matches }")

            # Find available slots (only one side is empty)
            available_slots = []
            for i, match in enumerate(matches):
                if match.get("left") is None:
                    available_slots.append((i, "left"))
                if match.get("right") is None:
                    available_slots.append((i, "right"))
            logger.debug(f"available_slots: { available_slots }")

            if available_slots:
                selected_index, side = random.choice(available_slots)
                logger.debug(f"selected_index: { selected_index }")
                logger.debug(f"side: { side }")
                logger.debug(
                    f"✓ Selected random match index: {selected_index}, side: {side}"
                )
                winner_player = updated_brackets[winner_stage][winner_match_index][
                    winner_side
                ]
                logger.debug(f"winner_player: { winner_player }")
                updated_brackets[sorted_stage_names[winner_stage_index + 1]][
                    selected_index
                ][side] = winner_player
                logger.debug("✓ Winner inserted into next stage")
            else:
                logger.warning("⚠️ No available slots in next stage to insert winner")

        tournament.brackets = updated_brackets
        tournament.save()
        logger.info(f"✓ UPDATED BRACKETS: { updated_brackets }")
