import os
import logging
from flask import request
from flask_restful import Resource
from models.volume import VolumeModel

from flask_jwt_extended import jwt_required

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Volume(Resource):

    @jwt_required()
    def get(self) -> dict:
        try:
            if (datum := request.json.get('huidig', False)):
                data = VolumeModel.find_to_date(vandaag=datum)
            elif (jaar_maand := request.json.get('jaar_maand', False)):
                data = VolumeModel.find_by_month(maand=jaar_maand)
            else:
                data = VolumeModel.find_by_date(datum)

            if data:
                return {'data': data}, 200  # return data and 200 OK code

            raise Exception('Volume not found!')
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