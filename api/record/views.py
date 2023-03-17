from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models.user import User
from ..models.record import Record
from ..models.course import Course
from ..models.schema import CourseSchema, RecordSchema, StudentSchema
from http import HTTPStatus
from flask import jsonify
from api import db
from ..utils.decorator import admin_required

record = Blueprint(
    'Record',
    __name__,
    url_prefix='/record',
    description='Endpoints for retrieving student and course records.'
)


@record.route('/course/')
@record.route('/course/<int:course_id>')
class GetStudentsOnCourse(MethodView):
    @record.response(HTTPStatus.OK, StudentSchema, description='Returns an object containing'
                                                               ' all students registered to a course')
    @admin_required()
    def get(self, course_id):
        """Get a list of all students that registered for the course"""
        course_exist = Course.query.filter_by(course_id=course_id).first()

        if course_exist:
            students = Record.query.filter_by(course_id=course_id).all()
            if students is not None:
                result = []
                for student in students:
                    student_data = User.query.filter_by(user_id=student.student_id).first()
                    result_dict = {'firstname': student_data.firstname, 'lastname': student_data.lastname,
                                   'email': student_data.email, 'matric_no': student_data.matric_no}

                    result.append(result_dict)
                return jsonify(result), HTTPStatus.OK
            else:
                abort(HTTPStatus.NO_CONTENT, message='There are currently no registered students')
        else:
            abort(HTTPStatus.NOT_FOUND, message='Course does not exist')