from api import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String(50), default="STUDENT")
    matric_no = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.user_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get_or_404(user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
