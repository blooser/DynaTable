from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def root(request):
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
