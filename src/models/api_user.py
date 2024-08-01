from os import getenv
from db import db
from sqlalchemy import exc

import logging

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class API_UserModel(db.Model):
    __tablename__ = "api_users"

    email = db.Column(db.VARCHAR, primary_key=True)
    password = db.Column(db.VARCHAR)
    hits = db.Column(db.INTEGER, default='k')

    def to_json(self)->dict:
        return {
            'email': self.email,
            'password': self.password,
            'hits': self.hits
        }

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by_email(cls, email:str) -> object:
        try:
            row = cls.query.filter_by(email=email).first()
            if row is None:
                raise Exception('Not found')
            return row.to_json()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False