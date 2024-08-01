import os
import logging

from flask_restful import Resource
from models.api_user import API_UserModel

from flask_jwt_extended import jwt_required

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class API_Users(Resource):


    def get_user(mail:str=None)->dict:
        return API_UserModel.find_by_email(email=mail)
