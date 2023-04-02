from functools import lru_cache

import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from starlite import ASGIConnection, NotAuthorizedException, BaseRouteHandler


async def user_authorization(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    auth_header = connection.headers.get('authorization')
    if not auth_header:
        raise NotAuthorizedException("Authentication header is not present")
    try:
        public_key = load_pub_key()
        jwt.decode(auth_header, public_key, algorithms=['RS256'])
    except InvalidSignatureError:
        raise NotAuthorizedException("The token signature is invalid")
    except ExpiredSignatureError:
        raise NotAuthorizedException("The token has expired")
    except DecodeError:
        raise NotAuthorizedException("The token is not valid")


async def admin_authorization(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    auth_header = connection.headers.get('authorization')
    public_key = load_pub_key()
    decoded_token = jwt.decode(auth_header, public_key, algorithms=['RS256'])
    if decoded_token.get('scope') not in ['ROLE_USER']:
        raise NotAuthorizedException("You are not authorized to access this resource")


@lru_cache(maxsize=1)
def load_pub_key():
    with open('src/resources/key.pub') as f:
        pub_key = f.read()
    return pub_key
