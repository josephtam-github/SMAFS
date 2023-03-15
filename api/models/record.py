from api import db


class Record(db.Model):
    __tablename__ = "record"

    student_id = db.Column(db.Integer(), db.ForeignKey("student.student_id"), unique=True, nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey("course.course_id"), unique=True, nullable=False)
    score = db.Column(db.Integer(), nullable=True)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            student_id, course_id,
        ),
    )

    def __repr__(self):
        return f"<Score {self.score}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
