from .models import Base, db
from datetime import timedelta


class Meeting(Base):
    """The Meeting Models"""

    __tablename__ = "meetings"
    __table_args__ = (db.UniqueConstraint("user_id", "meeting_name"), )

    id = db.Column(db.Integer, primary_key=True)
    meeting_name = db.Column(db.String(255), nullable=False)
    meeting_date = db.Column(db.Date)
    description = db.Column(db.String(255))
    set_duration = db.Column(db.Interval, default=timedelta(seconds=0))
    final_duration = db.Column(db.Interval, default=timedelta(seconds=0))
    set_start_time = db.Column(db.Time)
    set_end_time = db.Column(db.Time)
    final_start_time = db.Column(db.Time)
    final_end_time = db.Column(db.Time)
    completed = db.Column(db.Boolean)
    agendas = db.relationship("Agenda", backref='meeting', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
