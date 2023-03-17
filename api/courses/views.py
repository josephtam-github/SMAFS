from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models.user import User
from ..models.record import Record
from ..models.course import Course
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.schema import CourseSchema, RecordSchema
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask import jsonify
from api import db
from ..utils.decorator import admin_required

course = Blueprint(
    'Course',
    __name__,
    url_prefix='/course',
    description='Endpoints for creating, reading, updating, and deleting courses.'
)


@course.route('/register')
class Register(MethodView):
    @course.arguments(CourseSchema)
    @course.response(HTTPStatus.CREATED, CourseSchema, description='Returns an object containing created course detail')
    @admin_required()
    def post(self, new_data):
        """Register a new course"""
        new_course = Course(
            name=new_data['name'].upper(),
            teacher=new_data['teacher'].title(),
            credit=int(new_data['credit']),
        )
        new_course.save()

        return new_course, HTTPStatus.CREATED


@course.route('/<int:course_id>')
class CourseById(MethodView):
    @course.response(HTTPStatus.OK, CourseSchema, description='Returns an object containing requested course data')
    @admin_required()
    def get(self, course_id):
        """Get a specific course detail"""

        course_data = Course.query.filter_by(course_id=course_id).first()

        # check if user requested course exist
        if course_data is not None:
            return course_data, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.NOT_FOUND, message='Course does not exist')

    @course.arguments(CourseSchema)
    @course.response(HTTPStatus.CREATED, CourseSchema, description='Returns an object containing updated course data')
    @admin_required()
    def put(self, update_data, course_id):
        """Update a specific course detail"""

        course_to_update = Course.query.filter_by(course_id=course_id).first()

        # check if user requested course exist
        if course_to_update is not None:
            course_to_update.name = update_data['name'].upper()
            course_to_update.teacher = update_data['teacher'].title()
            course_to_update.credit = int(update_data['credit'])
            course_to_update.update()
            return course_to_update, HTTPStatus.CREATED
        else:
            abort(HTTPStatus.NOT_FOUND, message='Course does not exist')

    @course.response(HTTPStatus.OK, CourseSchema, description='Returns success message')
    @admin_required()
    def delete(self, course_id):
        """Delete a specific course detail"""

        course_data = Course.query.filter_by(course_id=course_id).first()

        # check if user requested course exist
        if course_data is not None:
            course_data.delete()
            return jsonify({'message': 'course successfully deleted'}), HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message='course does not exist')


@course.route('/all')
class ListCourse(MethodView):
    @course.response(HTTPStatus.OK, CourseSchema(many=True), description='Returns an object containing all course data')
    def get(self):
        """Get a list of all courses"""
        course_data = Course.query.all()

        # check if user requested course exist
        if course_data is not None:
            return course_data, HTTPStatus.OK
        else:
            abort(HTTPStatus.NO_CONTENT, message='There are currently no courses')


# Admin resource - Only an admin can register other students
@course.route('/<int:course_id>/')
@course.route('/<int:course_id>/<int:student_id>')
class CourseById(MethodView):
    @course.response(HTTPStatus.OK, RecordSchema, description='Returns an object containing requested course data')
    @admin_required()
    def get(self, course_id, student_id):
        """Register specified student to specified course"""

        student_data = User.query.filter_by(user_id=student_id, category='STUDENT').first()

        # check if user requested student exist
        if student_data is not None:
            course_data = Course.query.filter_by(course_id=course_id).first()
            if course_data is not None:
                record_exist = Record.query.filter_by(course_id=course_id, student_id=student_id).first()
                if record_exist:
                    abort(HTTPStatus.NOT_FOUND, message='Student has already been registered')
                else:
                    new_record = Record(
                        course_id=course_id,
                        student_id=student_id
                    )
                    new_record.save()
                    return new_record, HTTPStatus.CREATED
            else:
                abort(HTTPStatus.NOT_FOUND, message='Course does not exist')
        else:
            abort(HTTPStatus.NOT_FOUND, message='Student does not exist')
