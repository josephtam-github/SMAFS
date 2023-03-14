import marshmallow as mar
from marshmallow import EXCLUDE
from marshmallow.validate import Length
from marshmallow_sqlalchemy import field_for
from ..models.student import Student
from api import ma
from ..models.course import Course
from ..models.record import Record


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True
        unknown = EXCLUDE

    student_id = field_for(Student, "student_id", dump_only=True)
    firstname = field_for(Student, "firstname", required=True, validate=Length(min=2, max=45))
    lastname = field_for(Student, "lastname", required=True, validate=Length(min=2, max=45))
    email = field_for(Student, "email", required=True, validate=Length(min=5, max=50))
    is_admin = field_for(Student, "is_admin", dump_only=True)
    password = field_for(Student, "password_hash", required=True)

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class StudentQueryArgsSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE

    student_id = mar.fields.Integer()
    firstname = mar.fields.String(validate=Length(min=2, max=45))
    lastname = mar.fields.String(validate=Length(min=2, max=45))
    email = mar.fields.String(validate=Length(min=2, max=50))
    is_admin = mar.fields.Boolean()


class LoginQueryArgsSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE

    email = mar.fields.String(required=True, validate=Length(min=2, max=50))
    password = mar.fields.String(required=True)