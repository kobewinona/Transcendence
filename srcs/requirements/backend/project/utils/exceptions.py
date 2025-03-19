from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Force 401 for authentication errors
    if isinstance(exc, AuthenticationFailed):
        return Response(
            {"detail": str(exc), "code": "authentication_failed"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
