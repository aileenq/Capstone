import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from config import SQLALCHEMY_DATABASE_URI

if 'DATABASE_URL' in os.environ:
    database_path = os.environ['DATABASE_URL']
    if database_path.startswith("postgres://"):
        database_path = database_path.replace("postgres://", "postgresql://", 1)
else:
    database_path = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    setup_default_records()

def setup_default_records():
    actor = (Actor(
        name='aileen',
        gender='Female',
        age=18
    ))

    movie = (Movie(
        title='Aileen meets tiger',
        release_date=date.today()
    ))

    rating = Rating.insert().values(
        Movie_id=movie.id,
        Actor_id=actor.id,
        rating=3.0
    )

    actor.insert()
    movie.insert()
    db.session.execute(rating)
    db.session.commit()

# actor and movie is many_to_many relationship
Rating = db.Table('ratings',
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('rating', db.Float)
)
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(db.Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    release_date = Column(db.Date)
    actors = db.relationship('Actor', secondary=Rating, backref=db.backref('ratings', lazy='joined'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
