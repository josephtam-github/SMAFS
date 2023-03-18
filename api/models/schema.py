import marshmallow as mar
from marshmallow import EXCLUDE
from marshmallow.validate import Length, Range
from marshmallow_sqlalchemy import field_for
from ..models.user import User
from api import ma
from ..models.course import Course
from ..models.record import Record


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True
        unknown = EXCLUDE

    user_id = field_for(User, "user_id", dump_only=True)
    firstname = field_for(User, "firstname", required=True, validate=Length(min=2, max=45))
    lastname = field_for(User, "lastname", required=True, validate=Length(min=2, max=45))
    email = field_for(User, "email", required=True, validate=Length(min=5, max=50))
    category = field_for(User, "category", required=False)
    password = field_for(User, "password_hash", required=True)
    matric_no = field_for(User, "matric_no", dump_only=True)


class UserQueryArgsSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = mar.fields.Integer()
    firstname = mar.fields.String(validate=Length(min=2, max=45))
    lastname = mar.fields.String(validate=Length(min=2, max=45))
    email = mar.fields.Email(validate=Length(min=2, max=50))
    category = mar.fields.String(validate=Length(min=2, max=50))
    matric_no = mar.fields.String(validate=Length(min=2, max=50))


class LoginQueryArgsSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE

    email = mar.fields.String(validate=Length(min=2, max=50))
    matric_no = mar.fields.String(validate=Length(min=2, max=50))
    password = mar.fields.String(required=True)


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = False
        unknown = EXCLUDE

    firstname = field_for(User, "firstname", required=True, validate=Length(min=2, max=45))
    lastname = field_for(User, "lastname", required=True, validate=Length(min=2, max=45))
    email = field_for(User, "email", required=True, validate=Length(min=5, max=50))
    category = field_for(User, "category", required=False)
    password = field_for(User, "password_hash", required=True)
    matric_no = field_for(User, "matric_no", dump_only=True)


class StudentUpdateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = False
        unknown = EXCLUDE

    firstname = field_for(User, "firstname", required=True, validate=Length(min=2, max=45))
    lastname = field_for(User, "lastname", required=True, validate=Length(min=2, max=45))
    email = field_for(User, "email", required=True, validate=Length(min=5, max=50))
    password = field_for(User, "password_hash", required=True)


class CourseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        ordered = False
        unknown = EXCLUDE

    course_id = field_for(Course, "course_id", dump_only=True, validate=Length(min=2, max=45))
    name = field_for(Course, "name", required=True, validate=Length(min=2, max=45))
    teacher = field_for(Course, "teacher", required=True, validate=Length(min=5, max=50))
    credit = field_for(Course, "credit", required=True)


class CourseArgsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        ordered = False
        unknown = EXCLUDE

    name = field_for(Course, "name", required=True, validate=Length(min=2, max=45))
    teacher = field_for(Course, "teacher", required=True, validate=Length(min=5, max=50))
    credit = field_for(Course, "credit", required=True)


class RecordSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        ordered = False
        unknown = EXCLUDE

    course_id = field_for(Record, "course_id", validate=Length(min=2, max=45))
    student_id = field_for(Record, "student_id", validate=Length(min=2, max=45))


class ScoreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        ordered = False
        unknown = EXCLUDE

    name = field_for(Course, "name", required=True, validate=Length(min=2, max=45))
    teacher = field_for(Course, "teacher", required=True, validate=Length(min=5, max=50))
    credit = field_for(Course, "credit", required=True)
    score = field_for(Record, "score", required=True)
    grade = mar.fields.String()


class ScoreArgsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        ordered = False
        unknown = EXCLUDE

    name = field_for(Course, "name", required=True, validate=Length(min=2, max=45))
    firstname = field_for(User, "firstname", required=True, validate=Length(min=2, max=45))
    lastname = field_for(User, "lastname", required=True, validate=Length(min=2, max=45))
    matric_no = field_for(User, "matric_no", dump_only=True)
    score = field_for(Record, "score", required=True)
    grade = mar.fields.String()


class UpdateScoreArgsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        ordered = False
        unknown = EXCLUDE

    score = field_for(Record, "score", required=True, validate=Range(min=0, max=100))
