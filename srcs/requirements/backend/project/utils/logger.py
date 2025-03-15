import logging

from colorama import Fore, Style


class CustomFormatter(logging.Formatter):
    LEVEL_COLORS = {
        "DEBUG": Fore.BLUE,  # Blue
        "INFO": Fore.GREEN,  # Green
        "WARNING": Fore.YELLOW,  # Yellow
        "ERROR": Fore.RED,  # Red
        "CRITICAL": Fore.LIGHTWHITE_EX + Fore.RED,
    }

    LOGGER_COLORS = {
        "game_logs": Fore.CYAN,  # Cyan for game logs
        "rest_api": Fore.LIGHTGREEN_EX,
    }

    def format(self, record):
        # Color the logger name uniquely
        logger_color = self.LOGGER_COLORS.get(record.name, Fore.RESET)
        logger_name = f"{logger_color}[{record.name}]{Style.RESET_ALL}"

        # Apply log level color to the rest of the message
        level_color = self.LEVEL_COLORS.get(record.levelname, Fore.RESET)
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        log_message = record.getMessage()

        return f"{logger_name} {level_color}{record.levelname} {timestamp}: {log_message}{Style.RESET_ALL}"
