import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, Rating, db_drop_and_create_all
from config import bearer_tokens, SQLALCHEMY_TEST_DATABASE_URI
from datetime import date
import os

if 'CASTING_ASSISTANT' in os.environ:
    CASTING_ASSISTANT = os.environ['CASTING_ASSISTANT']
else:
    CASTING_ASSISTANT = bearer_tokens['casting_assistant']

if 'CASTING_DIRECTOR' in os.environ:
    CASTING_DIRECTOR = os.environ['CASTING_DIRECTOR']
else:
    CASTING_DIRECTOR = bearer_tokens['casting_director']

if 'EXECUTIVE_PRODUCER' in os.environ:
    EXECUTIVE_PRODUCER = os.environ['EXECUTIVE_PRODUCER']
else:
    EXECUTIVE_PRODUCER = bearer_tokens['executive_producer']

if 'SQLALCHEMY_TEST_DATABASE_URI' in os.environ:
    SQLALCHEMY_TEST_DATABASE_URI = os.environ['SQLALCHEMY_TEST_DATABASE_URI']

casting_assistant_auth_header = {
    'Authorization': CASTING_ASSISTANT
}

casting_director_auth_header = {
    'Authorization': CASTING_DIRECTOR
}

executive_producer_auth_header = {
    'Authorization': EXECUTIVE_PRODUCER
}

class AgencyTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = SQLALCHEMY_TEST_DATABASE_URI
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_create_new_actor(self):
        create_actor = {
            'name': 'Aileen',
            'age': 18,
            'gender': "Female"
        }

        res = self.client().post('/actors', json=create_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_error401_new_actor(self):

        create_actor = {
            'name': 'Aileen',
            'age': 18
        }

        res = self.client().post('/actors', json=create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing.')

    def test_error_422_create_new_actor(self):

        create_actor_without_name = {
            'age': 19
        }

        res = self.client().post('/actors', json=create_actor_without_name, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_actors(self):
        res = self.client().get('/actors?page=1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_actors(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing.')

    def test_error_404_get_actors(self):
        res = self.client().get('/actors?page=100', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_edit_actor(self):
        edit_actor_with_new_age = {
            'age': 30
        }
        res = self.client().patch('/actors/1', json=edit_actor_with_new_age, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    def test_error_400_edit_actor(self):

        res = self.client().patch('/actors/100', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_error_404_edit_actor(self):
        edit_actor_with_new_age = {
            'age': 30
        }
        res = self.client().patch('/actors/100', json=edit_actor_with_new_age,
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_error_401_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing.')

    def test_error_403_delete_actor(self):
        res = self.client().delete('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found in payload.')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_actor(self):
        res = self.client().delete('/actors/100', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_movie(self):

        json_create_movie = {
            'title': 'Crisso Movie',
            'release_date': date.today()
        }

        res = self.client().post('/movies', json=json_create_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_error_422_create_new_movie(self):
        """Test Error POST new movie."""

        create_movie_without_name = {
            'release_date': date.today()
        }

        res = self.client().post('/movies', json=create_movie_without_name, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    # ----------------------------------------------------------------------------#
    # Tests for /movies GET
    # ----------------------------------------------------------------------------#

    def test_get_all_movies(self):
        res = self.client().get('/movies?page=1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing.')

    def test_error_404_get_movies(self):
        res = self.client().get('/movies?page=100', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_edit_movie(self):
        edit_movie = {
            'release_date': date.today()
        }
        res = self.client().patch('/movies/1', json=edit_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_error_400_edit_movie(self):
        res = self.client().patch('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_error_404_edit_movie(self):
        edit_movie = {
            'release_date': date.today()
        }
        res = self.client().patch('/movies/100', json=edit_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_error_401_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing.')

    def test_error_403_delete_movie(self):
        res = self.client().delete('/movies/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found in payload.')

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_movie(self):
        res = self.client().delete('/movies/100', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable.
# From app directory, run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()