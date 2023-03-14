from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies, decode_token
from ..models.student import Student
from ..models.schema import StudentSchema, LoginQueryArgsSchema
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from api import db

auth = Blueprint(
    'Auth',
    __name__,
    url_prefix='/auth',
    description='Authentication for student registration and login with JWT token'
)


@auth.route('/signup')
class Register(MethodView):
    @auth.arguments(StudentSchema)
    @auth.response(HTTPStatus.OK, StudentSchema, description='Returns an object containing ')
    def post(self, new_data):
        """Register a new student"""

        new_student = Student(
            firstname=new_data['firstname'],
            lastname=new_data['lastname'],
            email=new_data['email'],
            password_hash=generate_password_hash(new_data['password'])
        )
        new_student.save()

        return new_student, HTTPStatus.OK


@auth.route('/login')
class Login(MethodView):
    @auth.arguments(LoginQueryArgsSchema)
    @auth.response(HTTPStatus.CREATED, LoginQueryArgsSchema, description='Returns the access and return tokens')
    def post(self, login_data):
        """Logs in student"""

        email = login_data['email']
        password = login_data['password']

        student = Student.query.filter_by(email=email).first()

        if (student is not None) and check_password_hash(student.password_hash, password):
            access_token = create_access_token(identity=student.student_id)
            refresh_token = create_refresh_token(identity=student.student_id)
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
        """
            Log the User Out
        """
        unset_jwt_cookies
        db.session.commit()
        return {"message": "Logout successful"}, HTTPStatus.OK
