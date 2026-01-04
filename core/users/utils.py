def set_jwt_cookies(response, access, refresh):
    response.set_cookie(
        key="access",
        value=access,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
    )
    response.set_cookie(
        key="refresh",
        value=refresh,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
    )


def clear_jwt_cookies(response):
    response.delete_cookie("access")
    response.delete_cookie("refresh")
