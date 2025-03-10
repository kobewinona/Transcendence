import os
import subprocess
from watchfiles import watch
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Watch for file changes and restart services"

    @staticmethod
    def restart_services():
        print("↻ Restarting Django and Daphne...")
        try:
            subprocess.run(["supervisorctl", "restart", "django"], check=True)
            subprocess.run(["supervisorctl", "restart", "daphne"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"✕ Error restarting services: {e}")

    def handle(self, *args, **kwargs):
        watch_path = os.getcwd()
        ignored_files = (".log", ".pyc", "__pycache__")

        print(f"✓ 👀 Watching for file changes...")

        try:
            for changes in watch(watch_path, recursive=True):
                filtered_changes = [
                    (change_type, path)
                    for change_type, path in changes
                    if not any(ignore in path for ignore in ignored_files)
                ]

                if filtered_changes:
                    print("ⓘ Detected changes:", filtered_changes)
                    self.restart_services()
        except KeyboardInterrupt:
            print("✕ Stopping file watcher...")
