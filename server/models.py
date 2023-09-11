from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import validates

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    num_games_played = db.Column(db.Integer)
    user_high_score = db.Column(db.Integer)
    user_score = db.Column(db.Integer)



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_history = db.Column(db.String)

    predictions = db.relationship('Prediction', secondary='user_predictions', back_populates='users')


class Prediction(db.Model, SerializerMixin):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    date_created = db.Column(db.Integer)

    users = db.relationship('User', secondary='user_predictions', back_populates='predictions')





class UserPrediction(db.Model, SerializerMixin):
    __tablename__ = 'user_predictions'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id'))

    user = db.relationship('User', back_populates='predictions')
    prediction = db.relationship('Prediction', back_populates='users')





from config import db, bcrypt