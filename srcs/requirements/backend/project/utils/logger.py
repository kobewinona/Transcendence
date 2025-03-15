import logging

from colorama import Fore, Style


class CustomFormatter(logging.Formatter):
    COLORS = {
        "game_logs": Fore.CYAN,  # Light Blue for Game Logs
        "rest_api": Fore.GREEN,  # Green for API Logs
        "channels": Fore.YELLOW,  # Yellow for Channels Logs
        "django": Fore.MAGENTA,  # Magenta for Django Logs
    }

    def format(self, record):
        log_color = self.COLORS.get(record.name, Fore.RESET)
        label = f"[{record.name}] "
        record.message = super().format(record)
        return f"{log_color}{label}{record.message}{Style.RESET_ALL}"
