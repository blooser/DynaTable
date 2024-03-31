import os

from django.db import connection


if os.getenv("TESTING", "False") == "True":
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys=OFF")
