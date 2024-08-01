import locale
from os import getenv
from db import db
from flask import request
from sqlalchemy import exc

from datetime import datetime, timedelta

import logging
from models.belasting import BelastingModel
from models.country import CountryModel

PY_ENV = getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class PriceModel(db.Model):
    __tablename__ = "energy"

    fromdate = db.Column(db.VARCHAR(10), primary_key=True)
    fromtime = db.Column(db.VARCHAR(5), primary_key=True)
    kind = db.Column(db.VARCHAR(5), primary_key=True)
    country = db.Column(db.VARCHAR, primary_key=True)
    price = db.Column(db.Float)

    def to_json(self)->dict:
        return {
            'fromdate': self.fromdate,
            'fromtime': self.fromtime,
            'kind': self.kind,
            'country': self.country,
            'price': self.price
        }

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find(cls, **data) -> list:
        try:

            query = db.session.query(PriceModel.fromdate.label('fromdate'), PriceModel.fromtime.label('fromtime'), PriceModel.kind.label('kind'), \
                                        PriceModel.price.label('price') , BelastingModel.btw.label('btw'), BelastingModel.opslag.label('opslag'), \
                                        PriceModel.country.label('country'), BelastingModel.ode.label('ode'), BelastingModel.eb.label('eb'))\
                                  .select_from(PriceModel)\
                                  .join(CountryModel, PriceModel.country == CountryModel.country_id) \
                                  .join(BelastingModel, (PriceModel.kind == BelastingModel.kind) & (PriceModel.fromdate == BelastingModel.datum)) \

            if data['todate'] is not None:
                query = query.filter(PriceModel.fromdate.between(data['fromdate'], data['todate']))
            else:
                query = query.filter(PriceModel.fromdate == data['fromdate'])

            if data['kind'] is not None:
                query = query.filter(PriceModel.kind == data['kind'])
            if data['country'] is not None:
                query = query.filter(PriceModel.country == data['country'])
            if data['fromtime'] is not None:
                query = query.filter(PriceModel.fromtime == data['fromtime'])

            data = []
            for row in query:
                data.append({
                    'fromdate': row._mapping['fromdate'],
                    'fromtime': row._mapping['fromtime'],
                    'kind': row._mapping['kind'],
                    'country': row._mapping['country'],
                    'price': row._mapping['price'],
                    'btw': row._mapping['btw'],
                    'opslag': row._mapping['opslag'],
                    'ode': row._mapping['ode'],
                    'eb': row._mapping['eb'],
                })

            return data
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_by(cls)->list:
        try:
            if not request.json:
                raise Exception('Nothing to search for')
            vandaag_ts = datetime.now()
            vandaag = vandaag_ts.strftime("%Y-%m-%d")
            morgen_strf = vandaag_ts + timedelta(days=+1)
            morgen = morgen_strf.strftime("%Y-%m-%d")

            data = {}
            data['fromdate'] = request.json.get('fromdate', vandaag)
            data['fromtime'] = request.json.get('fromtime', None)
            data['kind'] = request.json.get('kind', None)
            data['country'] = request.json.get('country', None)

            if data['country'] == "":
                data['country'] = None

            if data['kind'] == 'g' and data['fromtime'] is None:
                data['fromtime'] = "23:00"

            if data['fromtime'] == "":
                data['fromtime'] = None

            average = request.json.get('average', False)
            todate = request.json.get('todate', False)
            group_by = request.json.get('group_by', False)

            # Home assistent
            hacs = request.json.get('ha', None)
            if hacs is not None:
                data['fromdate'] = vandaag
                todate = morgen

            criteria = {}
            for key, value in data.items():
                if value is None or value == "":
                    continue
                criteria[key] = value

            #  for HA usage only
            if hacs is not None:
                query = db.session.query(PriceModel.fromdate.label('fromdate'), PriceModel.fromtime.label('fromtime'), PriceModel.kind.label('kind'), \
                                        PriceModel.price.label('price') , BelastingModel.btw.label('btw'), BelastingModel.opslag.label('opslag'), \
                                        PriceModel.country.label('country'), BelastingModel.ode.label('ode'), BelastingModel.eb.label('eb'))\
                                  .select_from(PriceModel)\
                                  .join(CountryModel, PriceModel.country == CountryModel.country_id) \
                                  .join(BelastingModel, (PriceModel.kind == BelastingModel.kind) & (PriceModel.fromdate == BelastingModel.datum)) \
                                  .filter(PriceModel.fromdate.between(data['fromdate'], todate))
                                #   .filter_by(**criteria) \
                if data['kind'] is not None:
                    query = query.filter(PriceModel.kind == data['kind'])
                if data['country'] is not None:
                    query = query.filter(PriceModel.country == data['country'])
                if data['fromtime'] is not None:
                    query = query.filter(PriceModel.fromtime == data['fromtime'])

            # Average and not Todate
            elif average and not todate:
                query = db.session.query(PriceModel.fromdate.label('fromdate'), PriceModel.fromtime.label('fromtime'), PriceModel.kind.label('kind'), \
                                         PriceModel.country.label('country'), db.func.avg(PriceModel.price).label('price') , \
                                         BelastingModel.btw.label('btw'), BelastingModel.opslag.label('opslag'), BelastingModel.ode.label('ode'), BelastingModel.eb.label('eb') ) \
                                  .select_from(PriceModel)\
                                  .filter_by(**criteria) \
                                  .join(CountryModel, PriceModel.country == CountryModel.country_id) \
                                  .join(BelastingModel, (PriceModel.kind == BelastingModel.kind) & (PriceModel.fromdate == BelastingModel.datum)) \
                                  .group_by(CountryModel.country_iso, PriceModel.kind, PriceModel.fromdate) \
                                  .order_by(db.func.avg(PriceModel.price))
            # Not Average and Todate
            elif not average and todate:
                query = db.session.query(PriceModel.fromdate.label('fromdate'), PriceModel.fromtime.label('fromtime'), PriceModel.kind.label('kind'), \
                                         PriceModel.country.label('country'), PriceModel.price.label('price') , \
                                         BelastingModel.btw.label('btw'), BelastingModel.opslag.label('opslag'), BelastingModel.ode.label('ode'), BelastingModel.eb.label('eb') )\
                                  .select_from(PriceModel)\
                                  .join(BelastingModel, (PriceModel.kind == BelastingModel.kind) & (PriceModel.fromdate == BelastingModel.datum))\
                                  .filter(PriceModel.fromdate.between(data['fromdate'], todate))

                if data['kind'] is not None:
                    query = query.filter(PriceModel.kind == data['kind'])
                if data['country'] is not None:
                    query = query.filter(PriceModel.country == data['country'])

                # er is EEN tijd ingevuld!
                if data['fromtime'] is not None and data['fromtime'] != "":
                    query = query.filter(PriceModel.fromtime == data['fromtime'])

            elif todate and average:
                if group_by and group_by == "ym":
                    query = db.session.query(db.func.strftime('%Y-%m-01', PriceModel.fromdate).label('fromdate'), \
                                         PriceModel.fromtime.label('fromtime'), PriceModel.kind.label('kind'), \
                                         PriceModel.country.label('country'),  db.func.avg(PriceModel.price).label('price') , \
                                         BelastingModel.btw.label('btw'), BelastingModel.opslag.label('opslag'), BelastingModel.ode.label('ode'), BelastingModel.eb.label('eb') )\
                                  .select_from(PriceModel)\
                                  .join(BelastingModel, (PriceModel.kind == BelastingModel.kind) & (PriceModel.fromdate == BelastingModel.datum))

                    query = query.filter(PriceModel.fromdate.between(data['fromdate'], todate))

                    if data['kind'] is not None:
                        query = query.filter(PriceModel.kind == data['kind'])
                    if data['country'] is not None:
                        query = query.filter(PriceModel.country == data['country'])

                    query = query.group_by(db.func.strftime('%Y', PriceModel.fromdate), db.func.strftime('%m', PriceModel.fromdate))

                else:
                    query = db.session.query(PriceModel.fromdate.label('fromdate'), \
                                         PriceModel.fromtime.label('fromtime'), PriceModel.kind.label('kind'), \
                                         PriceModel.country.label('country'),  db.func.avg(PriceModel.price).label('price') , \
                                         BelastingModel.btw.label('btw'), BelastingModel.opslag.label('opslag'), BelastingModel.ode.label('ode'), BelastingModel.eb.label('eb') )\
                                  .select_from(PriceModel)\
                                  .join(BelastingModel, (PriceModel.kind == BelastingModel.kind) & (PriceModel.fromdate == BelastingModel.datum))

                    query = query.filter(PriceModel.fromdate.between(data['fromdate'], todate))

                    if data['kind'] is not None:
                        query = query.filter(PriceModel.kind == data['kind'])
                    if data['country'] is not None:
                        query = query.filter(PriceModel.country == data['country'])

                    if group_by and group_by == "ft":
                        query = query.group_by(PriceModel.fromtime)
                    else:
                        query = query.group_by(PriceModel.fromdate)
            else:
                query = db.session.query(PriceModel.fromdate.label('fromdate'), PriceModel.fromtime.label('fromtime'), PriceModel.kind.label('kind'), \
                                         PriceModel.country.label('country'), PriceModel.price.label('price') , \
                                         BelastingModel.btw.label('btw'), BelastingModel.opslag.label('opslag'), BelastingModel.ode.label('ode'), BelastingModel.eb.label('eb') )\
                                  .select_from(PriceModel)\
                                  .join(BelastingModel, (PriceModel.kind == BelastingModel.kind) & (PriceModel.fromdate == BelastingModel.datum))

                for key, value in data.items():
                    if value is None or value == "":
                        continue
                    match key:
                        case 'fromdate':
                            query = query.filter(PriceModel.fromdate == value)
                        case 'fromtime':
                            query = query.filter(PriceModel.fromtime == value)
                        case 'kind':
                            query = query.filter(PriceModel.kind == value)
                        case 'country':
                            query = query.filter(PriceModel.country == value)

            data = []
            for row in query:
                data.append({
                    'fromdate': row._mapping['fromdate'],
                    'fromtime': row._mapping['fromtime'],
                    'kind': row._mapping['kind'],
                    'country': row._mapping['country'],
                    'price': row._mapping['price'],
                    'btw': row._mapping['btw'],
                    'opslag': row._mapping['opslag'],
                    'ode': row._mapping['ode'],
                    'eb': row._mapping['eb'],
                })

            return data

        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def lowest(cls)->list:
        try:
            if not request.json:
                raise Exception('Nothing to search for')
            data = cls.find_by()
            return [min(data, key=lambda item: float(item['price']))]
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def average(cls)->list:
        try:
            if not request.json:
                raise Exception('Nothing to search for')

            return cls.find_by()
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def highest(cls)->list:
        try:
            if not request.json:
                raise Exception('Nothing to search for')

            data = cls.find_by()
            return [max(data, key=lambda item: float(item['price']))]
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @classmethod
    def find_first(cls, kind:str=None, country:str="NL")->list:
        try:
            row = cls.query.filter_by(kind=kind, country=country).order_by(db.asc(cls.fromdate)).first()
            if row is None:
                raise Exception("Not found")
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
    def insert_price(cls) -> object:
        if not request.json:
            raise Exception('No changes')
        try:
            fromdate = request.json.get('fromdate')
            fromtime = request.json.get('fromtime')
            kind = request.json.get('kind')
            price = request.json.get('price')
            country = request.json.get('country', "NL")

            price_cls = cls.query.filter_by(fromdate=fromdate,fromtime=fromtime,kind=kind,country=country).first()

            if price_cls is not None:
                return True

            me = PriceModel(fromdate=fromdate, fromtime=fromtime, kind=kind, price=price,country=country)
            cls.save_to_db(me)

            return (me.to_json())
        except exc.SQLAlchemyError as e:
            log.error(e, exc_info=True)
            return False
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False


    @staticmethod
    def user_belastingen(user:dict = None)->dict:
        try:

            if user is not None:
                try:
                    user = {
                        key: value for key, value in user.items() if value is not None
                    }
                    opslag_e = user.get('opslag_electra', None)
                    ode_e = user.get('ode_electra', None)
                    eb_e = user.get('eb_electra', None)

                    opslag_g = user.get('opslag_gas', None)
                    ode_g = user.get('ode_gas', None)
                    eb_g = user.get('eb_gas', None)
                    return {'e': {'opslag': opslag_e, 'ode': ode_e, 'eb_e': eb_e}, 'g': {'opslag': opslag_g, 'ode': ode_g, 'eb_e': eb_g}}
                except (KeyError,Exception):
                    pass

            return False

        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @staticmethod
    def all_in_price(user_belastingen:dict = None, price_line:dict = None, opslag_price_dict:dict = None)->float:
        try:
            if price_line is None:
                raise Exception("PriceLine is None")
            if opslag_price_dict is None:
                raise Exception("OpslagPriceDict is None")

            ode = price_line['ode']
            eb = price_line['eb']
            if user_belastingen:
                try:
                    if user_belastingen[price_line['kind']]['ode'] is not None:
                        ode = user_belastingen[price_line['kind']]['ode']
                except KeyError:
                    pass
                try:
                    if user_belastingen[price_line['kind']]['eb'] is not None:
                        eb = user_belastingen[price_line['kind']]['eb']
                except KeyError:
                    pass

            btw = (int(price_line['btw'])/100)

            ode_btw = ode*btw
            eb_btw = eb*btw

            btw_total = ode_btw+eb_btw+opslag_price_dict['btw_prijs_plus_opslag']

            ode_plus_btw = ode+ode_btw
            eb_plus_btw = eb+eb_btw

            ode_plus_btw = ode*(1+btw)
            eb_plus_btw = eb*(1+btw)
            all_in_prijs = opslag_price_dict['prijs_plus_opslag_plus_btw']+ode_plus_btw+eb_plus_btw

            return {'btw_total': btw_total, 'eb': eb, 'ode': ode, 'all_in_prijs': all_in_prijs, 'btw_perc': int(price_line['btw'])}

        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @staticmethod
    def opslag_price(user_belastingen:dict = None, price_line:dict = None)->dict:
        try:
            if  price_line is None:
                raise Exception('price_line is None')

            opslag = price_line['opslag']
            if user_belastingen:
                try:
                    if user_belastingen[price_line['kind']]['opslag'] is not None:
                        opslag = user_belastingen[price_line['kind']]['opslag']
                except KeyError:
                    pass

            btw = (int(price_line['btw'])/100)
            prijs_plus_opslag = (opslag+price_line['price'])
            btw_prijs_plus_opslag = prijs_plus_opslag*btw
            prijs_plus_opslag_plus_btw = prijs_plus_opslag+btw_prijs_plus_opslag

            return {'opslag': opslag, 'prijs_plus_opslag': prijs_plus_opslag, 'btw_prijs_plus_opslag': btw_prijs_plus_opslag, 'prijs_plus_opslag_plus_btw': prijs_plus_opslag_plus_btw}

        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False

    @staticmethod
    def dutch_floats(price:float = None, my_locale:str="de_DE")->str:
        my_locale = f"{my_locale}.UTF-8"
        locale.setlocale(locale.LC_NUMERIC, my_locale)
        try:
            if price is None or price == "":
                return ""

            return locale.format_string("€ %.3f", price, grouping=False)
        except (KeyError,Exception) as e:
            log.error(e, exc_info=True)
            return False
