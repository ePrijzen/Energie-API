from os import getenv
from time import time
from db import db
from flask import request
from sqlalchemy import exc
import secrets
import hashlib
from datetime import datetime, timedelta

import logging

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class UserModel(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.INTEGER, primary_key=True)
    datetime = db.Column(db.INTEGER)
    kaal_opslag_allin = db.Column(db.CHAR, default='k')
    ochtend = db.Column(db.INTEGER, default=8)
    middag = db.Column(db.INTEGER, default=16)
    opslag_electra = db.Column(db.Float)
    opslag_gas = db.Column(db.Float)
    melding_lager_dan = db.Column(db.Float, default=0.001)
    ode_gas = db.Column(db.Float)
    ode_electra = db.Column(db.Float)
    eb_electra = db.Column(db.Float)
    eb_gas = db.Column(db.Float)
    country = db.Column(db.VARCHAR, default='NL')
    locale = db.Column(db.CHAR, default='de_DE')
    api_key = db.Column(db.VARCHAR)
    api_price = db.Column(db.Float, default=0.004152778)
    api_calls = db.Column(db.INTEGER, default=740)
    salt_key = db.Column(db.VARCHAR, default='ThEoIsTheBest')
    api_valid_date = db.Column(db.VARCHAR)


    def to_json(self)->dict:
        try:
            return {
                'user_id': self.user_id,
                'datetime': self.datetime,
                'kaal_opslag_allin': self.kaal_opslag_allin,
                'ochtend': self.ochtend,
                'middag': self.middag,
                'opslag_electra': self.opslag_electra,
                'opslag_gas': self.opslag_gas,
                'melding_lager_dan': self.melding_lager_dan,
                'ode_gas': self.ode_gas,
                'ode_electra': self.ode_electra,
                'eb_electra': self.eb_electra,
                'eb_gas': self.eb_gas,
                'country': self.country,
                'locale': self.locale,
                'api_key': self.api_key,
                'api_price': self.api_price,
                'api_calls': self.api_calls,
                'salt_key': self.salt_key,
                'api_valid_date': self.api_valid_date
            }
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by_userid(cls, user_id:int = None) -> object:
        try:
            if user_id is None:
                raise Exception("No User ID given")

            row = cls.query.filter_by(user_id=user_id).first()
            if row is None:
                return False

            data = []
            data.append(row.to_json())
            return data
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def all_users(cls) -> object:
        try:
            data = None
            try:
                data = request.get_json()
            except Exception:
                pass

            if data is None:
                return [user.to_json() for user in cls.query.all()]
            else:
                criteria = {}

                for key, value in data.items():
                    criteria[key] = value

                return [user.to_json() for user in cls.query.filter_by(**criteria).all()]
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def count_users(cls) -> int:
        try:
            return cls.query.count()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def subtract_api_call(cls, user_id:int = None) -> object:
        try:
            if user_id is None:
                raise Exception("No User ID given")

            user = cls.query.filter_by(user_id=user_id).first()
            if user is None:
                return False

            user.api_calls = int(user.api_calls) - 1
            db.session.commit()
            return (user.to_json())

        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def update_user(cls, user_id:int = None) -> object:
        try:
            if user_id is None:
                raise Exception("No User ID given")
            if not request.json:
                raise Exception('Nothing to change')

            user = cls.query.filter_by(user_id=user_id).first()

            if user is None:
                return cls.insert_user(user_id=user_id)

            if user is not None:
                user.kaal_opslag_allin = request.json.get('kaal_opslag_allin', user.kaal_opslag_allin)
                user.ochtend = request.json.get('ochtend', user.ochtend)
                user.middag = request.json.get('middag', user.middag)
                user.opslag_electra = request.json.get('opslag_electra', user.opslag_electra)
                user.opslag_gas = request.json.get('opslag_gas', user.opslag_gas)
                user.melding_lager_dan = request.json.get('melding_lager_dan', user.melding_lager_dan)
                user.ode_gas = request.json.get('ode_gas', user.ode_gas)
                user.ode_electra = request.json.get('ode_electra', user.ode_electra)
                user.eb_electra = request.json.get('eb_electra', user.eb_electra)
                user.eb_gas = request.json.get('eb_gas', user.eb_gas)
                user.country = request.json.get('country', user.country)
                user.locale = request.json.get('locale', user.locale)

                if request.json.get('new_api_key', False):
                    user.salt_key = cls.create_salt()
                    user.api_key = cls.get_api_key(user_id=user_id, salt=user.salt_key)
                else:
                    user.salt_key = request.json.get('salt_key', user.salt_key)
                    user.api_key = request.json.get('api_key', user.api_key)

                user.api_price = request.json.get('api_price', user.api_price)
                user.api_calls = request.json.get('api_calls', user.api_calls)
                user.api_valid_date = request.json.get('api_valid_date', user.api_valid_date)

                db.session.commit()
                return (user.to_json())

            return None
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def insert_user(cls, user_id:int = None) -> object:
        try:
            vandaag_ts = datetime.now()
            dertigdagen = vandaag_ts + timedelta(days=+30)
            dertigdagen = dertigdagen.strftime("%Y-%m-%d")

            if user_id is None:
                raise Exception("No User ID")

            if not request.json:
                raise Exception('No changes')

            user = cls.query.filter_by(user_id=user_id).first()

            if user is None:
                user_id = user_id
                tijdstamp = int(time())
                kaal_opslag_allin = request.json.get('kaal_opslag_allin')
                ochtend = request.json.get('ochtend', None)
                middag = request.json.get('middag', None)
                opslag_electra = request.json.get('opslag_electra', None)
                opslag_gas = request.json.get('opslag_gas', None)
                melding_lager_dan = request.json.get('melding_lager_dan', None)
                ode_gas = request.json.get('ode_gas', None)
                ode_electra = request.json.get('ode_electra', None)
                eb_electra = request.json.get('eb_electra', None)
                eb_gas = request.json.get('eb_gas', None)
                country = request.json.get('eb_gas', "NL")
                locale = request.json.get('locale', ",")

                salt_key = cls.create_salt()
                api_key = cls.get_api_key(user_id=user_id, salt=salt_key)
                api_price = request.json.get('api_price', None)
                api_calls = request.json.get('api_calls', 740)
                api_valid_date = dertigdagen

                me = UserModel(user_id=user_id, datetime=tijdstamp, kaal_opslag_allin=kaal_opslag_allin,
                            ochtend=ochtend, middag=middag, opslag_electra=opslag_electra,
                            opslag_gas=opslag_gas, melding_lager_dan=melding_lager_dan,
                            ode_gas=ode_gas, ode_electra=ode_electra, eb_electra=eb_electra,
                            eb_gas=eb_gas, country=country, locale=locale,
                            salt_key=salt_key,api_key=api_key,api_price=api_price,api_calls=api_calls, api_valid_date=api_valid_date)

                cls.save_to_db(me)
                return (me.to_json())
            else:
                return user.to_json()

            return False
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False


    @classmethod
    def delete_user(cls, user_id:int = None) -> object:
        try:
            if user_id is None:
                raise Exception("No User id")
            user = cls.query.filter_by(user_id=user_id).first()
            if user is None:
                raise Exception(f"User with {user_id} not found")
            db.session.delete(user)
            db.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @staticmethod
    def create_salt(nr:int = 8)->str:
        return secrets.token_hex(nr)

    @staticmethod
    def get_api_key(user_id:str = None, salt:str=None)->str:
            salted_password = str(user_id)+salt
            hashed_password = hashlib.sha3_384(salted_password.encode())
            return hashed_password.hexdigest()
