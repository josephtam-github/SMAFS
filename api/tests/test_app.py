import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..utils.decorator import admin_required
from ..models.user import User
from ..models.course import Course
from ..models.record import Record
from flask_jwt_extended import create_access_token


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_app(self):
        #ADMIN TESTS BEGIN HERE

        # Activate a test user
        admin_signup_data = {
            "firstname": "Test",
            "lastname": "Admin",
            "email": "admin@altschool.com",
            "password": "password"
        }

        response = self.client.post('/auth/register', json=admin_signup_data)

        admin = User.query.filter_by(email='admin@altschool.com').first()
        additional_claims = {"category": admin.category}
        token = create_access_token(identity=admin.user_id, additional_claims=additional_claims)

        admin_header = {
            "Authorization": f"Bearer {token}"
        }

        # Register a student
        student_signup_data = {
            "firstname": "Test",
            "lastname": "Student",
            "email": "teststudent@gmail.com",
            "password": "password",
        }

        response = self.client.post('/auth/register', json=student_signup_data)

        student = User.query.filter_by(email='teststudent@gmail.com').first()

        assert student.firstname == "Test"

        # check to see if password is hashed
        assert student.password_hash != "password"

        assert response.status_code == 201

        # Retrieve all students
        response = self.client.get('/student/all', headers=admin_header)

        assert response.status_code == 200

        assert response.json == [{'category': 'STUDENT',
                                  'email': 'teststudent@gmail.com',
                                  'firstname': 'Test',
                                  'lastname': 'Student',
                                  'matric_no': 'U2023/002'
                                  }]

        # Sign a student in
        student_login_data = {
            "email": "teststudent@gmail.com",
            "password": "password"
        }

        response = self.client.post('/auth/login', json=student_login_data)

        assert response.status_code == 202

        # Retrieve a student's details by ID
        response = self.client.get('/student/2', headers=admin_header)

        assert response.status_code == 201

        assert response.json == {
            "firstname": "Test",
            "lastname": "Student",
            "email": "teststudent@gmail.com",
            "matric_no": "U2023/002",
            "category": "STUDENT"
        }

        # Update a student's details
        student_update_data = {
            "firstname": "Sample",
            "lastname": "Student",
            "email": "samplestudent@gmail.com",
            "password": "password"
        }

        response = self.client.put('/student/2', json=student_update_data, headers=admin_header)

        assert response.status_code == 201

        assert response.json == {
            "firstname": "Sample",
            "lastname": "Student",
            "email": "samplestudent@gmail.com",
            "matric_no": "U2023/002",
            "category": "STUDENT"
        }

        # COURSE TESTING
        # Register a test course
        course_registration_data = {
            "name": "Test Course",
            "teacher": "Test Teacher",
            "credit": 3
        }

        response = self.client.post('/course/register', json=course_registration_data, headers=admin_header)
        assert response.status_code == 201

        # Register second course
        course_registration_data = {
            "name": "Second Course",
            "teacher": "Second Teacher",
            "credit": 3
        }

        response = self.client.post('/course/register', json=course_registration_data, headers=admin_header)
        assert response.status_code == 201

        # Get all courses
        response = self.client.get('/course/all', headers=admin_header)
        assert response.status_code == 200
        assert response.json == [{
            "course_id": 1, "name": "TEST COURSE", "teacher": "Test Teacher", "credit": 3},
            {"course_id": 2, "name": "SECOND COURSE", "teacher": "Second Teacher", "credit": 3}]

        # Update course
        course_registration_data = {
            "name": "Updated Course",
            "teacher": "Updated Teacher",
            "credit": 3
        }
        response = self.client.put('/course/2', json=course_registration_data, headers=admin_header)
        assert response.status_code == 201

        # Get updated courses
        response = self.client.get('/course/all', headers=admin_header)
        assert response.status_code == 200
        assert response.json == [{
            "course_id": 1, "name": "TEST COURSE", "teacher": "Test Teacher", "credit": 3},
            {"course_id": 2, "name": "UPDATED COURSE", "teacher": "Updated Teacher", "credit": 3}]

        # Delete course
        response = self.client.delete('/course/2', json=course_registration_data, headers=admin_header)
        assert response.status_code == 200

        # Get updated on deleted course
        response = self.client.get('/course/all', headers=admin_header)
        assert response.status_code == 200
        assert response.json == [{
            "course_id": 1, "name": "TEST COURSE", "teacher": "Test Teacher", "credit": 3}]

        # Admin enrolls a student for a test course
        response = self.client.get('/course/1/student/2', headers=admin_header)

        # Upload a student's grade in a course
        response = self.client.get('record/1/student/2/90', headers=admin_header)

        assert response.status_code == 201

        assert response.json == [{'name': 'TEST COURSE',
                                  'firstname': 'Sample',
                                  'lastname': 'Student',
                                  'matric_no': 'U2023/002',
                                  'score': 90,
                                  'grade': 'A'
                                  }]

        # Retrieve a students course
        response = self.client.get('/record/1/student/2', headers=admin_header)

        assert response.status_code == 200

        assert response.json == [{'name': 'TEST COURSE',
                                  'firstname': 'Sample',
                                  'lastname': 'Student',
                                  'matric_no': 'U2023/002',
                                  'score': 90,
                                  'grade': 'A'
                                  }]

        # Update a grade
        response = self.client.get('record/1/student/2/75', headers=admin_header)

        assert response.status_code == 201

        assert response.json == [{'name': 'TEST COURSE',
                                  'firstname': 'Sample',
                                  'lastname': 'Student',
                                  'matric_no': 'U2023/002',
                                  'score': 75,
                                  'grade': 'C'
                                  }]

        # Confirm student course upgrade
        response = self.client.get('/record/1/student/2', headers=admin_header)

        assert response.status_code == 200

        assert response.json == [{'name': 'TEST COURSE',
                                  'firstname': 'Sample',
                                  'lastname': 'Student',
                                  'matric_no': 'U2023/002',
                                  'score': 75,
                                  'grade': 'C'
                                  }]

        # Register a new student
        student_signup_data = {
            "firstname": "New",
            "lastname": "Student",
            "email": "teststudent2@gmail.com",
            "password": "password",
        }

        response = self.client.post('/auth/register', json=student_signup_data)

        assert response.status_code == 201

        # Delete a new student
        response = self.client.delete('/student/3', headers=admin_header)
        assert response.status_code == 200

        # logout admin
        response = self.client.delete('auth/logout', headers=admin_header)

        assert response.status_code == 200

        # STUDENT TESTS BEGIN HERE
        additional_claims = {"category": student.category}
        token = create_access_token(identity=student.user_id, additional_claims=additional_claims)

        student_header = {
            "Authorization": f"Bearer {token}"
        }

        # Get CGPA
        response = self.client.get('record/cgpa', headers=student_header)
        assert response.json == {"message": "Your current CGPA is 2.3"}

        # Get details of all course being offered
        response = self.client.get('course/student', headers=student_header)
        assert response.status_code == 200
        assert response.json == [{
            "course_id": 1, "name": "TEST COURSE", "teacher": "Test Teacher", "credit": 3}]

        # Get score for specified course
        response = self.client.get('record/student/1', headers=student_header)
        assert response.status_code == 200
        assert response.json == [{'credit': 3,
                                  'grade': 'C',
                                  'name': 'TEST COURSE',
                                  'score': 75,
                                  'teacher': 'Test Teacher'}]
