from .schema import ma, BaseSchema


class AgendaCreateSchema(BaseSchema):

    agenda_name = ma.String(required=True)
    set_duration = ma.TimeDelta(precision='seconds', required=False)
    set_start_time = ma.Time(required=True)
    set_end_time = ma.Time(required=False)
    meeting_id = ma.Integer(required=True)


class AgendaSchema(AgendaCreateSchema):

    final_duration = ma.TimeDelta(precision='seconds', required=False)
    final_start_time = ma.Time(required=True)
    final_end_time = ma.Time(required=False)

    _links = ma.Hyperlinks({
        'self':
        ma.URLFor('AgendaDetail', values=dict(id='<id>')),
        'meeting':
        ma.URLFor('MeetingDetail', values=dict(id='<meeting_id>'))
    })
