
import os
import logging

from flask import request, current_app, jsonify
from flask_restful import Resource

from flask_jwt_extended import create_access_token

from resources.api_user import API_Users


PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Login(Resource):

  def post(self):

    if request.is_json:
        email = request.json['email']
        password = request.json['password']

        user = API_Users.get_user(mail=email)
        if user and email == user["email"] and password == user["password"]:
            access_token = create_access_token(identity=email)
            return jsonify(msg='Login Successful', access_token=access_token)

        return {
            'msg': f"Bad email or Password, do you have a login for this?"
            }, 401

    else:
        return  {
           'msg': f"You have to fill in email and password credentials to get a bearer token!"
           }, 401
