from os import getenv
from db import db
from sqlalchemy import exc
from flask import request
from datetime import datetime

import logging

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class LeverancierModel(db.Model):
    __tablename__ = "leveranciers"

    leverancier = db.Column(db.VARCHAR, primary_key=True)
    fromdate = db.Column(db.VARCHAR(10), primary_key=True)
    kind = db.Column(db.VARCHAR(2), primary_key=True)
    price = db.Column(db.Float)
    country = db.Column(db.VARCHAR(10), primary_key=True)

    def to_json(self)->dict:
        return {
            'leverancier': self.leverancier,
            'fromdate': self.fromdate,
            'kind': self.kind,
            'price': self.price,
            'country': self.country
        }

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by(cls)->list:
        try:
            if not request.json:
                raise Exception('Nothing to search for')

            vandaag_ts = datetime.now()
            vandaag = vandaag_ts.strftime("%Y-%m-%d")

            data = {}
            data['fromdate'] = request.json.get('fromdate', vandaag)
            data['kind'] = request.json.get('kind', None)
            data['country'] = request.json.get('country', None)

            criteria = {}
            for key, value in data.items():
                if value is None or value == "":
                    continue
                criteria[key] = value

            query = cls.query.filter_by(**criteria).all()
            return [leverancier.to_json() for leverancier in query]

        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def save(cls) -> object:
        if not request.json:
            raise Exception('No changes')
        try:
            fromdate = request.json.get('fromdate')
            leverancier = request.json.get('leverancier')
            kind = request.json.get('kind')
            price = request.json.get('price')
            country = request.json.get('country', "NL")

            generation_cls= cls.query.filter_by(fromdate=fromdate, leverancier=leverancier, kind=kind, country=country).first()

            if generation_cls is not None:
                return True

            me = LeverancierModel(fromdate=fromdate, leverancier=leverancier, kind=kind, price=price, country=country)
            cls.save_to_db(me)

            return (me.to_json())
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False