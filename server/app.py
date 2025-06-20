#!/usr/bin/env python3

from flask import request, session, make_response,jsonify
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


class CheckSession(Resource):
    def get(self):
        user_id = session["user_id"]
        if not user_id:
            return make_response('', 204)
        
        user = User.query.filter_by(id=user_id).first().to_dict()

        response = make_response(jsonify(user), 200)

        return response
        
        
class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")


        user = User.query.filter_by(username=username).first()

        if not user.authenticate(password):
            return make_response(jsonify({"error": "Invalid credentials"}), 401)

        session["user_id"] = user.id  
        return make_response(jsonify(user.to_dict()), 200)


class Logout(Resource):
    def delete(self):
    
        session['user_id'] = None

        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
