from os import getenv
from db import db
from sqlalchemy import exc

import logging

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class CountryModel(db.Model):
    __tablename__ = "countries"

    # country_id = db.Column(db.VARCHAR, db.ForeignKey("energy.country"), primary_key=True)
    # country_iso = db.Column(db.VARCHAR)
    # country = db.Column(db.VARCHAR, default='k')

    country_id = db.Column(db.VARCHAR, primary_key=True)
    country_iso = db.Column(db.VARCHAR)
    country = db.Column(db.VARCHAR, default='k')

    def to_json(self)->dict:
        return {
            'country_id': self.country_id,
            'country_iso': self.country_iso,
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
    def find_by_countryid(cls, country_id:str) -> object:
        try:
            row = cls.query.filter_by(country_id=country_id).first()
            if row is None:
                raise Exception('Not found')
            return row.to_json()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def all_countries(cls) -> object:
        try:
            return [country.to_json() for country in cls.query.all()]
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False