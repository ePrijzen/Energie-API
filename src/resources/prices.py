import os
import logging

# from datetime import datetime
# import pytz

from flask_restful import Resource
from models.price import PriceModel
from flask import request

# local = pytz.timezone("Europe/Amsterdam")

from flask_jwt_extended import jwt_required

from models.user import UserModel

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)


class Prices(Resource):

    @jwt_required()
    def get(self) -> dict:
        try:
            lowest = request.json.get('lowest', False)
            highest = request.json.get('highest', False)
            average = request.json.get('highest', False)
            user_id = request.json.get('user_id', None)
            dutch_floats = request.json.get('dutch_floats', False)
            user = None
            user_locale = "nl_NL"
            if user_id is not None:
                if(user_data := UserModel.find_by_userid(user_id=user_id)):
                    try:
                        #let op dit is ruwe data dus geen ['data']
                        user = user_data[0]
                        user_locale = user['locale']
                    except Exception:
                        # no user available
                        pass

            if lowest:
                price_data = PriceModel.lowest()
            elif highest:
                price_data = PriceModel.highest()
            elif average:
                price_data = PriceModel.average()
            else:
                price_data = PriceModel.find_by()

            if price_data is None or not price_data:
                raise Exception('Did not get any Price Data!')

            user_belastingen = PriceModel.user_belastingen(user=user)

            if(price_data := self.calc_price_data(price_data=price_data, user_belastingen=user_belastingen, user_locale=user_locale, dutch_floats=dutch_floats)):
                return {'data': price_data}, 200  # return data and 200 OK code

            return {
                'msg': f"No data, sorry!"
            }, 406
        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503

    @jwt_required()
    def put(self):
        try:
            data = PriceModel.insert_price()
            if data:
               return {'msg': "success"}, 201  # return data and 200 OK code

            raise Exception('Not inserted')

        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503

    @staticmethod
    def calc_price_data(price_data:dict, user_belastingen:dict, user_locale:str, dutch_floats:bool)->dict:
        try:
            for i in range(len(price_data)):
                inkoop_price = price_data[i]['price']
                opslag_price_dict = PriceModel.opslag_price(user_belastingen=user_belastingen, price_line=price_data[i])

                all_in_price_dict = PriceModel.all_in_price(user_belastingen=user_belastingen, price_line=price_data[i], opslag_price_dict=opslag_price_dict)

                opslag_price = opslag_price_dict['prijs_plus_opslag_plus_btw']
                all_in_price = all_in_price_dict['all_in_prijs']
                btw_total = all_in_price_dict['btw_total']

                if dutch_floats:
                    inkoop_price = PriceModel.dutch_floats(inkoop_price, my_locale=user_locale)
                    opslag_price = PriceModel.dutch_floats(opslag_price, my_locale=user_locale)
                    all_in_price = PriceModel.dutch_floats(all_in_price, my_locale=user_locale)
                    btw_total = PriceModel.dutch_floats(btw_total, my_locale=user_locale)

                price_data[i]['price'] = inkoop_price
                price_data[i]['opslag_price'] = opslag_price
                price_data[i]['all_in_price'] = all_in_price
                price_data[i]['opslag'] = opslag_price_dict['opslag']
                price_data[i]['ode'] = all_in_price_dict['ode']
                price_data[i]['eb'] = all_in_price_dict['eb']
                price_data[i]['btw_perc'] = all_in_price_dict['btw_perc']
                price_data[i]['btw_total'] = btw_total

            return price_data
        except Exception as e:
            log.error(e, exc_info=True)
            return False