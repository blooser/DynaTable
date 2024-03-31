from django.db import connection


from dynatable.logger import get_logger
from dynatablebackend.db.util import (
    create_dynamic_model,
    get_dynamic_model,
    to_model_types,
    obj_to_dict,
)

import shortuuid

from functools import lru_cache

logger = get_logger("dynatablebackend.db")


def create_table(columns):
    table_id = shortuuid.uuid()

    logger.info(f"Creating new table '{table_id}' with {len(columns)} columns")

    fields = to_model_types(columns)

    dynamic_model = create_dynamic_model(table_id, fields)

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(dynamic_model)

    return table_id


def update_table(table_id, new_columns):
    logger.info(f"Updating table id={table_id}")

    ...


def add_table_row(table_id, row):
    logger.info(f"Adding row to table '{table_id}'")

    DynamicModel = get_dynamic_model(table_id)

    new_record = DynamicModel(**row)

    new_record.save()

    return True


@lru_cache(maxsize=32)
def get_table(table_id):
    logger.info(f"Retrieving table '{table_id}'")

    DynamicModel = get_dynamic_model(table_id)

    items = DynamicModel.objects.all()

    return list(map(lambda x: obj_to_dict(x), items))
