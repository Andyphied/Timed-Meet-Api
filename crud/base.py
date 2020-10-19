from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from models import db, Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update,
        Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, id: Any) -> Optional[ModelType]:
        return self.model.query.filter(self.model.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.model.query.offset(skip).limit(limit).all()

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_in)
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def update(
        self,
        db_obj: ModelType,
        obj_in: Dict[str, Any],
    ) -> ModelType:

        for field in obj_in:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def remove(self, id: int) -> ModelType:
        obj = self.model.query.get(id)
        db.session.delete(obj)
        db.session.commit()
        return obj
