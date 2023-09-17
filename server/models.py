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

    def __repr__(self):
        return f'<Game id = {self.id} >'
   

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

    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 1:
            raise ValueError('Username must be a string greater than 1 character')
        return username
    
    @validates('user_password')
    def validate_password(self, key, user_password):
        if len(user_password) < 1 or len(user_password) > 26 or not any(char.isdigit() for char in user_password):
            raise ValueError('Password must be a string between 1 and 26 characters and have at least 1 number or special character')
        return user_password
    
    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if len(first_name) < 1:
            raise ValueError('First name must be a string greater than 1 character.')
        return first_name
    
    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if len(last_name) < 1:
            raise ValueError('Last name must be a string greater than 1 character.')
        return last_name

    def __repr__(self):
        return f'<User id = {self.id} username = {self.username} user_password = {self.user_password} first_name = {self.first_name} last_name = {self.last_name} user_history = {self.user_history} >'


class Prediction(db.Model, SerializerMixin):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    date_created = db.Column(db.Integer)

    comments = db.relationship('Comment', back_populates = 'prediction')
    users = association_proxy('comments', 'user')

    serialize_rules = ('-comments.prediction',)

    def __repr__(self):
        return f'<Prediction id = {self.id} content = {self.content} date_created = {self.date_created}>'


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

    @validates('comment')
    def validate_username(self, key, comment):
        if not comment or len(comment) < 1:
            raise ValueError('Username must be a string greater than 1 character')
        return comment

    def __repr__(self):
        return f'<Comment id = {self.id} comment = {self.comment} like = {self.like}>'