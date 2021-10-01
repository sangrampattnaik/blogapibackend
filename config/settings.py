import datetime
from pathlib import Path
import os

from decouple import config
from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ServerSetttings(BaseSettings):
    HOST: str = config("HOST")
    PORT: int = config("PORT", cast=int, default=8000)
    DEBUG: bool = config("DEBUG", default=True, cast=bool)
    RELOAD: bool = config("RELOAD", default=True, cast=bool)


class PathSettings(BaseSettings):
    MEDIA_ROOT: str = os.path.join(BASE_DIR,'media')
    MEDIA_URL: str = "/media"


class JWTSettings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY")
    EXPIRATION_TIME = datetime.timedelta(
        days=config("TOKEN_EXP_IN_DAYS", cast=int, default=0),
        hours=config("TOKEN_EXP_IN_HOURS", cast=int, default=0),
        minutes=config("TOKEN_EXP_IN_MINUTES", cast=int, default=15),
        seconds=config("TOKEN_EXP_IN_SECONDS", cast=int, default=0),
    )


class Settings(ServerSetttings, JWTSettings,PathSettings):
    pass

settings = Settings()
if not os.path.exists(settings.MEDIA_ROOT):
    os.mkdir(os.path.join(BASE_DIR,'media'))
