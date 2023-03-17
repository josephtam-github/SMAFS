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
            teacher=new_data['teacher'].title(),
            credit=int(new_data['credit']),
        )
        new_course.save()

        return new_course, HTTPStatus.CREATED


@course.route('/<course_id>')
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


# # course resource - This is for courses to perform CRUD operations on their accounts
# @course.route('/')
# class course(MethodView):
#     @course.response(HTTPStatus.OK, courseSchema, description='Returns an object containing course\'s own data')
#     @jwt_required()
#     def get(self):
#         """Get a specific course detail"""
#         course_id = get_jwt_identity()
#         course_data = Course.query.filter_by(user_id=course_id, category='course').first()
#
#         # check if user requested course exist
#         if course_data is not None:
#             return course_data, HTTPStatus.CREATED
#         else:
#             abort(HTTPStatus.NOT_FOUND, message='course does not exist')
#
#     @course.arguments(courseSchema)
#     @course.response(HTTPStatus.CREATED, courseSchema, description='Returns an object containing course\'s new data')
#     @jwt_required()
#     def put(self, update_data):
#         """Update a specific user detail"""
#
#         course_id = get_jwt_identity()
#         user_to_update = Course.query.filter_by(user_id=course_id).first()
#
#         if user_to_update is not None:
#             user_to_update.firstname = update_data['firstname']
#             user_to_update.lastname = update_data['lastname']
#             user_to_update.email = update_data['email']
#             user_to_update.password_hash = generate_password_hash(update_data['password'])
#             user_to_update.update()
#             return user_to_update, HTTPStatus.CREATED
#         else:
#             abort(HTTPStatus.NOT_FOUND, message='Course does not exist')
