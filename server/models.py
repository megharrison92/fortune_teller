from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import validates


db = SQLAlchemy()

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    num_games_played = db.Column(db.Integer)
    user_high_score = db.Column(db.Integer)
    user_score = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates = 'games')
   

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    user_password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_history = db.Column(db.String)

    games = db.relationship('Game', back_populates = 'user')

    comments = db.relationship('Comment', back_populates = 'user')
    predictions = association_proxy('comments', 'prediction')

    serialize_rules = ('-comments.user',)


class Prediction(db.Model, SerializerMixin):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    date_created = db.Column(db.Integer)

    comments = db.relationship('Comment', back_populates = 'prediction')
    users = association_proxy('comments', 'user')

    serialize_rules = ('-comments.prediction',)


class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    like = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id'))

    user = db.relationship('User', back_populates = 'comments' )
    prediction = db.relationship('Prediction', back_populates = 'comments' )

    serialize_rules = ('-user.comments', '-prediction.comments',)