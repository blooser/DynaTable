from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dynatable.logger import get_logger

logger = get_logger("dynatable.views")


@api_view(["GET"])
def project_status(request):
    """
    API view that returns the status of the project.

    This view handles GET requests and returns information about the project,
    including its current status, application name, version, author, and contact email.

    Args:
        request: The incoming HTTP GET request.

    Returns:
        Response: A Response object containing project information in JSON format,
                  with an HTTP 200 OK status.

    Example:
        GET /api/project-status/
        Response:
            {
                "status": "running",
                "app": "DynaTable",
                "version": "0.0.1",
                "author": "Mateusz Solnica",
                "email": "blooser@protonmail.com"
            }
    """

    logger.debug("Returning project status")

    return Response(
        {
            "status": "running",
            "app": "DynaTable",
            "version": "0.0.1",
            "author": "Mateusz Solnica",
            "email": "blooser@protonmail.com",
        },
        status=status.HTTP_200_OK,
    )
