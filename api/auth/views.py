from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies, decode_token
from ..models.user import User
from ..models.schema import UserSchema, LoginQueryArgsSchema
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from api import db

auth = Blueprint(
    'Auth',
    __name__,
    url_prefix='/auth',
    description='Authentication for user registration and login with JWT token'
)


@auth.route('/signup')
class Register(MethodView):
    @auth.arguments(UserSchema)
    @auth.response(HTTPStatus.OK, UserSchema, description='Returns an object containing ')
    def post(self, new_data):
        """Register a new user"""

        new_user = User(
            firstname=new_data['firstname'],
            lastname=new_data['lastname'],
            email=new_data['email'],
            password_hash=generate_password_hash(new_data['password'])
        )
        new_user.save()

        return new_user, HTTPStatus.OK


@auth.route('/login')
class Login(MethodView):
    @auth.arguments(LoginQueryArgsSchema)
    @auth.response(HTTPStatus.CREATED, LoginQueryArgsSchema, description='Returns the access and return tokens')
    def post(self, login_data):
        """Logs in user"""

        email = login_data['email']
        password = login_data['password']

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)
            response = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return jsonify(response), HTTPStatus.CREATED
        else:
            abort(HTTPStatus.UNAUTHORIZED, message='Invalid credentials')


@auth.route('/logout')
class Logout(MethodView):
    @auth.response(HTTPStatus.OK, description='Returns success message')
    @jwt_required()
    def post(self):
        """Log the User Out"""
        unset_jwt_cookies
        db.session.commit()
        return {"message": "Logout successful"}, HTTPStatus.OK


@auth.route('/refresh')
class Refresh(MethodView):
    @auth.response(HTTPStatus.OK, description='Returns a new access token')
    @jwt_required(refresh=True)
    def post(self):
        """Generate Refresh Token"""
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        return jsonify({'access_token': access_token}), HTTPStatus.OK

