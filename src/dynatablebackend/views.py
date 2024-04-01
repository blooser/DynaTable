from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from dynatable.logger import get_logger
from dynatablebackend.serializers import ColumnListSerializer
from dynatablebackend.db import tables
from dynatablebackend.db.util import get_dynamic_model

logger = get_logger("dynatablebackend.views")


@api_view(["POST"])
def create_table(request: Request):
    """
    API view to create a new table.

    Handles POST requests to create a new table with specified columns. The request data
    should contain serialized column data. The function validates the data, creates a new
    table, and returns the table identifier.

    Args:
        request (Request): The request object containing serialized column data.

    Returns:
        Response: A Response object with the status code and created table identifier.
    """
    logger.info("Received request to create a new table")

    serializer = ColumnListSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error(
            f"Table creation failed due to invalid serializer data: {serializer.errors}"
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    columns = list(serializer.data)
    table_id = tables.create_table(columns)

    if table_id is None:
        logger.error("Failed to create table due to an internal error")
        return Response(
            {"message": "Failed to create table"}, status=status.HTTP_400_BAD_REQUEST
        )

    logger.info(f"Table created successfully with table_id: {table_id}")
    return Response({"table_id": table_id}, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_table_structure(request: Request, table_id: str):
    """
    API view to update the structure of an existing table.

    Handles PUT requests to modify the structure of a table identified by 'table_id'.
    The request data should contain serialized column data for updates. The function validates
    the data, checks if the table is empty, and updates the table's structure.

    Args:
        request (Request): The request object containing serialized column data.
        table_id (str): Identifier of the table to update.

    Returns:
        Response: A Response object with the status code and update status message.
    """
    logger.info(f"Received request to update table structure for '{table_id}'")

    serializer = ColumnListSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error(
            f"Update failed for table '{table_id}' due to invalid serializer data: {serializer.errors}"
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    DynamicModel = get_dynamic_model(table_id)
    if DynamicModel is None:
        logger.error(f"Update failed - Table '{table_id}' does not exist")
        return Response(
            {"message": f"Table '{table_id}' does not exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    is_empty = DynamicModel.objects.count() == 0
    if not is_empty:
        logger.error(f"Update failed - Table '{table_id}' contains data")
        return Response(
            {"message": f"Table '{table_id}' contains data, create new model then"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    columns = list(serializer.data)
    tables.update_table(table_id, columns)
    logger.info(f"Table structure for '{table_id}' updated successfully")
    return Response(
        {"message": "Table structure updated."}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def add_table_row(request: Request, table_id: str):
    """
    API view to add a new row to a specified table.

    Handles POST requests to add a new row of data to the table identified by 'table_id'.
    The request data should contain the data for the new row. The function validates the
    data and adds a new row to the specified table.

    Args:
        request (Request): The request object containing the data for the new row.
        table_id (str): Identifier of the table to add the row to.

    Returns:
        Response: A Response object with the status code and row addition status message.
    """
    logger.info(f"Received request to add new row to table '{table_id}'")

    data = request.data
    if not tables.add_table_row(table_id, data):
        logger.error(f"Failed to add row to table '{table_id}'")
        return Response(
            {"message": "Failed to add row to table"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    logger.info(f"Row added successfully to table '{table_id}'")
    return Response({"message": "Row added to table."}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_table_rows(request: Request, table_id: str):
    """
    API view to retrieve all rows from a specified table.

    Handles GET requests to fetch all rows of data from the table identified by 'table_id'.
    The function retrieves all the rows and returns them in the response.

    Args:
        request (Request): The request object.
        table_id (str): Identifier of the table from which to retrieve rows.

    Returns:
        Response: A Response object with the status code and the data rows from the table.
    """

    logger.info(f"Received request to retrieve rows from table '{table_id}'")

    rows = tables.get_table_rows(table_id)
    logger.info(f"Rows retrieved successfully from table '{table_id}'")
    return Response({"table_id": table_id, "rows": rows}, status=status.HTTP_200_OK)
