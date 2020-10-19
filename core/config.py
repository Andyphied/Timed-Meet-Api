import os
from pathlib import Path
from datetime import timedelta

ENVIRON = os.environ.get("ENVIRON", "LOCAL")

if ENVIRON == "LOCAL":
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    path = dir_path / ".."
    MOCK_URI = "sqlite+pysqlite:///{file_path}"
    FILE_PATH = f"{path}/db/db.sqlite3"
    DB_URI = MOCK_URI.format(file_path=FILE_PATH)
    DEBUG = True

elif ENVIRON == "PRODUCTION":

    DB_URI = os.environ.get('DATABASE_URL')
    DEBUG = False


class Config(object):
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js")
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = DEBUG
    JWT_TOKEN_LOCATION = ('headers', 'cookies')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_BLACKLIST_ENABLED = True


class Setting():
    API_TITLE = os.environ.get("API_TITLE", "MEET API")
    API_VERSION = os.environ.get("API_VERSION", "0.1")
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY',
                                         'OS0ceYEcMyZ9fqtCZO0F9A')


setting = Setting()
