import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, Flask
from models import setup_db, Question, Category

app = Flask(__name__)

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://abisolatayo@localhost:5432/trivia_test".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    #paginated_questions
    def test_get_paginated_questions(self):
        with app.app_context():
            res = self.client().get('/questions')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['total_questions'])
            self.assertTrue(len(data['questions']))

    #paginated_questions for failure
    def test_get_paginated_questions_failure(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

     #Retrieve Categories
    def test_retrieve_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data["categories"]))

    #Retrieve Categories for failure 
    def test_retrieve_categories_failure(self):
        res = self.client().get("/categories/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # def test_create_new_questions(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #     self.assertTrue(len(data['questions']))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()