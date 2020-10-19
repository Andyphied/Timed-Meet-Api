from typing import Any, Dict, Optional

from crud.base import CRUDBase
from models.users import User, db
from core.security import verify_password, get_password_hash


class CRUDUser(CRUDBase[User]):
    def get_by_email(self, email: str) -> Optional[User]:
        """Gets user by email

        Args:
            email (str): [user email address]

        Returns:
            Optional[User]: [The User Sqlalchemy Object]
        """
        return User.query.filter(User.email == email).first()

    def create(self, obj_in: Dict[str, Any]) -> User:
        """Creates a new users and also ensures the user password is hashed

        Args:
            obj_in (Dict[str, Any]): The dict object holding the user details

        Returns:
            User: The User Sqlalchemy Object
        """
        db_obj = User(
            email=obj_in["email"],
            hashed_password=get_password_hash(obj_in["password"]),
            full_name=obj_in["full_name"],
            is_superuser=obj_in["is_superuser"],
        )
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def update(self, db_obj: User, obj_in: Dict[str, Any]) -> User:

        if "password" in obj_in:
            hashed_password = get_password_hash(obj_in["password"])
            del obj_in["password"]
            obj_in["hashed_password"] = hashed_password
        return super().update(db_obj=db_obj, obj_in=obj_in)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_active(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
