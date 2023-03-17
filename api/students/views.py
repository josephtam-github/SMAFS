from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.schema import StudentSchema, UserQueryArgsSchema
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask import jsonify
from api import db
from ..utils.decorator import admin_required

student = Blueprint(
    'Student',
    __name__,
    url_prefix='/student',
    description='Endpoints for reading, updating, and deleting students.'
)


# Admin resource - This is because only an admin should
# have the right to perform CRUD operations on other users
@student.route('/<student_id>')
class StudentById(MethodView):
    @student.response(HTTPStatus.OK, StudentSchema, description='Returns an object containing requested student data')
    @admin_required()
    def get(self, student_id):
        """Get a specific student detail"""

        student_data = User.query.filter_by(user_id=student_id, category='STUDENT').first()

        # check if user requested student exist
        if student_data is not None:
            return student_data, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.NOT_FOUND, message='Student does not exist')

    @student.arguments(StudentSchema)
    @student.response(HTTPStatus.CREATED, StudentSchema, description='Returns an object containing updated student data')
    @admin_required()
    def put(self, update_data, student_id):
        """Update a specific user detail"""

        user_to_update = User.query.filter_by(user_id=student_id).first()

        if user_to_update is not None:
            user_to_update.firstname = update_data['firstname']
            user_to_update.lastname = update_data['lastname']
            user_to_update.email = update_data['email']
            user_to_update.password_hash = generate_password_hash(update_data['password'])
            user_to_update.update()
            return user_to_update, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.NOT_FOUND, message='User does not exist')

    @student.response(HTTPStatus.OK, StudentSchema, description='Returns success message')
    @admin_required()
    def delete(self, student_id):
        """Delete a specific student detail"""

        student_data = User.query.filter_by(user_id=student_id, category='STUDENT').first()

        # check if user requested student exist
        if student_data is not None:
            student_data.delete()
            return jsonify({'message': 'Student successfully deleted'}), HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message='Student does not exist')


@student.route('/all')
class ListStudent(MethodView):
    @student.response(HTTPStatus.OK, StudentSchema(many=True),
                      description='Returns an object containing all student data'
                      )
    @admin_required()
    def get(self):
        """Get a list of all students"""
        student_data = User.query.filter_by(category='STUDENT').all()

        # check if user requested student exist
        if student_data is not None:
            return student_data, HTTPStatus.OK
        else:
            abort(HTTPStatus.NO_CONTENT, message='There are currently no students')


# Student resource - This is for students to perform CRUD operations on their accounts
@student.route('/')
class Student(MethodView):
    @student.response(HTTPStatus.OK, StudentSchema, description='Returns an object containing student\'s own data')
    @jwt_required()
    def get(self):
        """Get a specific student detail"""
        student_id = get_jwt_identity()
        student_data = User.query.filter_by(user_id=student_id, category='STUDENT').first()

        # check if user requested student exist
        if student_data is not None:
            return student_data, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.NOT_FOUND, message='Student does not exist')

    @student.arguments(StudentSchema)
    @student.response(HTTPStatus.CREATED, StudentSchema, description='Returns an object containing student\'s new data')
    @jwt_required()
    def put(self, update_data):
        """Update a specific user detail"""

        student_id = get_jwt_identity()
        user_to_update = User.query.filter_by(user_id=student_id).first()

        if user_to_update is not None:
            user_to_update.firstname = update_data['firstname']
            user_to_update.lastname = update_data['lastname']
            user_to_update.email = update_data['email']
            user_to_update.password_hash = generate_password_hash(update_data['password'])
            user_to_update.update()
            return user_to_update, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.NOT_FOUND, message='User does not exist')
