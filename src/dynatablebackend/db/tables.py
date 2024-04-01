from typing import Any, Dict, List

import shortuuid
from django.db import connection
from dynatable.logger import get_logger

from dynatablebackend.db.util import (
    create_dynamic_model,
    get_combined_fields,
    get_dynamic_model,
    obj_to_dict,
    to_model_types,
)

logger = get_logger(__name__)


def create_table(columns: List[Dict[str, str]], table_id: str | None = None):
    """
    Creates a new table in the database with the specified columns and table identifier.

    This function first converts the given column definitions to Django model field types,
    then dynamically creates a new Django model with these fields. It proceeds to create
    a corresponding table in the database for this model using Django's schema editor.
    The function generates a unique table identifier if not provided.

    Args:
        columns (list of dict): A list of dictionaries representing columns to create, where
                                each dictionary contains 'name' (field name) and 'type' (field data type).
        table_id (str, optional): An optional unique identifier for the table. If not provided,
                                  a random UUID will be generated.

    Returns:
        str: The table identifier of the newly created table.

    Example:
        columns = [{"name": "title", "type": "string"}, {"name": "author", "type": "string"}]
        table_id = create_table(columns)
        # Creates a new table with 'title' and 'author' columns, and returns its table_id.
    """
    logger.info(
        f"Starting to create new table '{table_id}' with {len(columns)} columns"
    )

    if table_id is None:
        logger.info("Generating table id")

        table_id = shortuuid.uuid()

    model_types = to_model_types(columns)

    DynamicModel = create_dynamic_model(table_id, model_types)

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(DynamicModel)

    logger.info(f"Table '{table_id}' successfully created with {len(columns)} columns")

    return table_id


def update_table(table_id: str, columns: List[Dict[str, str]]):
    """
    Updates the schema of a specified table by adding new columns or overriding existing ones.

    This function retrieves an existing dynamic model based on the provided table_id, combines its
    fields with the new columns specified, deletes the old model's table schema, and then creates a
    new table schema with the updated fields. It effectively updates the table schema in the database
    to match the new combined fields configuration.

    Args:
        table_id (str): The identifier of the table to be updated.
        columns (list of dict): A list of dictionaries representing the columns to update or add.
                                Each dictionary should contain 'name' (field name) and 'type' (field data type).

    Returns:
        str: The table identifier of the updated table.

    Example:
        columns_to_update = [{"name": "bio", "type": "string"}]
        table_id = update_table("UserProfile", columns_to_update)
        # Updates the 'UserProfile' table by adding or modifying the 'bio' column.
    """
    logger.info(
        f"Starting to update table '{table_id}' with {len(columns)} new/updated columns"
    )

    DynamicModel = get_dynamic_model(table_id)

    combined_fields = get_combined_fields(table_id, columns)

    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(DynamicModel)

        NewDynamicModel = create_dynamic_model(table_id, combined_fields)

        schema_editor.create_model(NewDynamicModel)

    logger.info(
        f"Table '{table_id}' successfully updated with {len(columns)} new/updated columns"
    )

    return table_id


def add_table_row(table_id: str, row: List[Dict[str, Any]]):
    """
    Adds a new row to the specified table in the database.

    This function retrieves the dynamic model associated with the given table_id and
    creates a new record for this model using the provided row data. It attempts to save
    the new record to the database. If an exception occurs during the save operation,
    the function returns False indicating failure.

    Args:
        table_id (str): The identifier of the table to which the row will be added.
        row (dict): A dictionary representing the data for the new row, where keys are field names
                    and values are the corresponding values for each field in the record.

    Returns:
        bool: True if the record is successfully added to the database, False otherwise.

    Example:
        row_data = {"title": "Sample Title", "author": "Author Name"}
        success = add_table_row("BlogPost", row_data)
        # Attempts to add a new row to 'BlogPost' table and returns True if successful.
    """

    logger.info(f"Attempting to add a new row to table '{table_id}'")

    DynamicModel = get_dynamic_model(table_id)

    new_model_record = DynamicModel(**row)

    try:
        new_model_record.save()
        logger.info(f"New row added to table '{table_id}'")
    except Exception as e:
        logger.error(f"Failed to add a new row to table '{table_id}': {e}")

        return False

    return True


def get_table_rows(table_id: str):
    """
    Retrieves all rows from the specified table in the database.

    This function fetches the dynamic model associated with the given table_id and
    queries all records present in the corresponding table. It converts each record
    into a dictionary format and returns a list of these dictionaries.

    Args:
        table_id (str): The identifier of the table from which the rows are to be retrieved.

    Returns:
        list of dict: A list of dictionaries, where each dictionary represents a row from the table.
                      Each dictionary's keys correspond to the field names of the table.

    Example:
        rows = get_table_rows("Person")
        # Returns a list of dictionaries representing each row in the 'Person' table, e.g., [{"name": "Matt", "age": 112}, ...]

    Note:
        The function assumes that a utility function `obj_to_dict` is defined to convert
        model instances to dictionaries.
    """
    logger.info(f"Fetching rows from table '{table_id}'")

    DynamicModel = get_dynamic_model(table_id)

    items = DynamicModel.objects.all()

    logger.info(f"Rows from table '{table_id}' successfully retrieved")

    return list(map(lambda x: obj_to_dict(x), items))
