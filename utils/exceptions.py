class AuthError(Exception):
    pass


class ValidationError(Exception):
    def __str__(self) -> str:
        return "Validation Error"
