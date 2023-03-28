from functools import lru_cache

from starlite import ASGIConnection, BaseRouteHandler


async def is_authorized(connection: ASGIConnection, handler: BaseRouteHandler) -> None:
    pass
    # validate authorization
    # if not authorized, raise NotAuthorizedException
    # raise NotAuthorizedException()



@lru_cache(maxsize=1)
def load_pub_key():
    with open('resources/key.pub') as f:
        pub_key = f.read()
    return pub_key