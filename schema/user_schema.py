from .schema import BaseSchema, ma


class UserRegSchema(BaseSchema):
    """A schema to validate what is sent in when registering"""

    email = ma.String(required=True)
    password = ma.String(load_only=True)
    full_name = ma.String(required=True)
    is_superuser = ma.Boolean()


class UserUpdateSchema(BaseSchema):
    """A schema to validate what is sent in when registering"""

    email = ma.String()
    full_name = ma.String()


class UserLoginSchema(ma.Schema):
    """The schema to help validate login arguments"""

    email = ma.String(required=True)
    password = ma.String(required=True)
