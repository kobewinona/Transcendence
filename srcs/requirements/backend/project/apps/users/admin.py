from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
        "auth_provider",
        "avatar",
        "intra_id",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email", "auth_provider", "intra_id")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("auth_provider", "avatar", "intra_id")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    readonly_fields = ("auth_provider", "intra_id", "last_login", "date_joined")
