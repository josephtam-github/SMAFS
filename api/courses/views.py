from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models.user import User
from ..models.course import Course
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.schema import CourseSchema
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
            teacher=new_data['teacher'],
            credit=new_data['credit'],
        )
        new_course.save()

        return new_course, HTTPStatus.CREATED


@course.route('/all')
class ListCourse(MethodView):
    @course.response(HTTPStatus.OK, CourseSchema(many=True), description='Returns an object containing all course data')
    def get(self):
        """Get a list of all courses"""
        course_data = Course.query.all()

        # check if user requested student exist
        if course_data is not None:
            return course_data, HTTPStatus.OK
        else:
            abort(HTTPStatus.NO_CONTENT, message='There are currently no students')
