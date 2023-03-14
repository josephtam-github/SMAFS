from api import db


class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"<Student {self.student_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_by_id(cls, student_id):
        return cls.query.get_or_404(student_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
