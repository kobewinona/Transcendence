from django.apps import AppConfig

class CustomAuthConfig(AppConfig):  # Change from AuthConfig to CustomAuthConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.apps.custom_auth'
