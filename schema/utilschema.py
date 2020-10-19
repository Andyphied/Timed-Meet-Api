from .schema import ma


class GenericMsgSchema(ma.Schema):
    msg = ma.String()


class PaginateSchama(ma.Schema):
    limit = ma.Integer()
    skip = ma.Integer()
