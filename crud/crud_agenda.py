from typing import Any, Dict, List

from crud.base import CRUDBase
from models.agenda import Agenda, db


class CRUDAgenda(CRUDBase[Agenda]):
    def create_with_meeting_id(self, obj_in: Dict[str, Any],
                               meeting_id: int) -> Agenda:
        db_obj = self.model(**obj_in, meeting_id=meeting_id)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def get_multi_by_meeting(self,
                             meeting_id: int,
                             skip: int = 0,
                             limit: int = 100) -> List[Agenda]:
        return (self.model.filter(
            meeting_id=meeting_id).offset(skip).limit(limit).all())


agenda = CRUDAgenda(Agenda)
