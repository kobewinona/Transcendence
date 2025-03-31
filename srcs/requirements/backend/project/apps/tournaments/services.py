from .models import Tournament
import logging

logger = logging.getLogger("tournaments_logs")


def update_bracket(tournament_id, winner_name, score):
    tournament = Tournament.objects.get(id=tournament_id)
    tournament.update_bracket(tournament_id, winner_name, score)
