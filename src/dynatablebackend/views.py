from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dynatable.logger import get_logger


logger = get_logger("dynatablebackend.views")


@api_view(["POST"])
def create_table(request):
    logger.info("Creating table")

    return Response({"message": "Table created."}, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_table_structure(request, id):
    logger.info("Updating table")

    return Response({"message": "Table structure updated."}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_table_row(request, id):
    logger.info("Adding new table row")

    return Response({"message": "Row added to table."}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_table_rows(request, id):
    logger.info("Retrieving table")

    return Response({"message": "Rows retrieved."}, status=status.HTTP_200_OK)
