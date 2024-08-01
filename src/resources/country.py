import os
import logging

from flask_restful import Resource
from models.country import CountryModel

from flask_jwt_extended import jwt_required

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Countries(Resource):

    @jwt_required()
    def get(self, country_id:int=None) -> dict:
        try:
            if country_id is None:
                data = CountryModel.all_countries()
            else:
                data = CountryModel.find_by_countryid(country_id=country_id)
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