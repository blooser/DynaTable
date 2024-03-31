from sqlalchemy import Table, Column, MetaData
from sqlalchemy.orm import sessionmaker

from dynatable.logger import get_logger
from dynatablebackend.db.util import str_to_column_type

import shortuuid

from functools import lru_cache

logger = get_logger("dynatablebackend.db")


def create_table(engine, columns):
    table_id = shortuuid.uuid()

    logger.info(f"Creating new table '{table_id}' with {len(columns)} columns")

    metadata = MetaData()

    column_definitions = [
        Column(column["name"], str_to_column_type(column["type"])) for column in columns
    ]

    table = Table(table_id, metadata, *column_definitions)

    table.create(engine)

    return table_id


def update_table(engine, table_id, new_columns):
    logger.info(f"Updating table id={table_id}")

    ...


def add_table_row(engine, table_id, row):
    logger.info(f"Adding rows to table id={table_id}")

    ...


@lru_cache(maxsize=32)
def get_table(engine, table_id):
    logger.info(f"Retrieving table id={table_id}")

    metadata = MetaData()
    table = Table(table_id, metadata)

    with sessionmaker(bind=engine) as session:
        return list(session.query(table).all())
