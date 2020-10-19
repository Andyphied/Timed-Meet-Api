from .schema import ma
from marshmallow import EXCLUDE


class UserRegSchema(ma.Schema):
    """A schema to validate what is sent in when registering"""
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    email = ma.String(required=True)
    password = ma.String(load_only=True)
    full_name = ma.String(required=True)
    is_superuser = ma.Boolean()


class UserUpdateSchema(ma.Schema):
    """A schema to validate what is sent in when registering"""
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    email = ma.String()
    full_name = ma.String()


class UserLoginSchema(ma.Schema):
    """The schema to help validate login arguments"""
    class Meta:
        unknown = EXCLUDE

    email = ma.String(required=True)
    password = ma.String(required=True)
