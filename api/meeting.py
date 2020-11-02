from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from crud import user as user_crud, meeting as meeting_crud
from schema import MeetingSchema, PaginateSchema, MeetingSchemaAdmin,\
    MeetingCreateSchema, MeetingSchemaUser, GenericMsgSchema, AgendaSchema,\
    StartMeetingSchema, EndMeetingSchema

meeting_blp = Blueprint("Meetings",
                        __name__,
                        url_prefix="/meetings",
                        description="Operations on Meetings")


@meeting_blp.route("/")
class MeetingCreateGet(MethodView):
    @jwt_required
    @meeting_blp.arguments(PaginateSchema)
    @meeting_blp.response(MeetingSchemaAdmin(many=True))
    def get(self, new_data):
        """[Admin] Reveal all Meetings in the system - [PROTECTED]

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
            meetings = meeting_crud.get_multi(skip=new_data['skip'],
                                              limit=new_data['limit'])
        elif 'limit' in new_data:
            meetings = meeting_crud.get_multi(limit=new_data['limit'])
        elif 'skip' in new_data:
            meetings = meeting_crud.get_multi(skip=new_data['skip'])
        else:
            meetings = meeting_crud.get_multi()

        return meetings

    @jwt_required
    @meeting_blp.arguments(MeetingCreateSchema)
    @meeting_blp.response(MeetingCreateSchema)
    def post(self, new_data):
        """Create a New Meeting - [PROTECTED]

        Args:
            new_data ([type]): [description]
        """

        user_id = get_jwt_identity()
        meeting = meeting_crud.create_with_owner(new_data, user_id=user_id)
        if not meeting['added']:
            abort(409, message="Meeting with this name exits for this user")
        meeting = meeting['db_obj']
        return meeting


@meeting_blp.route("/<meeting_id>")
class MeetingUpdateGetDelete(MethodView):
    @jwt_required
    @meeting_blp.arguments(MeetingSchema)
    @meeting_blp.response(MeetingSchema)
    def put(self, new_data, meeting_id):
        """Update a Meeting [Protected]

        Args:
            new_data ([type]): [description]
            meeting_id (int): The Meeting id

        Only send what has changed
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        meeting = meeting_crud.get(meeting_id)
        if not user.is_superuser:
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(
                    401,
                    message="You don't have permission to update this Meeting")
        if not meeting:
            abort(404, message="Meeting does not exist")

        meeting = meeting_crud.get(meeting_id)
        meeting = meeting_crud.update(meeting, new_data)
        if not meeting['added']:
            abort(409, message="Meeting with this name exits for this user")
        meeting = meeting['db_obj']

        return meeting

    @jwt_required
    @meeting_blp.response(MeetingSchemaUser)
    def get(self, meeting_id):
        """Get a Meeting [Protected]

        Args:
            new_data ([type]): [description]
            meeting_id (int): The Meeting id
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        meeting = meeting_crud.get(meeting_id)
        if not user.is_superuser:
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(401,
                      message="You don't have permission to view this Meeting")
        if not meeting:
            abort(404, message="Meeting does not exist")

        return meeting

    @jwt_required
    @meeting_blp.response(GenericMsgSchema, code=202)
    def delete(self, meeting_id):
        """Delete a Meeting [Protected]

        Args:
            new_data ([type]): [description]
            meeting_id (int): The Meeting id
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        meeting = meeting_crud.get(meeting_id)
        if not user.is_superuser:
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(
                    401,
                    message="You don't have permission to remove this Meeting")
        if not meeting:
            abort(404, message="Meeting does not exist")

        meeting_crud.remove(meeting_id)
        return {'msg': 'User Removed'}


@meeting_blp.route("/me")
class MyMeeting(MethodView):
    @jwt_required
    @meeting_blp.arguments(PaginateSchema)
    @meeting_blp.response(MeetingSchema(many=True))
    def get(self, new_data):
        """Get My Meetings [PROTECTED]
        """
        user_id = get_jwt_identity()

        if 'limit' in new_data and 'skip' in new_data:
            meetings = meeting_crud.get_multi_by_owner(user_id=user_id,
                                                       skip=new_data['skip'],
                                                       limit=new_data['limit'])
        elif 'limit' in new_data:
            meetings = meeting_crud.get_multi_by_owner(user_id=user_id,
                                                       limit=new_data['limit'])
        elif 'skip' in new_data:
            meetings = meeting_crud.get_multi_by_owner(user_id=user_id,
                                                       skip=new_data['skip'])
        else:
            meetings = meeting_crud.get_multi_by_owner(user_id=user_id)

        return meetings


@meeting_blp.route("/me/today")
class MyMeetingSToday(MethodView):
    @jwt_required
    @meeting_blp.response(MeetingSchema(many=True))
    def get(self):
        """Get Today's Meeting for a User [PROTECTED]
        """
        user_id = get_jwt_identity()
        meetings = meeting_crud.get_today_meetings(user_id=user_id)
        return meetings


@meeting_blp.route("/<meeting_id>/agendas")
class MeetingAgendas(MethodView):
    @jwt_required
    @meeting_blp.response(AgendaSchema(many=True))
    def get(self, meeting_id: int):
        """Get  A Meeting Agenda(s) [Protected]
        """
        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        meeting = meeting_crud.get(meeting_id)
        if not user.is_superuser:
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(401, message="You don't have permission to get agendas")
        if not meeting:
            abort(404, message="Meeting does not exist")

        agendas = meeting_crud.get_meeting_agendas(meeting=meeting)

        return agendas


@meeting_blp.route("/start")
class StartMeeting(MethodView):
    @jwt_required
    @meeting_blp.arguments(StartMeetingSchema)
    @meeting_blp.response(MeetingSchemaUser)
    def post(self, new_data):
        """Start A Meeting [Protected]

        Args:
            new_data ([type]): [description]

        Returns:
            [type]: [description]
        """
        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        meeting_id = new_data['meeting_id']
        meeting = meeting_crud.get(meeting_id)
        if not user.is_superuser:
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(
                    401,
                    message="You don't have permission to start this meeting")
        if not meeting:
            abort(404, message="Meeting does not exist")

        if meeting_crud.is_meeting_started(meeting):
            abort(409, message="You already started the meeting")
        meeting = meeting_crud.start_meeting(new_data)
        return meeting


@meeting_blp.route("/end")
class EndMeeting(MethodView):
    @jwt_required
    @meeting_blp.arguments(EndMeetingSchema)
    @meeting_blp.response(MeetingSchemaUser)
    def post(self, new_data):
        """End A Meeting [Protected]

        Args:
            new_data ([type]): [description]

        Returns:
            [type]: [description]
        """
        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        meeting_id = new_data['meeting_id']
        meeting = meeting_crud.get(meeting_id)
        if not user.is_superuser:
            if not meeting_crud.is_user_meeting(user_id=user_id,
                                                meeting=meeting):
                abort(401, message="You don't have permission to get agendas")
        if not meeting:
            abort(404, message="Meeting does not exist")

        if not meeting_crud.is_meeting_started(meeting):
            abort(409, message="This meeting has not started")

        if meeting.completed:
            abort(409, message="This meeting has ended")

        meeting = meeting_crud.end_meeting(meeting_id, new_data['end_time'])
        return meeting
