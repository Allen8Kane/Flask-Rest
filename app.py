import json
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.utils import parse_version

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    profession = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    @property
    def serialize(self):
        return {'id':self.id,'username': self.username, 'profession': self.profession, 'salary': self.salary}


class get_users(Resource):
    def get(self):
        result = []
        users = User.query.order_by(User.username).all()
        for user in users:
            result.append(user.serialize)
        return result


class user(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first_or_404()
        user = user.serialize
        return user
    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first_or_404()
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("profession")
        parser.add_argument("salary")
        params = parser.parse_args()
        user.username = params['username']
        user.profession = params['profession']
        user.salary = params['salary']
        db.session.commit()
        return "user data updated", 201
    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return 'user was deleted',200


class create_user(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("profession")
        parser.add_argument("salary")
        params = parser.parse_args()
        user = User(username=params['username'], profession=params['profession'],salary=params['salary'])
        db.session.add(user)
        db.session.commit()
        return 201

api.add_resource(user, '/user/<int:user_id>')
api.add_resource(get_users, '/users')
api.add_resource(create_user, '/user')
