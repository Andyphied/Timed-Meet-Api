from .models import Base, db
from datetime import timedelta


class Agenda(Base):
    """The Agenda Models"""

    __tablename__ = "agendas"
    __table_args__ = (db.UniqueConstraint("meeting_id", "agenda_name"), )

    id = db.Column(db.Integer, primary_key=True)
    agenda_name = db.Column(db.String(255), nullable=False)
    set_duration = db.Column(db.Interval,
                             nullable=False,
                             default=timedelta(seconds=0))
    final_duration = db.Column(db.Interval, default=timedelta(seconds=0))
    completed = db.Column(db.Boolean)
    meeting_id = db.Column(db.Integer,
                           db.ForeignKey('meetings.id'),
                           nullable=False)
