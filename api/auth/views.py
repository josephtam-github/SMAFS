from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, \
    get_jwt_identity, unset_jwt_cookies, decode_token, get_jwt
from ..models.user import User
from ..models.blocklist import TokenBlocklist
from ..models.schema import UserSchema, LoginQueryArgsSchema
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from api import db, jwt
from datetime import datetime, timezone
from ..utils.matriculator import matric


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


auth = Blueprint(
    'Auth',
    __name__,
    url_prefix='/auth',
    description='Authentication for user registration and login with JWT token'
)


@auth.route('/register')
class Register(MethodView):
    @auth.arguments(UserSchema)
    @auth.response(HTTPStatus.OK, UserSchema, description='Returns an object containing ')
    def post(self, new_data):
        """Register a new user"""
        # Sets first user's role to admin
        last_user = User.query.order_by(User.user_id.desc()).first()
        if last_user:
            category = 'STUDENT'
            matric_no = matric(int(last_user.user_id) + 1)
        else:
            category = 'ADMIN'
            matric_no = matric(1)

        new_user = User(
            firstname=new_data['firstname'],
            lastname=new_data['lastname'],
            email=new_data['email'],
            password_hash=generate_password_hash(new_data['password']),
            category=category,
            matric_no=matric_no
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
            additional_claims = {"category": user.category}
            access_token = create_access_token(identity=user.user_id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.user_id, additional_claims=additional_claims)
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
    def delete(self):
        """Log the User Out"""
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return {"message": "Logout successful"}, HTTPStatus.OK


@auth.route('/refresh')
class Refresh(MethodView):
    @auth.response(HTTPStatus.OK, description='Returns a new access token')
    @jwt_required(refresh=True)
    def post(self):
        """Generate Refresh Token"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        access_token = create_access_token(identity=user_id, additional_claims=claims)
        return jsonify({'access_token': access_token}), HTTPStatus.OK

