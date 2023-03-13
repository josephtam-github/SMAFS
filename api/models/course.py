from api import db


class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    teacher = db.Column(db.String(90), nullable=False)
    credit = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"<Course {self.course_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_by_id(cls, course_id):
        return cls.query.get_or_404(course_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
