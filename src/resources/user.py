from os import getenv
import logging

from flask_restful import Resource

from models.belasting import BelastingModel
from models.user import UserModel

from flask_jwt_extended import jwt_required

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Users(Resource):

    @jwt_required()
    def get(self, user_id:int=None) -> dict:
        try:
            if user_id is None:
                users = UserModel.all_users()
            else:
                users = UserModel.find_by_userid(user_id=user_id)

            if not users:
                return {'msg': 'Not Found'}, 404 # User not found!

            belastingen = BelastingModel.find_by_date()
            for index, user in enumerate(users):
                users[index] = self.user_belastingen(user=user, belastingen=belastingen)

            return {'data': users}, 200  # return data and 200 OK code
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
    def put(self, user_id:int)->dict:
        try:
            # if get_jwt_identity() == priceprocess@itheo.tech or in ['priceprocess@itheo.tech']

            data = UserModel.insert_user(user_id=user_id)
            if data:
                return {"msg": "succes"}, 201
            else:
                raise Exception(f"Failure")
        except Exception as e:
            log.error(f"{e} user ID {user_id}, data {data}", exc_info=True)
            return {
                'msg': f"{e}"
            }, 503

    @jwt_required()
    def patch(self, user_id:int) -> dict:
        try:
            data = UserModel.update_user(user_id=user_id)
            if data:
                return {'data': data}, 200  # return data and 200 OK code

            raise Exception('id not found!')

        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503

    @jwt_required()
    def delete(self, user_id:int) -> dict:
        try:
            data = UserModel.delete_user(user_id=user_id)
            if data:
               return "", 204  # return data and 200 OK code

            raise Exception('id not found!')
        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503


    @staticmethod
    def user_belastingen(user:dict = None, belastingen:dict=None)->dict:
        try:
            for belasting in belastingen:
                if belasting['kind'] == 'g':
                    opslag_g = float(belasting['opslag'])
                    ode_g = float(belasting['ode'])
                    eb_g = float(belasting['eb'])
                    # btw_g = float(belasting['btw'])

                elif belasting['kind'] == 'e':
                    opslag_e = float(belasting['opslag'])
                    ode_e = float(belasting['ode'])
                    eb_e = float(belasting['eb'])
                    btw_e = float(belasting['btw'])

            if user is not None:
                user = {
                    key: value for key, value in user.items() if value is not None
                }
                user['kaal_opslag_allin'] = user.get('kaal_opslag_allin', 'k')
                user['opslag_electra'] = user.get('opslag_electra', opslag_e)
                user['opslag_gas'] = user.get('opslag_gas', opslag_g)
                user['ode_gas'] = user.get('ode_gas', ode_g)
                user['ode_electra'] = user.get('ode_electra', ode_e)
                user['eb_gas'] = user.get('eb_gas', eb_g)
                user['eb_electra'] = user.get('eb_electra', eb_e)
                user['btw'] = user.get('btw', btw_e)

            return user
        except Exception as e:
            log.warning(e, exc_info=True)
