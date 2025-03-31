import logging
import os
import subprocess

from django.core.management.base import BaseCommand

from watchfiles import watch

logger = logging.getLogger("fast-reload_logs")


class Command(BaseCommand):
    help = "Watch for file changes and restart services"

    @staticmethod
    def restart_services():
        logger.info("↻ Restarting Django and Daphne...")
        try:
            subprocess.run(["supervisorctl", "restart", "django"], check=True)
            subprocess.run(["supervisorctl", "restart", "daphne"], check=True)
            logger.info("✓ Restart complete.")
        except subprocess.CalledProcessError as e:
            logger.error(f"✕ Error restarting services: {e}")

    def handle(self, *args, **kwargs):
        watch_path = os.getcwd()
        ignored_files = (".log", ".pyc", "__pycache__")

        logger.info(f"✓ 👀 Watching for file changes...")

        try:
            for changes in watch(watch_path, recursive=True):
                filtered_changes = [
                    (change_type, path)
                    for change_type, path in changes
                    if not any(ignore in path for ignore in ignored_files)
                ]

                if filtered_changes:
                    logger.debug(f"ⓘ Detected changes: { filtered_changes }")

                    mypy_result = subprocess.run(
                        ["pipenv", "run", "mypy", "."],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    if mypy_result.returncode == 0:
                        logger.info("✓ No Mypy issues found. Restarting services...")
                        self.restart_services()
                    else:
                        logger.error("✕ Mypy found issues, skipping restart.")
                        if mypy_result.stdout.strip():
                            logger.error(f"Mypy Output:\n{mypy_result.stdout}")
        except KeyboardInterrupt:
            logger.error("✕ Stopping file watcher...")
