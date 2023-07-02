from typing import Any
from django.core.management import BaseCommand, CommandError
from django.db import connection
from pathlib import Path
import os

class Command(BaseCommand):
    help = "Populating database"
    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            current_dir = os.path.dirname(__file__)
            sqlfile_path = os.path.join(current_dir, 'data.sql')
            
            with connection.cursor() as cursor:
                cursor.execute(Path(sqlfile_path).read_text())
            
        except CommandError as err:
            print("Command failed")
