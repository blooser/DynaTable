from sqlalchemy import text, Table, Column, MetaData, Integer
from sqlalchemy.orm import sessionmaker, registry

from dynatable.logger import get_logger
from dynatablebackend.db.util import (
    str_to_column_type,
    create_table_class,
    get_table_class,
)

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
    column_definitions.append(Column("id", Integer, primary_key=True))

    table = Table(table_id, metadata, *column_definitions)

    table_type = create_table_class(table_id)
    mapper_registry = registry()
    mapper_registry.map_imperatively(table_type, table)

    table.create(engine)

    return table_id


def update_table(engine, table_id, new_columns):
    logger.info(f"Updating table id={table_id}")

    ...


def add_table_row(engine, table_id, row):
    logger.info(f"Adding row to table '{table_id}'")

    metadata = MetaData()

    table = Table(table_id, metadata, autoload_with=engine)

    columns = table.columns.keys()

    if len(columns) - 1 != len(row.keys()):
        return False

    table_class = get_table_class(table_id)

    if table_class is None:
        return False

    Session = sessionmaker(bind=engine)

    table_row = table_class(**row)

    with Session() as session:
        session.add(table_row)
        session.commit()

    return True


@lru_cache(maxsize=32)
def get_table(engine, table_id):
    logger.info(f"Retrieving table id={table_id}")

    # metadata = MetaData()
    # table = Table(table_id, metadata)

    Session = sessionmaker(bind=engine)

    with Session() as session:
        query = text(f'SELECT * FROM "{table_id}"')
        result = session.execute(query)

        return map(lambda x: tuple(x), list(result.fetchall()))
