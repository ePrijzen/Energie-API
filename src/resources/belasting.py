import os
import logging

from flask_restful import Resource
from models.belasting import BelastingModel

from flask_jwt_extended import jwt_required

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Belastingen(Resource):

    @jwt_required()
    def get(self) -> dict:
        try:
            data = BelastingModel.find_by()
            if data:
                return {'data': data}, 200  # return data and 200 OK code

            raise Exception('Belasting not found!')
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