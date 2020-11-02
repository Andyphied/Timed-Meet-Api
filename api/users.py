from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from crud import user as user_crud, auth as auth_crud
from schema import UserRegSchema, PaginateSchema, AuthTokenSchema,\
    UserUpdateSchema, GenericMsgSchema

# from app.models import User

user_blp = Blueprint("Users",
                     __name__,
                     url_prefix="/users",
                     description="Operations on Users")


@user_blp.route("/")
class UserCreateGet(MethodView):
    @jwt_required
    @user_blp.arguments(PaginateSchema)
    @user_blp.response(UserRegSchema(many=True))
    def get(self, new_data):
        """[Admin] Reveal of users in the system - [PROTECTED]

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
            users = user_crud.get_multi(skip=new_data['skip'],
                                        limit=new_data['limit'])
        elif 'limit' in new_data:
            users = user_crud.get_multi(limit=new_data['limit'])
        elif 'skip' in new_data:
            users = user_crud.get_multi(skip=new_data['skip'])
        else:
            users = user_crud.get_multi()

        return users


@user_blp.route("/me/")
class MyUserDetails(MethodView):
    @jwt_required
    @user_blp.response(UserRegSchema())
    def get(self):
        """Reveal a user own detail - [PROTECTED]
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        if not user:
            abort(404, message="User not Found")

        return user

    @jwt_required
    @user_blp.arguments(UserUpdateSchema)
    @user_blp.response(UserRegSchema(), code=201)
    def put(self, new_data):
        """Update a user own details - [PROTECTED]
        Only send what has changed
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        if not user:
            abort(404, message="User not Found")
        user = user_crud.update(user, new_data)
        if not user['added']:
            abort(409, message="User with this email exits")
        user = user['db_obj']
        return user

    @jwt_required
    @user_blp.response(GenericMsgSchema, code=202)
    def delete(self):
        """Delete a user own details - [PROTECTED]
        """

        user_id = get_jwt_identity()
        user = user_crud.get(user_id)
        if not user:
            abort(404, message="User not Found")
        all_tokens = auth_crud.get_user_tokens(user_id)
        tokens = [token.to_dict() for token in all_tokens]
        for token in tokens:
            auth_crud.revoke_token(token['id'], user_id)
        user = user_crud.remove(user_id)

        return {'msg': 'User Removed'}


@user_blp.route("/<user_id>/")
class UserById(MethodView):
    @jwt_required
    @user_blp.arguments(AuthTokenSchema, location='headers')
    @user_blp.response(UserRegSchema())
    def get(self, new_data, user_id):
        """Reveal another user detail - [PROTECTED]

        Args:
            user_id (int): [The User id]
        """

        request_id = get_jwt_identity()
        user = user_crud.get(request_id)
        if not user.is_superuser:
            abort(401,
                  message="You do not have permission to view this endpoint")
        user = user_crud.get(user_id)

        return user

    @jwt_required
    @user_blp.arguments(UserUpdateSchema)
    @user_blp.response(UserRegSchema())
    def put(self, new_data, user_id):
        """[Admin] Update another user detail - [PROTECTED]

        Args:
            user_id (int): [The User id]

        Only send what has changed
        """

        request_id = get_jwt_identity()
        user = user_crud.get(request_id)
        if not user.is_superuser:
            abort(401,
                  message="You do not have permission to view this endpoint")
        user = user_crud.get(user_id)
        user = user_crud.update(user, new_data)
        if not user['added']:
            abort(409, message="User with this email exist")
        user = user['db_obj']
        return user

    @jwt_required
    @user_blp.arguments(AuthTokenSchema, location='headers')
    @user_blp.response(GenericMsgSchema, code=202)
    def delete(self, new_data, user_id):
        """[ADMIN] Deletes another user from the system [PROTECTED]

        Args:
            user_id (int): [The User id]

        Returns:
            msg: [if it was sucessful or not]
        """
        print(new_data)
        request_id = get_jwt_identity()
        user = user_crud.get(request_id)
        if not user.is_superuser:
            abort(401,
                  message="You do not have permission to view this endpoint")
        all_tokens = auth_crud.get_user_tokens(user_id)
        tokens = [token.to_dict() for token in all_tokens]
        for token in tokens:
            auth_crud.revoke_token(token['id'], user_id)
        user = user_crud.remove(user_id)

        return {'msg': 'User Removed'}
