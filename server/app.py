# Remote library imports
from flask import request, make_response, session, jsonify
from flask_restful import Resource
import ipdb
from flask_migrate import Migrate

# Local imports
from config import app, api, db
# Add your model imports
from models import User, Prediction, Game, Comment

@app.route('/')
def hello():
    return '<h1>Capstone Project</h1>'

class Users(Resource):
    def get(self):
        q = [user.to_dict(rules = ()) for user in User.query.all()]
        response = make_response(q, 200)
        return response
    
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(new_user.to_dict(), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
