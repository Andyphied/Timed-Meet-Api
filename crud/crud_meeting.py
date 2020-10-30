from typing import Any, Dict, List
from datetime import date
from crud.base import CRUDBase
from models.meeting import Meeting, db


class CRUDMeeting(CRUDBase[Meeting]):
    def create_with_owner(self, obj_in: Dict[str, Any],
                          user_id: int) -> Meeting:
        db_obj = self.model(**obj_in, user_id=user_id)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self,
                           user_id: int,
                           skip: int = 0,
                           limit: int = 100) -> List[Meeting]:
        return (self.model.filter(
            user_id=user_id).offset(skip).limit(limit).all())

    def get_today_meetings(self,
                           user_id: int,
                           _date: date,
                           skip: int = 0,
                           limit: int = 100) -> List[Meeting]:
        return (self.model.filter(
            meeting_date=_date).offset(skip).limit(limit).all())


meeting = CRUDMeeting(Meeting)
