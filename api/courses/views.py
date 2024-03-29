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


# Admin resources
@course.route('/register')
class Register(MethodView):
    @course.arguments(CourseSchema)
    @course.response(HTTPStatus.CREATED, CourseSchema, description='Returns an object containing created course detail')
    @admin_required()
    def post(self, new_data):
        """Register a new course - Admin only

        Returns the details of the new course from database
        """

        name_exist = Course.query.filter_by(name=new_data['name'].upper()).first()
        if name_exist:
            abort(HTTPStatus.NOT_ACCEPTABLE, message='This name already exists')

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
        """Get a specific course detail - Admin only

        Returns the course's detail as a list of objects
        """

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
        """Update a specific course detail - Admin only

        Returns the updated course detail from database
        """

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
        """Delete a specific course detail - Admin only

        Returns a message upon successful deletion
        """

        course_data = Course.query.filter_by(course_id=course_id).first()

        # check if user requested course exist
        if course_data is not None:
            course_data.delete()
            return jsonify({'message': 'course successfully deleted'}), HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message='course does not exist')


@course.route('/<int:course_id>/student/<int:student_id>')
class StudentCourseById(MethodView):
    @course.response(HTTPStatus.CREATED, RecordSchema, description='Returns an object containing requested course data')
    @admin_required()
    def get(self, course_id, student_id):
        """Register specified student to specified course - Admin only

        Returns the course and user id, the score for the course is set to null.
        """

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


# Student resources
@course.route('/all')
class ListCourse(MethodView):
    @course.response(HTTPStatus.OK, CourseSchema(many=True), description='Returns an object containing all course data')
    @jwt_required()
    def get(self):
        """Get a list of all courses

        Returns all registered courses
        """
        course_data = Course.query.all()

        # check if user requested course exist
        if course_data is not None:
            return course_data, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message='There are currently no courses')


@course.route('/student')
class CourseById(MethodView):
    @course.response(HTTPStatus.OK, CourseSchema, description='Returns an object containing detail'
                                                              ' of all offered course')
    @jwt_required()
    def get(self):
        """Get detail of all courses being offered

        Returns all the courses offered as a list of objects
        """
        student_id = get_jwt_identity()
        course_data = Record.query.filter_by(student_id=student_id).all()

        # check if user requested course data exist
        if course_data is not None:
            result = []
            for courses in course_data:
                course_detail = Course.query.filter_by(course_id=courses.course_id).first()
                result_dict = {
                    'course_id': course_detail.course_id,
                    'name': course_detail.name,
                    'teacher': course_detail.teacher,
                    'credit': course_detail.credit
                }
                result.append(result_dict)
            return jsonify(result), HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message='You have not been registered for any course')
