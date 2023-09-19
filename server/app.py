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
    
api.add_resource( Users, '/users' )

class UsersById(Resource):
    def get(self):
        user = User.query.filter( User.id == id ).first()
        if user is None:
            return make_response({'error': 'User not found'}, 404)
        return make_response(user.to_dict(), 200)
    
    def delete(self, id):
        user = User.query.filter( User.id == id ).first()
        if user is None:
            return make_response({'error': 'User not found'}, 404)
        db.session.delete(user)
        db.session.commit()
        return make_response('', 204)
    
api.add_resource( UsersById, '<int:id>')

class Predictions(Resource):
    def get(self):
        predictions = [prediction.to_dict(rules=())for prediction in Prediction.query.all()]
        response = make_response(predictions, 200)
        return response
    
    def post(self):
        data = request.get_json()
        new_prediction = Prediction(content=data['content'], date_created=data['date_created'])
        db.session.add(new_prediction)
        db.session.commit()
        return make_response(new_prediction.to_dict(), 200)
    
api.add_resource( Predictions, '/predictions')

class PredictionsById(Resource):
    def get(self, id):
        prediction = Prediction.query.filter( Prediction.id == id ).first()
        if prediction is None:
            return make_response({'error': 'Prediction not found'}, 404)
        return make_response(prediction.to_dict(), 200)
    
    def put(self,id):
        prediction = Prediction.query.filter( Prediction.id == id ).first()
        if prediction is None:
            return make_response({'error': 'Prediction not found'}, 404)
        
        data = request.get_json()
        prediction.content = data.get('content', prediction.content)
        prediction.date_created = data.get('date_created', prediction.date_created)
        db.session.commit()
        return make_response(prediction.to_dict(), 200)
    
    def delete(self, id):
        prediction = Prediction.query.filter( Prediction.id == id ).first()
        if prediction is None:
            return make_response({'error': 'Prediction not found'}, 404)
        db.session.delete(prediction)
        db.session.commit()
        return make_response('', 204)
    
api.add_resource( PredictionsById, '/predictions/<int:id>')

class Comments(Resource):
    def get(self):
        comments = [comment.to_dict(rules=()) for comment in Comment.query.all()]
        response = make_response(comments, 200)
        return response
    
    def post(self):
        data = request.get_json()
        new_comment = Comment(comment=data['comment'], like=data['like'])
        db.session.add(new_comment)
        db.session.commit()
        return make_response(new_comment.to_dict(), 200)
    
api.add_resource( Comments, '/comments')

class CommentsById(Resource):
    def get(self, id):
        comment = Comment.query.filter( Comment.id == id ).first()
        if comment is None:
            return make_response({'error': 'Comment not found'}, 404)
        return make_response(comment.to_dict(), 200)
    
    def put(self, id):
        comment = Comment.query.filter( Comment.id == id ).first()
        if comment is None:
            return make_response({'error': 'Comment not found'}, 404)
        
        data = request.get_json()
        comment.comment = data.get('comment', comment.comment)
        comment.like = data.get('like', comment.like)
        db.session.commit()
        return make_response(comment.to_dict(), 200)
    
    def delete(self, id):
        comment = Comment.query.filter( Comment.id == id ).first()
        if comment is None:
            return make_response({'error': 'Comment not found'}, 404)
        db.session.delete(comment)
        db.session.commit()
        return make_response('', 204)
    
api.add_resource( CommentsById, '/comments/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
