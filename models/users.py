from .models import Base, db


class User(Base):
    """The Users Models"""

    __tabelename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    full_name = db.Column(db.String(255))
    hashed_password = db.Column(db.String(255))
    is_superuser = db.Column(db.Boolean, default=False)
