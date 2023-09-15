# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource
import ipdb
from flask_migrate import Migrate

# Local imports
from config import app, api
# Add your model imports
from models import User, Prediction, Game, Comment

#should the secret key go here?

@app.route('/')
def hello():
    return 'Hello from Flask Backend!'


if __name__ == '__main__':
    app.run(port=5555, debug=True)
