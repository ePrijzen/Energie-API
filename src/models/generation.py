from os import getenv
from db import db
from sqlalchemy import exc
from flask import request
from datetime import datetime

import logging

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class GenerationModel(db.Model):
    __tablename__ = "generation"

    fromdate = db.Column(db.VARCHAR(10), primary_key=True)
    fromtime = db.Column(db.VARCHAR(5), primary_key=True)
    kind = db.Column(db.VARCHAR(5), primary_key=True)
    mw = db.Column(db.INTEGER)
    country = db.Column(db.VARCHAR, db.ForeignKey('countries.country_id'), primary_key=True)

    def to_json(self)->dict:
        return {
            'fromdate': self.fromdate,
            'fromtime': self.fromtime,
            'kind': self.kind,
            'mw': self.mw,
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
            data['fromtime'] = request.json.get('fromtime', None)
            data['kind'] = request.json.get('kind', None)
            data['country'] = request.json.get('country', None)

            criteria = {}
            for key, value in data.items():
                if value is None or value == "":
                    continue
                criteria[key] = value

# SELECT g.fromdate, g.fromtime, sum(g.mw), g.kind, g.country
# FROM generation as g
# WHERE g.fromdate = '2022-10-17'
# AND g.country = 'NL'
# AND g.kind = 's'
# GROUP BY g.fromdate, strftime ('%H',g.fromtime);

            query = db.session.query(cls.fromdate, cls.fromtime, cls.kind, cls.country, db.func.sum(cls.mw).label('mw')) \
                            .filter_by(**criteria).group_by(cls.fromdate, db.func.strftime('%H', cls.fromtime), cls.kind)
            # return [price.to_json() for price in query]
            data = []
            for gen in query.all():
                data.append({
                    'fromdate': gen[0],
                    'fromtime': gen[1],
                    'kind': gen[2],
                    'country': gen[3],
                    'mw': gen[4]
                })
            return data

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
            fromtime = request.json.get('fromtime')
            kind = request.json.get('kind')
            mw = request.json.get('mw')
            country = request.json.get('country', "NL")

            generation_cls= cls.query.filter_by(fromdate=fromdate, fromtime=fromtime, kind=kind, country=country).first()

            if generation_cls is not None:
                return True

            me = GenerationModel(fromdate=fromdate, fromtime=fromtime, kind=kind, mw=mw, country=country)
            cls.save_to_db(me)

            return (me.to_json())
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False