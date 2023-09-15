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
    for i in range(num_users):
        user = User(
            username = fake.user_name(),
            user_password = fake.password(),
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            user_history = fake.text()
        )
        db.session.add(user)

def create_predictions(num_predictions, users):
    for i in range(num_predictions):
        prediction = Prediction(
            content = fake.sentence(),
            date_created = fake.date_time_this_decade()
        )
        random_user = random.choice(users)
        prediction.users.append(random_user)
        db.session.add(prediction)

def create_games(num_games, users):
    for i in range(num_games):
        game = Game(
            num_games_played = fake.random_int(1, 100),
            user_high_score = fake.random_int(100, 100000000),
            user_score = fake.random_int(1, 25000),
            users = [random.choice(users)]
        )
        random_user = random.choice(users)
        game.users = random_user
        db.session.add(game)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        num_users = 10
        num_predictions = 20
        num_games = 30

        create_users(num_users)
        db.session.commit()

        users = User.query.all()

        create_predictions(num_predictions, users)
        db.session.commit()

        create_games(num_games, users)
        db.session.commit()