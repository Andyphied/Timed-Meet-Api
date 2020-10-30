from .models import Base, db


class Agenda(Base):
    """The Agenda Models"""

    __tablename__ = "agendas"
    __table_args__ = (db.UniqueConstraint("meeting_id", "agenda_name"), )

    id = db.Column(db.Integer, primary_key=True)
    agenda_name = db.Column(db.String(255), nullable=False)
    set_duration = db.Column(db.Interval)
    final_duration = db.Column(db.Interval)
    set_start_time = db.Column(db.Time)
    set_end_time = db.Column(db.Time)
    final_start_time = db.Column(db.Time)
    final_end_time = db.Column(db.Time)
    completed = db.Column(db.Boolean)
    meeting_id = db.Column(db.Integer,
                           db.ForeignKey('meeting.id'),
                           nullable=False)
