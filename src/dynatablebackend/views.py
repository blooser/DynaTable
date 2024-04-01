from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dynatable.logger import get_logger
from dynatablebackend.serializers import ColumnListSerializer
from dynatablebackend.db import tables
from dynatablebackend.db.util import get_dynamic_model

logger = get_logger("dynatablebackend.views")


@api_view(["POST"])
def create_table(request):
    logger.info("Creating table")

    serializer = ColumnListSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    columns = list(serializer.data)

    table_id = tables.create_table(columns)

    if table_id is None:
        return Response(
            {"message": "Failed to create table"}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"table_id": table_id}, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_table_structure(request, id):
    logger.info("Updating table")

    serializer = ColumnListSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    DynamicModel = get_dynamic_model(id)

    if DynamicModel is None:
        return Response(
            {"message": f"Table with id={id} does not exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    is_empty = DynamicModel.objects.count() == 0

    if not is_empty:
        return Response(
            {"message": f"Table '{id}' contains data, create new model then"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    columns = list(serializer.data)

    tables.update_table(id, columns)

    return Response(
        {"message": "Table structure updated."}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def add_table_row(request, id):
    logger.info("Adding new table row")

    data = request.data

    if not tables.add_table_row(id, data):
        return Response(
            {"message": "Failed to add row to table"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response({"message": "Row added to table."}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_table_rows(request, id):
    logger.info("Retrieving table")

    rows = tables.get_table(id)

    return Response({"rows": rows}, status=status.HTTP_200_OK)
