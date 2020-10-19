from typing import Any
from datetime import datetime

from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound

from crud.base import CRUDBase
from models.auth import TokenBlacklist, db


class CRUDAuth(CRUDBase[TokenBlacklist]):
    def _epoch_utc_to_datetime(self, epoch_utc: Any) -> datetime:
        """
        Helper function for converting epoch timestamps (as stored in JWTs)
        into python datetime objects (which are easier to use with sqlalchemy).
        """
        return datetime.fromtimestamp(epoch_utc)

    def add_token_to_database(self, encoded_token: str,
                              identity_claim: str) -> bool:
        """
        Adds a new token to the database. It is not revoked when it is added.
        :param identity_claim:
        """
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        token_type = decoded_token['type']
        user_identity = decoded_token[identity_claim]
        expires = self._epoch_utc_to_datetime(decoded_token['exp'])
        revoked = False

        db_token = TokenBlacklist(
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires=expires,
            revoked=revoked,
        )
        db.session.add(db_token)
        db.session.commit()
        return True

    def is_token_revoked(self, decoded_token) -> bool:
        """
        Checks if the given token is revoked or not. Because we are adding all
        the tokens that we create into this database, if the token is not
        present in the database we are going to consider it revoked, as we
        don't know where it was created.
        """
        jti = decoded_token['jti']
        try:
            token = TokenBlacklist.query.filter_by(jti=jti).one()
            return token.revoked
        except NoResultFound:
            return True

    def revoke_token(self, token_id: int, user: str) -> bool:
        """
        Revokes the given token. Returns False if the token does
        not exist in the database and True if it does
        """
        try:
            token = TokenBlacklist.query.filter_by(id=token_id,
                                                   user_identity=user).one()
            token.revoked = True
            db.session.commit()
            return True
        except NoResultFound:
            return False

    def unrevoke_token(self, token_id: int, user: str) -> bool:
        """
        Unrevokes the given token. Returns False if the token does
        not exist in the database and True if it does
        """
        try:
            token = TokenBlacklist.query.filter_by(id=token_id,
                                                   user_identity=user).one()
            token.revoked = False
            db.session.commit()
            return True
        except NoResultFound:
            return False

    def prune_database(self) -> bool:
        """
        Delete tokens that have expired from the database.
        How (and if) you call this is entirely up you. You could expose it to
        an endpoint that only administrators could call, you could run it as a
        cron, set it up with flask cli, etc.
        """
        now = datetime.now()
        expired = TokenBlacklist.query.filter(
            TokenBlacklist.expires < now).all()
        for token in expired:
            db.session.delete(token)
        db.session.commit()
        return True

    def get_user_tokens(self, user_identity: str):
        """
        Returns all of the tokens, revoked and unrevoked, that are stored for
        the given user
        """
        return TokenBlacklist.query.filter_by(
            user_identity=user_identity).all()


auth = CRUDAuth(TokenBlacklist)
