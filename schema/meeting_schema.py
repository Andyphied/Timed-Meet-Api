from .schema import ma, BaseSchema
from flask_marshmallow.fields import Hyperlinks, URLFor
from models import Meeting


class MeetingCreateSchema(BaseSchema):

    meeting_name = ma.String(required=True)
    description = ma.String(required=False)
    meeting_date = ma.Date(required=False)
    set_duration = ma.TimeDelta(precision='seconds', required=False)
    set_start_time = ma.Time(required=True)
    set_end_time = ma.Time(required=False)
    user_id = ma.Integer(dump_only=True)


class MeetingSchemaAdmin(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meeting
        include_fk = True


class MeetingSchema(MeetingCreateSchema):

    final_duration = ma.TimeDelta(precision='seconds', required=False)
    final_start_time = ma.Time(required=False)
    final_end_time = ma.Time(required=False)


class MeetingSchemaUser(MeetingSchema):
    class Meta:
        model = Meeting

    _links = Hyperlinks({
        'user':
        URLFor('MyUserDetails', values=None),
        'agendas':
        URLFor('MeetingAgendas', values=dict(meeting_id='<meeting_id>')),
    })


class StartMeetingSchema(ma.Schema):
    meeting_id = ma.Integer(required=True)
    start_time = ma.Time(required=True)
