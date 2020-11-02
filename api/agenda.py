from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.utils import time_subtract, time_plus
from crud import user as user_crud, agenda as agenda_crud,\
    meeting as meeting_crud
from schema import AgendaSchema, PaginateSchema, AgendaCreateSchema,\
    AgendaUpdateSchema, GenericMsgSchema, AgendaCompleteSchema

agenda_blp = Blueprint("Agendas",
                       __name__,
                       url_prefix="/agendas",
                       description="Operations on Agendas")


@agenda_blp.route("/")
class AgendaCreateGet(MethodView):
    @jwt_required
    @agenda_blp.arguments(PaginateSchema)
    @agenda_blp.response(AgendaSchema(many=True))
    def get(self, new_data):
        """[Admin] Reveal all agendas in the system - [PROTECTED]

        Args:
            Skip (int): number of entries to skip
            [defaults to '0' if not provided],
            Limit (int): the limit of number of data released
            [defaults to '100' if not provided]
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        if not user.is_superuser:
            abort(401,
                  message="You do not have permission to view this endpoint")
        if 'limit' in new_data and 'skip' in new_data:
            agendas = agenda_crud.get_multi(skip=new_data['skip'],
                                            limit=new_data['limit'])
        elif 'limit' in new_data:
            agendas = agenda_crud.get_multi(limit=new_data['limit'])
        elif 'skip' in new_data:
            agendas = agenda_crud.get_multi(skip=new_data['skip'])
        else:
            agendas = agenda_crud.get_multi()

        return agendas

    @jwt_required
    @agenda_blp.arguments(AgendaCreateSchema)
    @agenda_blp.response(AgendaCreateSchema)
    def post(self, new_data):
        """Create a new Agenda - [PROTECTED]

        Args:
            new_data ([type]): [description]
        """

        user_id = get_jwt_identity()
        meeting = meeting_crud.get(new_data['meeting_id'])
        if not meeting_crud.is_user_meeting(user_id=user_id, meeting=meeting):
            abort(401,
                  message="You don't have permission to add agenda to meeting")
        if not meeting:
            abort(404, message="Meeting does not exist")

        if meeting_crud.is_meeting_started(meeting):
            abort(409, message="Can not add agenda to an ungoing meeting")

        agenda = agenda_crud.create(new_data)
        if not agenda['added']:
            abort(409, message="Agenda with same name exits in this meeting")
        agenda = agenda['db_obj']
        meeting_crud.update_meeting_endtime(new_data['meeting_id'],
                                            agenda.set_duration)
        return agenda


@agenda_blp.route("/<agenda_id>")
class AgendaUpdateGetDelete(MethodView):
    @jwt_required
    @agenda_blp.arguments(AgendaUpdateSchema)
    @agenda_blp.response(AgendaUpdateSchema)
    def put(self, new_data, agenda_id):
        """Update an Agenda [Protected]

        Args:
            new_data ([type]): [description]
            agenda_id (int): The Agenda id

        Only send what has changed
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        agenda = agenda_crud.get(agenda_id)
        set_duration = agenda.set_duration
        meeting_id = agenda_crud.get_meeting_id(agenda=agenda)
        meeting = meeting_crud.get(meeting_id)
        if not user.is_superuser:
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(
                    401,
                    message="You don't have permission to update this agenda")
        if not agenda:
            abort(404, message="Agenda does not exist")

        if meeting_crud.is_meeting_started(meeting):
            abort(409, message="Can't update an agenda in an ungoing meeting")

        new_agenda = agenda_crud.update(agenda, new_data)
        if not new_agenda['added']:
            abort(409, message="Agenda with same name exits in this meeting")
        new_agenda = new_agenda['db_obj']

        if new_data['set_duration']:
            data = {
                "set_duration": ((meeting.set_duration - set_duration) +
                                 new_agenda.set_duration),
                "set_end_time":
                time_plus(time_subtract(meeting.set_end_time, set_duration),
                          new_agenda.set_duration)
            }

            meeting_crud.update(meeting, data)

        return new_agenda

    @jwt_required
    @agenda_blp.response(AgendaSchema)
    def get(self, agenda_id):
        """Get an Agenda [Protected]

        Args:
            new_data ([type]): [description]
            agenda_id (int): The Agenda id
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        agenda = agenda_crud.get(agenda_id)
        if not agenda:
            abort(404, message="Agenda does not exist")
        if not user.is_superuser:
            meeting_id = agenda_crud.get_meeting_id(agenda=agenda)
            meeting = meeting_crud.get(meeting_id)
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(401,
                      message="You don't have permission to view this agenda")
        return agenda

    @jwt_required
    @agenda_blp.response(GenericMsgSchema, code=202)
    def delete(self, agenda_id):
        """Delete an Agenda [Protected]

        Args:
            new_data ([type]): [description]
            agenda_id (int): The Agenda id
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        agenda = agenda_crud.get(agenda_id)
        if not agenda:
            abort(404, message="Agenda does not exist")
        meeting_id = agenda_crud.get_meeting_id(agenda=agenda)
        if not user.is_superuser:
            meeting_id = agenda_crud.get_meeting_id(agenda=agenda)
            meeting = meeting_crud.get(meeting_id)
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(
                    401,
                    message="You don't have permission to remove this agenda")
        meeting_crud.update_meeting_endtime(meeting_id, -(agenda.set_duration))
        agenda_crud.remove(agenda_id)
        return {'msg': 'Agenda Removed'}


@agenda_blp.route("/<agenda_id>/complete")
class AgendaComplete(MethodView):
    @jwt_required
    @agenda_blp.arguments(AgendaCompleteSchema)
    @agenda_blp.response(AgendaSchema)
    def put(self, new_data, agenda_id):
        """Marks an Agenda as Completeted

        Args:
            new_data ([type]): [description]
            agenda_id (int): The agenda unique id

        Returns:
            Agenda: an agenda object
        """
        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        agenda = agenda_crud.get(agenda_id)
        meeting_id = agenda_crud.get_meeting_id(agenda=agenda)
        if not user.is_superuser:
            meeting = meeting_crud.get(meeting_id)
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(
                    401,
                    message="You don't have permission to complete this agenda"
                )
        _meeting = meeting_crud.get(meeting_id)
        if not meeting_crud.is_meeting_started(_meeting):
            abort(409, message="Start the meeting first")
        if agenda.completed:
            abort(409, message="Agenda Already Completed")
        agenda = agenda_crud.completed(agenda, new_data['final_duration'])
        meeting_crud.update_meeting_final_endtime(_meeting,
                                                  new_data['final_duration'])
        if agenda_crud.is_all_agenda_completed(meeting_id=meeting_id):
            meeting_crud.completed(meeting_id=meeting_id)
        return agenda
