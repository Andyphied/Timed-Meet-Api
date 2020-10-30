from .models import Base, db


class Meeting(Base):
    """The Meeting Models"""

    __tablename__ = "meetings"
    __table_args__ = (db.UniqueConstraint("user_id", "meeting_name"), )

    id = db.Column(db.Integer, primary_key=True)
    meeting_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    set_duration = db.Column(db.Interval)
    final_duration = db.Column(db.Interval)
    set_start_time = db.Column(db.Time)
    set_end_time = db.Column(db.Time)
    final_start_time = db.Column(db.Time)
    final_end_time = db.Column(db.Time)
    completed = db.Column(db.Boolean)
    agendas = db.relationship("Agenda", backref='meeting', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
