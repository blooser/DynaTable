from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dynatable.logger import get_logger
from dynatablebackend.serializers import ColumnListSerializer
from dynatablebackend.db import engine, tables

logger = get_logger("dynatablebackend.views")


@api_view(["POST"])
def create_table(request):
    logger.info("Creating table")

    serializer = ColumnListSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    columns = list(serializer.data)

    table_id = tables.create_table(engine, columns)

    if table_id is None:
        return Response(
            {"message": "Failed to create table"}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"table_id": table_id}, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_table_structure(request, id):
    logger.info("Updating table")

    serializer = ColumnListSerializer(data=request.data)

    if serializer.is_valid():
        return Response(
            {"message": "Table structure updated."}, status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_table_row(request, id):
    logger.info("Adding new table row")

    return Response({"message": "Row added to table."}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_table_rows(request, id):
    logger.info("Retrieving table")

    return Response({"message": "Rows retrieved."}, status=status.HTTP_200_OK)
