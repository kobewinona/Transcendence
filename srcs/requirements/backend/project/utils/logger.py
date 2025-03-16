import logging

from colorama import Fore, Style


class CustomFormatter(logging.Formatter):
    LEVEL_COLORS = {
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.LIGHTWHITE_EX + Fore.RED,
    }

    LOGGER_COLORS = {
        "game_logs": Fore.CYAN,
        "auth_logs": Fore.LIGHTGREEN_EX,
        "fast-reload_logs": Fore.MAGENTA,
        "tournaments_logs": Fore.LIGHTBLUE_EX,
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
