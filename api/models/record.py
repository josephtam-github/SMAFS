from api import db
from .user import User

class Record(db.Model):
    __tablename__ = "record"

    student_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"), unique=True, nullable=False)
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
        user = User.query.filter(user_id=self.student_id, category='STUDENT').\
            first_or_404(description='There is no student with id: {}'.format(self.student_id))
        if user is not None:
            db.session.add(self)
            db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
