from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies, decode_token
from ..models.student import Student
from ..models.schema import StudentSchema
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint(
    'Auth',
    __name__,
    url_prefix='/auth',
    description='Authentication for student registration and login with JWT token'
)


@auth.route('/signup')
class Register(MethodView):
    @auth.arguments(StudentSchema)
    @auth.response(201, StudentSchema)
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
