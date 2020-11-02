from typing import List, Any, Dict
from datetime import timedelta
from crud.base import CRUDBase, db
from models.agenda import Agenda


class CRUDAgenda(CRUDBase[Agenda]):
    def get_multi_by_meeting(self,
                             meeting_id: int,
                             skip: int = 0,
                             limit: int = 100) -> List[Agenda]:
        """Help get all agendas  under a meeting

        Args:
            meeting_id (int): The meeting unique id
            skip (int, optional): number of entries to skip. Defaults to 0.
            limit (int, optional): limit no of objects. Defaults to 100.

        Returns:
            List[Agenda]: The list of Agenda Object
        """
        return (Agenda.query.filter(
            meeting_id == meeting_id).offset(skip).limit(limit).all())

    def get_meeting_id(self, agenda: Agenda) -> int:
        """
        help get meeting_id
        """
        meeting_id = agenda.meeting_id
        return meeting_id

    def completed(self, db_obj: Agenda, duration: timedelta) -> Agenda:
        """Help mark an agenda as completed

        Args:
            agenda (Agenda): The agenda model object

        Returns:
            Agenda: [The updated agenda object
        """

        db_obj.completed = True
        db_obj.final_duration = duration
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def is_all_agenda_completed(self, meeting_id: int) -> bool:
        """Checks if all the agendas in meeting has sbeen completed

        Args:
            meeting_id (int): The meeting unique id

        Returns:
            bool: True or False
        """
        meetings = self.get_multi_by_meeting(meeting_id=meeting_id)
        status_set = {x.completed for x in meetings}
        return all(status_set)

    def remove_all(self, agendas: List[Agenda]) -> Dict[str, Any]:
        """Delete all agendas passed through

        Args:
            agendas (List[Meeting]): The List of agendas

        Returns:
            Dict[str, Any]: sucess message
        """
        for agenda in agendas:
            agenda_id = agenda.id
            self.remove(agenda_id)
        return {'deleted': True}


agenda = CRUDAgenda(Agenda)
