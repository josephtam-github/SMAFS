from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, \
    get_jwt_identity, get_jwt
from ..models.user import User
from ..models.blocklist import TokenBlocklist
from ..models.schema import UserSchema, LoginQueryArgsSchema
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from datetime import datetime, timezone
from ..utils.matriculator import matric


auth = Blueprint(
    'Auth',
    __name__,
    url_prefix='/auth',
    description='Authentication for user registration and login with JWT token'
)


@auth.route('/register')
class Register(MethodView):
    @auth.arguments(UserSchema)
    @auth.response(HTTPStatus.CREATED, UserSchema, description='Returns an object containing created user detail')
    def post(self, new_data):
        """Register a new user

        Returns the new user info from the database
        """
        # Sets first user's role to admin
        last_user = User.query.order_by(User.user_id.desc()).first()
        if last_user:
            category = 'STUDENT'
            matric_no = matric(int(last_user.user_id) + 1)
            email_exist = User.query.filter_by(email=new_data['email']).first()
            if email_exist:
                abort(HTTPStatus.NOT_ACCEPTABLE, message='This email already exists')
        else:
            category = 'ADMIN'
            matric_no = 'A2023/001'

        new_user = User(
            firstname=new_data['firstname'],
            lastname=new_data['lastname'],
            email=new_data['email'],
            password_hash=generate_password_hash(new_data['password']),
            category=category,
            matric_no=matric_no
        )
        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth.route('/login')
class Login(MethodView):
    @auth.arguments(LoginQueryArgsSchema)
    @auth.response(HTTPStatus.ACCEPTED, LoginQueryArgsSchema, description='Returns the access and return tokens')
    def post(self, login_data):
        """Logs in user

        Returns access and refresh tokens
        """

        if 'email' in login_data.keys():
            email = login_data['email']
            user = User.query.filter_by(email=email).first()

        elif 'matric_no' in login_data.keys():
            matric_no = login_data['matric_no']
            user = User.query.filter_by(matric_no=matric_no).first()
        else:
            abort(HTTPStatus.BAD_REQUEST, message='You must input either your matriculation number or your email '
                                                  'along with your password')
        password = login_data['password']

        if (user is not None) and check_password_hash(user.password_hash, password):
            additional_claims = {"category": user.category}
            access_token = create_access_token(identity=user.user_id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.user_id, additional_claims=additional_claims)
            response = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return jsonify(response), HTTPStatus.ACCEPTED
        else:
            abort(HTTPStatus.UNAUTHORIZED, message='Invalid credentials')


@auth.route('/logout')
class Logout(MethodView):
    @auth.response(HTTPStatus.OK, description='Returns success message')
    @jwt_required()
    def delete(self):
        """Log the User Out

        Returns success message
        """
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        blocked_token = TokenBlocklist(jti=jti, created_at=now)
        blocked_token.save()
        return {"message": "Logout successful"}, HTTPStatus.OK


@auth.route('/refresh')
class Refresh(MethodView):
    @auth.response(HTTPStatus.OK, description='Returns a new access token')
    @jwt_required(refresh=True)
    def post(self):
        """Generate Refresh Token

        Returns new access token
        """
        user_id = get_jwt_identity()
        claims = get_jwt()
        access_token = create_access_token(identity=user_id, additional_claims=claims)
        return jsonify({'access_token': access_token}), HTTPStatus.OK

