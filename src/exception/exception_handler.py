from starlite import Request, Response
from starlite.status_codes import HTTP_500_INTERNAL_SERVER_ERROR


def json_exception_handler(_: Request, exc: Exception) -> Response:
    """Default handler for exceptions subclassed from HTTPException."""
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", "")

    return Response(
        content={"message": detail, "status_code": status_code},
        status_code=status_code
    )
