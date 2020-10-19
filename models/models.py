from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    """The Base for other models"""

    __abstract__ = True

    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime,
                           default=datetime.now(),
                           onupdate=db.func.now())
