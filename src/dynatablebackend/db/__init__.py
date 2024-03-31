from sqlalchemy import create_engine

from dynatablebackend.db.config import URI

engine = create_engine(URI)
