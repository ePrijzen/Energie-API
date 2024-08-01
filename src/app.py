from datetime import timedelta
import sys
import os
import yaml

from flask import Flask
from flask_restful import Api
from db import db

from flask_jwt_extended import JWTManager
from resources.belasting import Belastingen
from resources.country import Countries
from resources.generation import Generation
from resources.leverancier import Leverancier
from resources.homeassistant import HomeAssistant
from resources.volume import Volume
from resources.user import Users
from resources.login import Login
from resources.prices import Prices
from resources.system import System

import logging
import logging.config
dir_path = os.path.dirname(os.path.realpath(__file__))

database_path = None
config_folder = None
log_folder = None
os.environ['TZ'] = 'Europe/Amsterdam'

PY_ENV = os.getenv('PY_ENV', 'dev')

match PY_ENV:
    case 'dev':
        config_filename = "development.yml"
        # database_path = os.path.join(dir_path, "..", "..", "data")
        database_path = os.path.join(dir_path, "..", "data")
        config_folder = os.path.join(dir_path, "..","config")
        log_folder = os.path.join(dir_path, "..", "logging")

        logging.config.fileConfig(os.path.join(config_folder, 'logging.conf'))
        log = logging.getLogger(PY_ENV)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        sqllg = logging.getLogger('sqlalchemy.engine')
        sqllg.setLevel(logging.INFO)
        wklg = logging.getLogger('werkzeug')
        wklg.setLevel(logging.DEBUG)
    case 'acc':
        config_filename = "acceptance.yml"
        database_path = os.path.join(dir_path, "data")
        config_folder = os.path.join(dir_path, 'config')
        log_folder = os.path.join(dir_path, "logging")

        logging.config.fileConfig(os.path.join(config_folder, 'logging.conf'))
        log = logging.getLogger(PY_ENV)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        sqllg = logging.getLogger('sqlalchemy.engine')
        sqllg.setLevel(logging.DEBUG)
        wklg = logging.getLogger('werkzeug')
        wklg.setLevel(logging.DEBUG)
    case 'prod':
        config_filename = "production.yml"
        database_path = os.path.join(dir_path, "..", "data")
        config_folder = os.path.join(dir_path, "..", "config")
        log_folder = os.path.join(dir_path, "..", "logging")

        logging.config.fileConfig(os.path.join(config_folder, 'logging.conf'))
        log = logging.getLogger(PY_ENV)
        logger = logging.getLogger()
        logger.setLevel(logging.ERROR)
        sqllg = logging.getLogger('sqlalchemy.engine')
        sqllg.setLevel(logging.ERROR)
        wklg = logging.getLogger('werkzeug')
        wklg.setLevel(logging.ERROR)
    case _:
        pass

def check_file(file:str = "")->bool:
    if os.path.exists(file):
        return True
    return False

try:
    config_file = os.path.join(config_folder, config_filename)
    if not check_file(file=config_file):
        raise Exception(f"Config file not found {config_file}")
except Exception as e:
    log.critical(e, exc_info=True)
    sys.exit(e)

config = None
try:
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
except Exception as e:
    log.critical(e, exc_info=True)
    sys.exit(e)

database = os.path.join(database_path, config['db']['name'])

app = Flask(__name__)
try:
    app.config['DEBUG'] = config['API']['debug']
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = config['API']['secret']
    app.config['JWT_SECRET_KEY'] = config['API']['secret']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
except KeyError as e:
    log.critical(e, exc_info=True)
    sys.exit(e)

api = Api(app)

db.init_app(app)
jwt = JWTManager(app) # /auth endpoint
# https://github.com/fmgervasoni/flask-restful-and-sqlalchemy

api.add_resource(Login, '/energy/api/v1.0/login', endpoint="login")
api.add_resource(Users, '/energy/api/v1.0/users', endpoint="users")
api.add_resource(Users, '/energy/api/v1.0/users/<string:user_id>', endpoint="user")
api.add_resource(Prices, '/energy/api/v1.0/prices', endpoint="prices")
api.add_resource(Generation, '/energy/api/v1.0/generation', endpoint="generation")
api.add_resource(System, '/energy/api/v1.0/system', endpoint="system")
api.add_resource(Belastingen, '/energy/api/v1.0/belastingen', endpoint="belastingen")
api.add_resource(Countries, '/energy/api/v1.0/countries', endpoint="countries")
api.add_resource(Leverancier, '/energy/api/v1.0/leveranciers', endpoint="leveranciers")
api.add_resource(Countries, '/energy/api/v1.0/countries/<string:country_id>', endpoint="country")
api.add_resource(Volume, '/energy/api/v1.0/volume', endpoint="volume")
api.add_resource(HomeAssistant, '/energy/api/v1.0/ha', endpoint="homeassistant")

if __name__ == "__main__":
    @app.errorhandler(Exception)
    def server_error(err):
        log.critical(err)

    if app.config["DEBUG"]:
        with app.app_context():
            db.create_all()

    from waitress import serve
    serve(app, host="127.0.0.1", port=5001)
