import os

if os.getenv("Testing", "False") == "True":
    URI = "sqllite///:memory:"
else:
    URI = "postgresql://postgres:postgres@localhost:5432/dynatable"
