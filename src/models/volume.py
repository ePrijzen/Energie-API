from datetime import datetime
from os import getenv
from flask import request
from db import db
from sqlalchemy import exc

import logging

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class VolumeModel(db.Model):
    __tablename__ = "volume"

    fromdate = db.Column(db.VARCHAR, primary_key=True)
    e = db.Column(db.Float)
    g = db.Column(db.Float)

    def to_json(self)->dict:
        return {
            'fromdate': self.fromdate,
            'e': self.e,
            'g': self.g
        }

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by_date(cls, datum:str = None) -> object:
        try:
            if datum is None:
                vandaag_ts = datetime.now()
                vandaag = vandaag_ts.strftime("%Y-%m-%d")

            data = {}
            data['fromdate'] = request.json.get('datum', vandaag)

            criteria = {}
            for key, value in data.items():
                if value is None or value == "":
                    continue
                criteria[key] = value

            return [volume.to_json() for volume in  cls.query.filter_by(**criteria).all()]
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_to_date(cls, vandaag:str=None) -> object:
        try:
            if vandaag is None:
                vandaag_ts = datetime.now()
                vandaag = vandaag_ts.strftime("%Y-%m-%d")
                maand_start = vandaag_ts.strftime("%Y-%m-01")
            else:
                datum_ts = datetime.strptime(vandaag, "%Y-%m-%d")
                maand_start = datum_ts.strftime("%Y-%m-01")

            query = db.session.query( db.func.sum(VolumeModel.e).label('e'),  db.func.sum(VolumeModel.g).label('g'), db.func.strftime('%m', VolumeModel.fromdate).label('maand') ) \
                                  .select_from(VolumeModel)\
                                  .filter(VolumeModel.fromdate.between(maand_start, vandaag)) \
                                  .group_by(db.func.strftime('%m', VolumeModel.fromdate))

            data = []
            for row in query:
                data.append({
                    'maand': row._mapping['maand'],
                    'e': row._mapping['e'],
                    'g': row._mapping['g'],
                })

            return data
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by_month(cls, jaar_maand:str="") -> object:
        try:
            if not jaar_maand:
                vandaag_ts = datetime.now()
                jaar_maand = vandaag_ts.strftime("%Y-%m")

            query = db.session.query( db.func.sum(VolumeModel.e).label('e'),  db.func.sum(VolumeModel.g).label('g'), db.func.strftime('%m', VolumeModel.fromdate).label('maand') ) \
                                  .select_from(VolumeModel)\
                                  .filter(db.func.strftime('%Y-%m', VolumeModel.fromdate) == jaar_maand) \
                                  .group_by(db.func.strftime('%m', VolumeModel.fromdate))

            data = []
            for row in query:
                data.append({
                    'maand': row._mapping['maand'],
                    'e': row._mapping['e'],
                    'g': row._mapping['g'],
                })

            return data
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False
