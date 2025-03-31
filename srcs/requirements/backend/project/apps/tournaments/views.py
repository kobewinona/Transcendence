import logging
import random

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from project.apps.tournaments.models import Tournament
from project.authentication import JWTOrIntraAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()
logger = logging.getLogger("tournaments_logs")


class UserTournaments(APIView):
    authentication_classes = [JWTOrIntraAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if Tournament.objects.filter(host=user, status="in_progress").exists():
            return Response(
                {"error": "There is already an active tournament in progress."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data
        logger.debug(f"UserTournaments POST data: { data }")
        tournament_name = data.get("name")
        players = data.get("players", [])
        game = data.get("game", {})
        gameplay = data.get("gameplay", {})

        errors = {}

        if not tournament_name:
            errors["name"] = "Tournament name is required"

        if not isinstance(players, list) or len(players) < 2:
            errors["error"] = "At least two players are required"
        else:
            seen_names = set()
            player_errors = []

            for player in players:
                player_error = {}
                name = player.get("name", "").strip()

                if not name:
                    player_error["name"] = "Player name is required"
                elif name in seen_names:
                    player_error["name"] = "Player name must be unique"
                else:
                    seen_names.add(name)

                player_errors.append(player_error)

            if any(player_errors):
                errors["players"] = player_errors

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        tournament = Tournament.objects.create(
            name=tournament_name,
            host=user,
            players=players,
            game=game,
            gameplay=gameplay,
        )
        tournament.generate_brackets()

        response_data = {
            "id": str(tournament.id),
            "name": tournament.name,
            "host": {"id": tournament.host.id, "email": tournament.host.email},
            "status": tournament.status,
            "players": tournament.players,
            "brackets": tournament.brackets,
            "game": tournament.game,
            "gameplay": tournament.gameplay,
            "created_at": tournament.created_at.isoformat(),
            "updated_at": tournament.updated_at.isoformat(),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        status_filter = request.query_params.get("status")
        tournaments_query = Tournament.objects.filter(host=user).order_by("-created_at")

        if status_filter:
            tournaments_query = tournaments_query.filter(status=status_filter)

        response_data = [
            {
                "id": str(t.id),
                "winner": t.winner,
                "name": t.name,
                "host": {"id": t.host.id, "email": t.host.email},
                "status": t.status,
                "players": t.players,
                "game": t.game,
                "gameplay": t.gameplay,
                "brackets": t.brackets,
                "created_at": t.created_at.isoformat(),
                "updated_at": t.updated_at.isoformat(),
            }
            for t in tournaments_query
        ]

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user

        try:
            tournament = Tournament.objects.get(host=user, status="in_progress")
        except Tournament.DoesNotExist:
            return Response(
                {"error": "No active tournament found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        status_update = data.get("status")
        winner_update = data.get("winner")

        # Validate status
        valid_statuses = ["in_progress", "finished", "abandoned"]
        if status_update and status_update not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Choose from {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if status_update == "finished" and not winner_update:
            return Response(
                {
                    "error": "A winner must be provided when marking the tournament as finished."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Apply updates
        if status_update:
            tournament.status = status_update
        if winner_update:
            tournament.winner = winner_update

        tournament.save()

        return Response(
            {
                "id": str(tournament.id),
                "name": tournament.name,
                "status": tournament.status,
                "winner": tournament.winner,
                "updated_at": tournament.updated_at.isoformat(),
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, tournament_id):
        data = request.data
        winner_name = data.get("winner")
        score_data = data.get("score", {})

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
                updated_brackets[sorted_stage_names[winner_stage_index + 1]][
                    selected_index
                ][side] = {"name": winner_name}
                logger.debug("✓ Winner inserted into next stage")
            else:
                logger.warning("⚠️ No available slots in next stage to insert winner")

        tournament.brackets = updated_brackets
        tournament.save()
        logger.info(f"✓ UPDATED BRACKETS: { updated_brackets }")
        return Response(
            {
                "id": str(tournament.id),
                "winner": winner_name,
                "score": score_data,
                "updated_at": tournament.updated_at.isoformat(),
            },
            status=status.HTTP_200_OK,
        )
