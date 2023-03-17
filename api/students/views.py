from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models.user import User
from ..models.schema import StudentSchema, UserQueryArgsSchema
from http import HTTPStatus
from flask import jsonify
from api import db
from ..utils.matriculator import matric, dematric

student = Blueprint(
    'Student',
    __name__,
    url_prefix='/student',
    description='Endpoints for reading, updating, and deleting students.'
)


@student.route('/<student_id>')
class Student(MethodView):
    @student.response(HTTPStatus.OK, StudentSchema, description='Returns an object containing requested student data')
    def get(self, student_id):
        """Get specific student detail"""

        student_data = User.query.filter_by(user_id=student_id, category='STUDENT').first()

        # check if user requested student exist
        if student_data is not None:
            return student_data, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.NOT_FOUND, message='Student does not exist')

