from typing import Any, Dict, List
from datetime import date, timedelta
from crud.base import CRUDBase
from models.meeting import Meeting, db


class CRUDMeeting(CRUDBase[Meeting]):
    def create_with_owner(self, obj_in: Dict[str, Any],
                          user_id: int) -> Meeting:
        db_obj = Meeting(**obj_in, user_id=user_id)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self,
                           user_id: int,
                           skip: int = 0,
                           limit: int = 100) -> List[Meeting]:
        return (Meeting.query.filter(
            user_id=user_id).offset(skip).limit(limit).all())

    def get_today_meetings(self,
                           user_id: int,
                           skip: int = 0,
                           limit: int = 100) -> List[Meeting]:
        return (Meeting.query.filter(
            meeting_date=date.today()).offset(skip).limit(limit).all())

    def is_user_meeting(self, user_id: int, meeting_id: int) -> bool:
        meeting = Meeting.query.get(meeting_id)
        if meeting.user_id == user_id:
            return True
        return False

    def is_meeting_started(self, meeting: Meeting) -> bool:
        if not meeting.final_start_time:
            return False
        return True

    def update_meeting_final_endtime(self, meeting: Meeting,
                                     interval: timedelta) -> Meeting:
        data = {
            "final_duration": (meeting.final_duration + interval),
            "final_end_time": (meeting.final_start_time + interval)
        }
        meeting = self.update(meeting, data)
        return meeting

    def update_meeting_endtime(self, meeting_id: int,
                               interval: timedelta) -> Meeting:
        meeting = self.get(meeting_id)
        data = {
            "set_duration": (meeting.set_duration + interval),
            "set_end_time": (meeting.set_start_time + interval)
        }
        meeting = self.update(meeting, data)
        return meeting

    def completed(self, meeting_id: int) -> Meeting:
        """Help mark an meeting as completed

        Args:
            agenda (Meeting): The meeting model object

        Returns:
            Agenda: The updated meeting object
        """
        db_obj = self.get(meeting_id)
        db_obj.completed = True
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)


meeting = CRUDMeeting(Meeting)
