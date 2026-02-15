from django.conf import settings


def set_jwt_cookies(response, access, refresh):
    response.set_cookie(
        key="access",
        value=str(access),
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
        max_age=60 * 15,
    )

    response.set_cookie(
        key="refresh",
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 7,
    )

def clear_jwt_cookies(response):
    response.delete_cookie(
        "access",
        path="/",
    )
    response.delete_cookie(
        "refresh",
        path="/",
    )
