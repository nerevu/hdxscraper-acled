from os import path as p

# module vars
_basedir = p.dirname(__file__)
_parentdir = p.dirname(_basedir)
_db_name = 'scraperwiki.sqlite'
_project = 'hdxscraper-acled'


# configuration
class Config(object):
    BASE_URL = 'http://www.acleddata.com/wp-content/uploads/'
    TABLE = 'ACLED'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(_basedir, _db_name)
    API_LIMIT = 1000
    SW = False
    DEBUG = False
    TESTING = False
    PROD = False
    CHUNK_SIZE = 2 ** 14
    ROW_LIMIT = None


class Scraper(Config):
    PROD = True
    SW = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(_parentdir, _db_name)


class Production(Config):
    PROD = True


class Development(Config):
    DEBUG = True
    CHUNK_SIZE = 2 ** 4
    ROW_LIMIT = 50


class Test(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    CHUNK_SIZE = 2 ** 4
    ROW_LIMIT = 10
    TESTING = True
