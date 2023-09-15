# Standard library imports
from random import randint, choice as rc
import random
# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Game, User, Prediction, Comment

fake = Faker()

def create_users(num_users):
    users = []
    for i in range(num_users):
        user = User(
            username = fake.user_name(),
            user_password = fake.password(),
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            user_history = fake.text()
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

def create_predictions(num_predictions, users):
    predictions = []
    for i in range(num_predictions):
        prediction = Prediction(
            content = fake.text(),
            date_created = fake.date_time_this_decade().timestamp()
        )
        user = random.choice(users)
        comment = Comment(user=user, prediction=prediction)
        predictions.append(prediction)
    db.session.add_all(predictions)
    db.session.commit()

def create_comments(num_comments, predictions, users):
    comments = []
    for i in range(num_comments):
        comment = Comment(
            comment = fake.text(),
            like =randint(1,100)
        )
        user = random.choice(users)
        prediciton = random.choice(predictions)
        comment.user = user
        comment.prediction = prediciton
        comments.append(comment)
    db.session.add_all(comments)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        num_users = 10
        num_predictions = 20
        num_comments = 30

        print("Clearing db...")
        Comment.query.delete()
        Prediction.query.delete()
        User.query.delete()

        print("Seeding users...")
        create_users(num_users)

        users = User.query.all()

        print("Seeding predictions...")
        create_predictions(num_predictions, users)

        predictions = Prediction.query.all()

        print("Seeding comments...")
        create_comments(num_comments, predictions, users)

        print("Done seeding!")