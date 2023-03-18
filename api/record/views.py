from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy import Null
from ..models.user import User
from ..models.record import Record
from ..models.course import Course
from ..models.schema import RecordSchema, StudentSchema, ScoreSchema, UpdateScoreArgsSchema, ScoreArgsSchema
from http import HTTPStatus
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import db
from ..utils.decorator import admin_required
from ..utils.grader import letter_grade
from ..utils.gpa import grade_to_gpa

record = Blueprint(
    'Record',
    __name__,
    url_prefix='/record',
    description='Endpoints for retrieving student and course records.'
)


# Admin resource - only admin should see all who registered for a course
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
                abort(HTTPStatus.NOT_FOUND, message='There are currently no registered students')
        else:
            abort(HTTPStatus.NOT_FOUND, message='Course does not exist')


# Student score resource - Show current score in a course
@record.route('/student/<int:course_id>')
class GetStudentCourseScore(MethodView):
    @record.response(HTTPStatus.OK, ScoreSchema, description='Returns an object containing'
                                                             ' students score in a course')
    @jwt_required()
    def get(self, course_id):
        """Get students score for a specified course"""
        course_exist = Course.query.filter_by(course_id=course_id).first()
        student_id = get_jwt_identity()

        if course_exist:
            score = Record.query.filter_by(course_id=course_id, student_id=student_id).first()
            if score is not None:
                result = []
                if score.score is Null:
                    score_val = "You haven't been scored yet"
                    grade_val = "You haven't been graded yet"
                else:
                    score_val = score.score
                    grade_val = letter_grade(score.score)

                result_dict = {'name': course_exist.name,
                               'teacher': course_exist.teacher,
                               'credit': course_exist.credit,
                               'score': score_val,
                               'grade': grade_val
                               }

                result.append(result_dict)
                return jsonify(result), HTTPStatus.OK
            else:
                abort(HTTPStatus.NOT_FOUND, message='You have not been registered for this course')
        else:
            abort(HTTPStatus.NOT_FOUND, message='Course does not exist')


@record.route('/<int:course_id>/')
@record.route('/<int:course_id>/<int:student_id>')
class StudentCourseScoreById(MethodView):
    @record.arguments(UpdateScoreArgsSchema)
    @record.response(HTTPStatus.CREATED, ScoreArgsSchema, description='Returns an object containing'
                                                                      ' students course data with new score')
    @admin_required()
    def put(self, score_data, course_id, student_id):
        """Add score to specified student, who has been registered for the specified course"""

        student_data = User.query.filter_by(user_id=student_id, category='STUDENT').first()

        # check if user requested student exist
        if student_data is not None:
            course_data = Course.query.filter_by(course_id=course_id).first()
            if course_data is not None:
                record_exist = Record.query.filter_by(course_id=course_id, student_id=student_id).first()
                if record_exist:
                    record_exist.score = int(score_data['score'])
                    record_exist.save()

                    result = []
                    result_dict = {'name': course_data.name,
                                   'firstname': student_data.firstname,
                                   'lastname': student_data.lastname,
                                   'matric_no': student_data.matric_no,
                                   'score': record_exist.score,
                                   'grade': letter_grade(record_exist.score)
                                   }

                    result.append(result_dict)
                    return jsonify(result), HTTPStatus.CREATED
                else:
                    abort(HTTPStatus.NOT_FOUND, message='Student has not been registered')
            else:
                abort(HTTPStatus.NOT_FOUND, message='Course does not exist')
        else:
            abort(HTTPStatus.NOT_FOUND, message='Student does not exist')

    @record.response(HTTPStatus.OK, ScoreArgsSchema, description='Returns an object containing'
                                                                 ' student\'s score in a course')
    @admin_required()
    def get(self, course_id, student_id):
        """Get a specified students score for a specified course"""
        course_exist = Course.query.filter_by(course_id=course_id).first()

        if course_exist:
            score = Record.query.filter_by(course_id=course_id, student_id=student_id).first()
            if score is not None:
                student_data = User.query.filter_by(user_id=student_id).first()
                result = []
                if score.score is Null:
                    score_val = "The student hasn't been scored yet"
                    grade_val = "The student hasn't been graded yet"
                else:
                    score_val = score.score
                    grade_val = letter_grade(score.score)

                result_dict = {'name': course_exist.name,
                               'firstname': student_data.firstname,
                               'lastname': student_data.lastname,
                               'matric_no': student_data.matric_no,
                               'score': score_val,
                               'grade': grade_val
                               }

                result.append(result_dict)
                return jsonify(result), HTTPStatus.OK
            else:
                abort(HTTPStatus.NOT_FOUND, message='The student has not been registered for this course')
        else:
            abort(HTTPStatus.NOT_FOUND, message='Course does not exist')


@record.route('/cgpa')
class GetStudentCourseScore(MethodView):
    @record.response(HTTPStatus.OK, ScoreSchema, description='Returns a message containing'
                                                             ' students CGPA of all courses')
    @jwt_required()
    def get(self):
        """Get students CGPA for all courses"""
        student_id = get_jwt_identity()
        course_exist = Record.query.filter_by(student_id=student_id).all()

        if course_exist:
            total_gpa = 0
            course_count = 0
            for course in course_exist:
                course_count += 1
                if course is not Null:
                    total_gpa += grade_to_gpa(letter_grade(course.score))

            cgpa = total_gpa / course_count
            cgpa = float("{:.2f}".format(cgpa))
            return jsonify({"message": f"Your current CGPA is {cgpa}"}), HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message='You have not registered for any course yet')
