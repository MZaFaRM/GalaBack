from rest_framework.response import Response
from .exceptions import AuthError


class CustomResponse:
    def __init__(self, status_code, message, data=None, error=None):
        self.status_code = status_code
        self.message = message
        self.data = data or {}
        self.error = error or ""

    def to_dict(self):
        return Response(
            status=self.status_code,
            data={
                "message": self.message,
                "data": self.data,
                "errors": self.error,
            },
        )


class HandleException:
    def __init__(self, message: str, data, exception: Exception = None) -> None:
        self.status_code = 401 if isinstance(exception, AuthError) else 400
        self.message = message
        self.error = str(exception) if exception else "Validation Error"
        self.data = data

    def send_response(self):
        return CustomResponse(
            status_code=self.status_code,
            message=self.message,
            error=self.error,
            data=self.data,
        ).to_dict()
