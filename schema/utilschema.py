from .schema import ma


class GenericMsgSchema(ma.Schema):
    msg = ma.String()


class PaginateSchema(ma.Schema):
    limit = ma.Integer()
    skip = ma.Integer()
