import os
import logging
from flask import request

from flask_restful import Resource
from models.user import UserModel
from models.price import PriceModel
from resources.prices import Prices

from datetime import datetime, timedelta

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class HomeAssistant(Resource):
    def post(self)->dict:
        try:
            return self.HA()
        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503

    def get(self)->dict:
        try:
            return self.HA()
        except Exception as e:
            log.error(e, exc_info=True)
            return {
                'msg': f"{e}"
            }, 503

    @staticmethod
    def prep_data(price_data:dict, country:str="NL")->dict:
        try:
            for i in range(len(price_data)):
                price_data[i]['datetime'] = f"{price_data[i]['fromdate']}T{price_data[i]['fromtime']}:00"
                price_data[i]['purchase_price'] = price_data[i]['price']
                price_data[i]['extra_fee_price'] = price_data[i]['opslag_price']

                del price_data[i]['price']
                del price_data[i]['opslag']
                del price_data[i]['ode']
                del price_data[i]['country']
                del price_data[i]['eb']
                del price_data[i]['btw']
                del price_data[i]['btw_perc']
                del price_data[i]['btw_total']
                del price_data[i]['kind']
                del price_data[i]['fromdate']
                del price_data[i]['opslag_price']
                del price_data[i]['fromtime']

                if country != "NL":
                    del price_data[i]['opslag_price']
                    del price_data[i]['all_in_price']

            if len(price_data) == 1:
                return price_data[0]

            return price_data
        except Exception as e:
            log.error(e, exc_info=True)
            return False

    def HA(self)->dict:
        try:

            """
            {"user_id": ,
            "api_key": "",
            "soort": "e",
            "datum": "2022-11-11",
            "totdatum": "2022-11-12",
            "land": "NL",
            "munt": false
            }
"""
            user_id = None
            api_key = None

            data = 0
            try:
                user_id = request.json.get('user_id', None)
                api_key = request.json.get('api_key', None)
                data = 1
            except Exception as e:
                pass

            if data == 0:
                try:
                    user_id = request.args.get('user_id', None)
                    api_key = request.args.get('api_key', None)
                    data = 1
                except Exception as e:
                    pass

            if data == 0:
                try:
                    user_id = request.data.get('user_id', None)
                    api_key = request.data.get('api_key', None)
                    data = 1
                except Exception as e:
                    pass

            if user_id is None or api_key is None:
                log.error(f"{request}")
                return {'msg': 'Sorry, wrong credentials'}, 401

            if(user := UserModel.find_by_userid(user_id=user_id)):
                user = user[0]
                if user['api_key'] != api_key:
                    return {'msg': 'Sorry, wrong credentials'}, 401

            if user['api_calls'] <= 0:
                return {'msg': 'Sorry, you are out of api calls please buy new api calls'}, 401

            vandaag_ts = datetime.now()
            vandaag = vandaag_ts.strftime("%Y-%m-%d")
            morgen_strf = vandaag_ts + timedelta(days=+1)
            morgen = morgen_strf.strftime("%Y-%m-%d")
            korte_tijd = int(vandaag_ts.strftime("%H"))
            data = 0
            if data == 0:
                try:
                    fromdate = request.json.get('date', vandaag)
                    todate = request.json.get('todate', morgen)
                    fromtime = request.json.get('time', None)
                    country = request.json.get('country', "NL")
                    dutch_floats = request.json.get('currency', False)
                    data = 1
                except Exception as e:
                    pass

            if data == 0:
                try:
                    fromdate = request.data.get('date', vandaag)
                    todate = request.data.get('todate', morgen)
                    fromtime = request.data.get('time', None)
                    country = request.data.get('country', "NL")
                    dutch_floats = request.data.get('currency', False)
                    data = 1
                except Exception as e:
                    pass

            if data == 0:
                try:
                    fromdate = request.args.get('date', vandaag)
                    todate = request.args.get('todate', morgen)
                    fromtime = request.args.get('time', None)
                    country = request.args.get('country', "NL")
                    dutch_floats = request.args.get('currency', False)
                    data = 1
                except Exception as e:
                    pass

            if data == 0:
                raise Exception(f"{request}")

            user_belastingen = PriceModel.user_belastingen(user=user)
            data = 0
            stroom_data = None
            gas_data = None
            kind = 'e'
            if(price_data := PriceModel.find(fromdate=fromdate, todate=todate, fromtime=fromtime, kind=kind, country=country)):
                if(stroom_data := Prices.calc_price_data(price_data=price_data, user_belastingen=user_belastingen, user_locale= user['locale'], dutch_floats=dutch_floats)):
                    stroom_data = self.prep_data(price_data=price_data, country=country)
                    data = 1

            kind = 'g'
            if(price_data := PriceModel.find(fromdate=fromdate, todate=todate, fromtime=fromtime, kind=kind, country=country)):
                if(gas_data := Prices.calc_price_data(price_data=price_data, user_belastingen=user_belastingen, user_locale= user['locale'], dutch_floats=dutch_floats)):
                    gas_data = self.prep_data(price_data=price_data, country=country)
                    data += 1

            if data > 0:
                UserModel.subtract_api_call(user_id=user_id)
                data = {"e": stroom_data, "g": gas_data}
                return { "message":"Success", "data": data}, 200  # return data and 200 OK code

            return {
                'msg': f"No data, sorry!"
            }, 406
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

