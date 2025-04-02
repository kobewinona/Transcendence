import logging
import random

import requests
from django.contrib.auth import get_user_model
from project.apps.tournaments.models import Tournament
from project.authentication import JWTOrIntraAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()
logger = logging.getLogger("tournaments_logs")

API_RANDOMUSER_URL = "https://randomuser.me/api/"
API_RANDOMUSER_BUFFER_MULTIPLIER = 2


def get_next_power_of_two(n):
    return 1 if n < 1 else 2 ** (n - 1).bit_length()


def fetch_unique_random_names(existing_names, needed):
    tries = 0
    max_tries = 5
    unique_names = set()
    generated_players = []

    while len(unique_names) < needed and tries < max_tries:
        tries += 1
        fetch_count = needed * API_RANDOMUSER_BUFFER_MULTIPLIER
        res = requests.get(f"{API_RANDOMUSER_URL}?results={fetch_count}")
        res.raise_for_status()

        data = res.json()
        logger.info(f"Random names data results: {data['results']}")
        for user in data["results"]:
            name = user["login"]["username"]
            if name not in existing_names and name not in unique_names:
                unique_names.add(name)
                generated_players.append(
                    {
                        "name": name,
                        "controlled_by": "ai",
                        "key": user["login"]["uuid"],
                    }
                )

    return generated_players[:needed]


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
        logger.debug(f"UserTournaments POST data: {data}")

        errors = {}

        tournament_name = data.get("name")
        if not tournament_name:
            errors["name"] = "Tournament name is required"
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        players = data.get("players", [])
        if not isinstance(players, list) or len(players) < 2:
            return Response(
                {"error": "At least two players are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            existing_names = {
                p.get("name", "").strip() for p in players if p.get("name")
            }
            player_count = len(players)
            target_count = get_next_power_of_two(player_count)
            shortage = target_count - player_count

            if shortage > 0:
                new_players = fetch_unique_random_names(existing_names, shortage)
                players.extend(new_players)

            logger.info(f"updated players: {players}")

            for player in players:
                name = player.get("name", "").strip()
                if not name:
                    return Response(
                        {"error": "Player name is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            names = [p.get("name", "").strip() for p in players]
            if len(set(names)) < len(names):
                return Response(
                    {"error": "All player names must be unique."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        logger.debug(f"players: {players}")

        game = data.get("game", {})
        gameplay = data.get("gameplay", {})

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
                "notified": t.notified,
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

    def patch(self, request, tournament_id):
        user = request.user

        try:
            t = Tournament.objects.get(host=user, id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {"error": "No tournament found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        status_update = data.get("status")
        winner_update = data.get("winner")
        notified_update = data.get("notified")

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
            t.status = status_update
        if winner_update:
            t.winner = winner_update
        if notified_update:
            t.notified = notified_update

        t.save()

        return Response(
            {
                "id": str(t.id),
                "winner": t.winner,
                "notified": t.notified,
                "name": t.name,
                "host": {"id": t.host.id, "email": t.host.email},
                "status": t.status,
                "players": t.players,
                "game": t.game,
                "gameplay": t.gameplay,
                "brackets": t.brackets,
                "created_at": t.created_at.isoformat(),
                "updated_at": t.updated_at.isoformat(),
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
        logger.debug(f"sorted_stage_names: {sorted_stage_names}")

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

        logger.debug(f"updated_brackets: {updated_brackets}")
        logger.debug(f"winner_stage: {winner_stage}")
        logger.debug(f"winner_stage_index: {winner_stage_index}")
        logger.debug(f"next stage index: {winner_stage_index + 1}")

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
            logger.debug(f"available_slots: {available_slots}")

            if available_slots:
                selected_index, side = random.choice(available_slots)
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
        logger.info(f"✓ UPDATED BRACKETS: {updated_brackets}")
        return Response(
            {
                "id": str(tournament.id),
                "winner": winner_name,
                "score": score_data,
                "updated_at": tournament.updated_at.isoformat(),
            },
            status=status.HTTP_200_OK,
        )
