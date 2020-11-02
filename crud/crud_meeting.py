from typing import Any, Dict, List
from datetime import date, timedelta, time
from sqlalchemy.exc import IntegrityError

from crud.base import CRUDBase
from models.meeting import Meeting, db
from models.agenda import Agenda
from utils.utils import time_plus
from .crud_agenda import agenda as crud_agenda


class CRUDMeeting(CRUDBase[Meeting]):
    def create_with_owner(self, obj_in: Dict[str, Any],
                          user_id: int) -> Dict[str, Any]:
        db_obj = Meeting(**obj_in, user_id=user_id)
        db.session.add(db_obj)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'added': False}
        db.session.refresh(db_obj)
        return {'added': True, 'db_obj': db_obj}

    def get_multi_by_owner(self,
                           user_id: int,
                           skip: int = 0,
                           limit: int = 100) -> List[Meeting]:
        return (Meeting.query.filter(Meeting.user_id == user_id).order_by(
            'meeting_date').offset(skip).limit(limit).all())

    def get_today_meetings(self, user_id: int) -> List[Meeting]:
        return (Meeting.query.filter(user_id == user_id).filter(
            Meeting.meeting_date == date.today()).order_by('created_on').all())

    def is_user_meeting(self, user_id: int, meeting: Meeting) -> bool:
        if meeting.user_id == user_id:
            return True
        return False

    def is_meeting_started(self, meeting: Meeting) -> bool:
        if not meeting.final_start_time:
            return False
        return True

    def update_meeting_final_endtime(self, meeting: Meeting,
                                     interval: timedelta) -> Meeting:
        if meeting.final_end_time:
            data = {
                "final_duration": (meeting.final_duration + interval),
                "final_end_time": time_plus(meeting.final_end_time, interval)
            }
        else:
            data = {
                "final_duration": (meeting.final_duration + interval),
                "final_end_time": time_plus(meeting.final_start_time, interval)
            }
        meeting = self.update(meeting, data)
        return meeting

    def update_meeting_endtime(self, meeting_id: int,
                               interval: timedelta) -> Meeting:
        meeting = self.get(meeting_id)
        data = {
            "set_duration": (meeting.set_duration + interval),
            "set_end_time": time_plus(meeting.set_start_time, interval)
        }
        meeting = self.update(meeting, data)
        return meeting

    def end_meeting(self, meeting_id: int, end_time: time) -> Meeting:
        """Help mark an meeting as completed

        Args:
            agenda (Meeting): The meeting model object

        Returns:
            Agenda: The updated meeting object
        """
        db_obj = self.get(meeting_id)
        db_obj.completed = True
        db_obj.final_end_time = end_time
        db_obj.final_duration = end_time - db_obj.final_start_time
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def get_meeting_agendas(self, meeting: Meeting) -> List[Agenda]:
        """Get meeting agendas

        Args:
            meeting (Meeting): The meeting object

        Returns:
            Meeting: [description]
        """

        meeting = meeting.agendas
        return meeting

    def start_meeting(self, data: Dict[str, Any]) -> Meeting:
        """Start Meeting

        Args:
            start_time (time): Actual meeting start time
            meeting_id (int): the meeting unique id

        Returns:
            Meeting: Meeting status
        """
        db_obj = self.get(data['meeting_id'])
        db_obj.final_start_time = data['start_time']
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def remove(self, id: int) -> Meeting:
        """Delete a meeting and all agendas under it

        Args:
            id (int): meeting id

        Returns:
            Meeting: Meeting object
        """
        meeting = self.get(id=id)
        agendas = meeting.agendas
        crud_agenda.remove_all(agendas=agendas)
        return super().remove(id=id)

    def remove_all(self, meetings: List[Meeting]) -> Dict[str, Any]:
        """Delete all meetings passed through

        Args:
            agendas (List[Meeting]): The List of meetings

        Returns:
            Dict[str, Any]: sucess message
        """
        for meeting in meetings:
            meeting_id = meeting.id
            self.remove(meeting_id)
        return {'deleted': True}


meeting = CRUDMeeting(Meeting)
