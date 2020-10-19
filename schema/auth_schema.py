from marshmallow import INCLUDE, EXCLUDE

from .schema import ma
from models import TokenBlacklist


class TokenSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    access_token = ma.String(required=True)
    refresh_token = ma.String(required=True)
    token_type = ma.String(required=True)


class RefreshTokenSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    access_token = ma.String(required=True)
    token_type = ma.String(required=True)


class AuthTokenSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    Authorization = ma.String()


class ChgPasswordSchma(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    old_password = ma.String(required=True)
    new_password = ma.String(required=True)


class TokenBlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TokenBlacklist
        unknown = INCLUDE

    id = ma.Integer(data_key='token_id')
