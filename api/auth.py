from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    jwt_required,
)

from crud import user as user_crud, auth as auth_crud
from core.factory import jwt
from core.security import verify_password
from schema import (UserRegSchema, UserLoginSchema, TokenSchema,
                    RefreshTokenSchema, AuthTokenSchema, TokenBlacklistSchema,
                    GenericMsgSchema, ChgPasswordSchma)

auth_blp = Blueprint("Auth",
                     __name__,
                     url_prefix="/auth",
                     description="Authentication Operations")


# Defined a callback function to check if a token has been revoked or not
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return auth_crud.is_token_revoked(decoded_token)


@auth_blp.route("/register")
class UserRegister(MethodView):
    @auth_blp.arguments(UserRegSchema)
    @auth_blp.response(UserRegSchema, code=201)
    def post(self, new_data):
        """Register New Users

        Args:
            new_data (dict): the data gotten after deserilaization
        """

        user = user_crud.get_by_email(new_data["email"])
        if user:
            abort(
                409,
                message="A user with this email already exists in the system")
        user = user_crud.create(new_data)
        return user


@auth_blp.route("/login")
class UserLogin(MethodView):
    @auth_blp.arguments(UserLoginSchema)
    @auth_blp.response(TokenSchema, code=200)
    def post(self, new_data):
        """User Login

        Args:
            new_data (dict): the data gotten after deserilaization
        """

        user = user_crud.authenticate(email=new_data['email'],
                                      password=new_data['password'])
        if not user:
            abort(401, message="Wrong email address or password")
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        auth_crud.add_token_to_database(access_token, 'sub')
        auth_crud.add_token_to_database(refresh_token, 'sub')

        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }
        return data


@auth_blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_refresh_token_required
    @auth_blp.arguments(AuthTokenSchema, location='headers')
    @auth_blp.response(RefreshTokenSchema, code=200)
    def post(self, new_data):
        """Create Access Token using Refresh Token

        Args:
            new_data (dict): the data gotten after deserilaization
        """

        current_user = get_jwt_identity()
        access_token = create_access_token(current_user)

        auth_crud.add_token_to_database(access_token, 'sub')

        data = {'access_token': access_token, 'token_type': 'Bearer'}
        return data


@auth_blp.route("/token")
class GetTokens(MethodView):
    @jwt_required
    @auth_blp.arguments(AuthTokenSchema, location='headers')
    @auth_blp.response(TokenBlacklistSchema(many=True), code=200)
    def get(self, new_data):
        """View Tokens

        Args:
            new_data (dict): the data gotten after deserilaization
        """

        current_user = get_jwt_identity()
        all_tokens = auth_crud.get_user_tokens(current_user)
        tokens = [token.to_dict() for token in all_tokens]
        return tokens


@auth_blp.route("/token/<token_id>/")
class RevokeTokens(MethodView):
    @jwt_required
    @auth_blp.arguments(AuthTokenSchema, location='headers')
    @auth_blp.response(GenericMsgSchema, code=200)
    def put(self, new_data, token_id):
        """Revoke User token

        Args:
            token_id (int): The token id
        """

        current_user = get_jwt_identity()
        revoked = auth_crud.revoke_token(token_id, current_user)
        if not revoked:
            abort(404, message="Token Not Found")
        return {'msg': 'Token revoked'}


@auth_blp.route("/changepassword/me/")
class UpdatePassword(MethodView):
    @jwt_required
    @auth_blp.arguments(ChgPasswordSchma)
    @auth_blp.response(GenericMsgSchema, code=200)
    def put(self, new_data):
        """Password Change [PROTECTED]

        Args:
            old_passowrd (str): [The current password]
            new_password (int): [The new password]
        """

        current_user = get_jwt_identity()
        user = user_crud.get(current_user)
        if not user:
            abort(404, message="User not Found")

        verified = verify_password(new_data['old_password'],
                                   user.hashed_password)
        if not verified:
            abort(401, message='Wrong old Password')

        data = {'password': new_data['new_password']}
        user_crud.update(user, data)

        return {'msg': 'Password Changed'}
