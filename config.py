from os import path as p

BASEDIR = p.dirname(__file__)
PARENTDIR = p.dirname(BASEDIR)
DB_NAME = 'scraperwiki.sqlite'
RECIPIENT = 'reubano@gmail.com'


# configuration
class Config(object):
    BASE_URL = 'http://www.acleddata.com/wp-content/uploads/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(BASEDIR, DB_NAME)
    API_LIMIT = 1000
    SW = False
    DEBUG = False
    TESTING = False
    PROD = False
    CHUNK_SIZE = 2 ** 14
    ROW_LIMIT = None
    LOGFILE = p.join(PARENTDIR, 'http', 'log.txt')


class Scraper(Config):
    PROD = True
    SW = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(PARENTDIR, DB_NAME)


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
