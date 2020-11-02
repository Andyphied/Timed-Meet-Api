from flask_marshmallow import Marshmallow
from marshmallow import EXCLUDE

ma = Marshmallow()


class BaseSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = ma.Integer(dump_only=True)
    created_on = ma.DateTime(dump_only=True)
    updated_on = ma.DateTime(dump_only=True)
