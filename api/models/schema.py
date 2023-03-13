import marshmallow as ma
from marshmallow import EXCLUDE
from marshmallow.validate import Length
from marshmallow_sqlalchemy import field_for
from ..models.student import Student
from ..models.course import Course
from ..models.record import Record


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
        ordered = True
        unknown = EXCLUDE

    student_id = field_for(Student, "id", dump_only=True)
    firstname = field_for(Student, "firstname", required=True, validate=Length(min=2, max=45))
    lastname = field_for(Student, "lastname", required=True, validate=Length(min=2, max=45))
    email = field_for(Student, "email", required=True, validate=Length(min=5, max=50))
    is_staff = field_for(Student, "is_staff", required=True)
    password_hash = field_for(Student, "password_hash", dump_only=True)

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
        ordered = True

    firstname = mar.fields.String(validate=Length(min=2, max=45))
    lastname = mar.fields.String(validate=Length(min=2, max=45))
    email = mar.fields.String(validate=Length(min=2, max=50))
    is_staff = mar.fields.Boolean()
