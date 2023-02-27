import os
from flask import Flask, request, abort, jsonify
from models import setup_db, db_drop_and_create_all, Actor, Movie, Rating
from auth import AuthError, requires_auth
from flask_cors import CORS

PAGE_SIZE = 10


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return "Hi, there, Please use postman to send request with authorization token"

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    def paginate_results(requests, selection):
        page = requests.args.get('page', 1, type=int)

        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE

        objects_formatted = [object_name.format() for object_name in selection]
        return objects_formatted[start:end]

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()
        actors_paginated = paginate_results(request, actors)

        if len(actors_paginated) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors_paginated
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_actors(jwt):
        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if not (name and age and gender):
            abort(422)

        actor = (Actor(
            name=name,
            age=age,
            gender=gender
        ))
        actor.insert()

        return jsonify({
            'success': True,
            'created': actor.id
        })

    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actors(payload, actor_id):
        if not actor_id:
            abort(400)
        body = request.get_json()
        if not body:
            abort(400)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404)

        name = body.get('name', actor.name)
        age = body.get('age', actor.age)
        gender = body.get('gender', actor.gender)

        # Set new field values
        actor.name = name
        actor.age = age
        actor.gender = gender

        actor.update()

        return jsonify({
            'success': True,
            'updated': actor.id,
            'actor': [actor.format()]
        })

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, actor_id):
        if not actor_id:
            abort(400)

        # Find actor which should be deleted by id
        actor_to_delete = Actor.query.filter(
            Actor.id == actor_id).one_or_none()
        if not actor_to_delete:
            abort(404)

        actor_to_delete.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        selection = Movie.query.all()
        movies_paginated = paginate_results(request, selection)

        if len(movies_paginated) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies_paginated
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_movies(jwt):
        body = request.get_json()
        if not body:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not (title and release_date):
            abort(422)

        new_movie = (Movie(
            title=title,
            release_date=release_date
        ))
        new_movie.insert()

        return jsonify({
            'success': True,
            'created': new_movie.id
        })

    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movies(jwt, movie_id):
        body = request.get_json()

        if not movie_id:
            abort(400)

        if not body:
            abort(400)

        movie_to_update = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if not movie_to_update:
            abort(404)

        title = body.get('title', movie_to_update.title)
        release_date = body.get('release_date', movie_to_update.release_date)

        movie_to_update.title = title
        movie_to_update.release_date = release_date

        movie_to_update.update()

        return jsonify({
            'success': True,
            'edited': movie_to_update.id,
            'movie': [movie_to_update.format()]
        })

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, movie_id):
        if not movie_id:
            abort(400)

        movie_to_delete = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if not movie_to_delete:
            abort(404)

        movie_to_delete.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
