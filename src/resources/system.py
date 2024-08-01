import os
import logging

from flask_restful import Resource
from models.user import UserModel
from models.price import PriceModel

from flask_jwt_extended import jwt_required

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class System(Resource):
    @jwt_required()
    def get(self) -> dict:
        num_users = UserModel.count_users()
        eerste_e_prijs = PriceModel.find_first(kind='e')
        eerste_g_prijs = PriceModel.find_first(kind='g')
        data = {}
        data['num_users'] = num_users
        data['first_gas_date'] = eerste_g_prijs[0]['fromdate']
        data['first_gas_price'] =  eerste_g_prijs[0]['price']
        data['first_electra_date'] = eerste_e_prijs[0]['fromdate']
        data['first_electra_price'] = eerste_e_prijs[0]['price']
        return {'data': data}, 200
