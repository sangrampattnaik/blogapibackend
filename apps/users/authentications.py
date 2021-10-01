import datetime

import jwt
import tortoise
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from config import settings

from .models import User

jwt_token = APIKeyHeader(
    name="Authorization",
    scheme_name="Bearer JWT token",
    description="provide token as format (Bearer JWT-TOKEN)",
)


async def authetnicate(token: str = Depends(jwt_token)) -> User:
    try:
        if token is None:
            raise HTTPException(detail="unauthorized access", status_code=401)

        prefix, value = token.split()
        if prefix != "Bearer":
            raise HTTPException(detail="unauthorized access", status_code=401)
        payload = jwt.decode(value, settings.SECRET_KEY, "HS256")
        user = await User.get(id=payload["id"])
        return user
    except (
        ValueError,
        tortoise.exceptions.DoesNotExist,
        jwt.ExpiredSignatureError,
        jwt.exceptions.InvalidSignatureError,
    ):
        raise HTTPException(detail="unauthorized access", status_code=401)


async def create_jwt_token(user: User, /) -> str:
    payload = {
        "id": user.id,
        "type": "Bearer",
        "exp": datetime.datetime.utcnow() + settings.EXPIRATION_TIME
        ## You can add also these things
        # jti
        # username
        # mobile
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
