from datetime import datetime
from os import getenv
from flask import request
from db import db
from sqlalchemy import exc

import logging

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class BelastingModel(db.Model):
    __tablename__ = "belastingen"

    kind = db.Column(db.VARCHAR, primary_key=True)
    btw = db.Column(db.Float)
    opslag = db.Column(db.Float)
    ode = db.Column(db.Float)
    eb = db.Column(db.Float)
    datum = db.Column(db.VARCHAR(10), primary_key=True)

    def to_json(self)->dict:
        return {
            'kind': self.kind,
            'btw': self.btw,
            'opslag': self.opslag,
            'ode': self.ode,
            'eb': self.eb,
            'datum': self.datum
        }

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by(cls) -> object:
        try:
            vandaag_ts = datetime.now()
            vandaag = vandaag_ts.strftime("%Y-%m-%d")

            data = {}
            data['datum'] = request.json.get('datum', vandaag)
            data['kind'] = request.json.get('kind', None)

            criteria = {}
            for key, value in data.items():
                if value is None or value == "":
                    continue
                criteria[key] = value

            return [belasting.to_json() for belasting in  cls.query.filter_by(**criteria).all()]
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by_date(cls, datum:str = None) -> object:
        try:
            if datum is None:
                vandaag_ts = datetime.now()
                datum = vandaag_ts.strftime("%Y-%m-%d")

            data = {}
            data['datum'] = datum

            criteria = {}
            for key, value in data.items():
                if value is None or value == "":
                    continue
                criteria[key] = value

            return [belasting.to_json() for belasting in  cls.query.filter_by(**criteria).all()]
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False