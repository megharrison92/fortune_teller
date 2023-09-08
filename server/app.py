# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource
import ipdb


# Local imports
from config import app, db, api
# Add your model imports

@app.route('/')
def hello():
    return 'Hello from Flask Backend!'


if __name__ == '__main__':
    app.run(port=5555, debug=True)
