from .schema import ma, BaseSchema


class AgendaCreateSchema(BaseSchema):

    agenda_name = ma.String(required=True)
    set_duration = ma.TimeDelta(precision='seconds', required=False)
    meeting_id = ma.Integer(required=True)


class AgendaSchema(AgendaCreateSchema):

    final_duration = ma.TimeDelta(precision='seconds', required=False)
    completed = ma.Boolean(dump_only=True)

    _links = ma.Hyperlinks({
        'self':
        ma.URLFor('Agendas.AgendaUpdateGetDelete',
                  values=dict(agenda_id='<id>')),
        'meeting':
        ma.URLFor('Meetings.MeetingUpdateGetDelete',
                  values=dict(meeting_id='<meeting_id>'))
    })


class AgendaUpdateSchema(AgendaCreateSchema):
    agenda_name = ma.String(required=False)
    meeting_id = ma.Integer(dump_only=True)


class AgendaCompleteSchema(ma.Schema):
    final_duration = ma.TimeDelta(precision='seconds', required=True)
