import os
import logging

from flask_restful import Resource
from models.generation import GenerationModel

from flask_jwt_extended import jwt_required

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Generation(Resource):

    @jwt_required()
    def get(self) -> dict:
        try:
            data = GenerationModel.find_by()
            if data is None:
                raise Exception('id not found!')
            return {'data': data}, 200  # return data and 200 OK code
        except KeyError as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"What do you want?"
            }, 400
        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503

    @jwt_required()
    def put(self):
        try:
            data = GenerationModel.save()
            if data:
               return {'msg': "success"}, 201  # return data and 200 OK code

            raise Exception('Not inserted')

        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503
