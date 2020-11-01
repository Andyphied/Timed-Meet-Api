from .schema import ma, BaseSchema


class AgendaCreateSchema(BaseSchema):

    agenda_name = ma.String(required=True)
    set_duration = ma.TimeDelta(precision='seconds', required=False)
    meeting_id = ma.Integer(required=True)


class AgendaSchema(AgendaCreateSchema):

    final_duration = ma.TimeDelta(precision='seconds', required=False)

    _links = ma.Hyperlinks({
        'self':
        ma.URLFor('AgendaUpdateGetDelete', values=dict(agend_id='<id>')),
        'meeting':
        ma.URLFor('MeetingDetail', values=dict(id='<meeting_id>'))
    })


class AgendaUpdateSchema(AgendaCreateSchema):
    agenda_name = ma.String(required=False)
    meeting_id = ma.Integer(dump_only=True)


class AgendaCompleteSchema(ma.Schema):
    final_duration = ma.TimeDelta(precision='seconds', required=True)
