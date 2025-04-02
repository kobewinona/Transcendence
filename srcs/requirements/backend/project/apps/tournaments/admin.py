from django.contrib import admin
from project.apps.tournaments.models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "winner",
        "notified",
        "host",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "host__email")
    list_filter = ("status",)
    ordering = ("-created_at",)
