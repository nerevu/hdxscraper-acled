#!/usr/bin/env python
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import os.path as p
import itertools as it
import swutils
import config

from subprocess import call
from operator import itemgetter

from pprint import pprint
from flask import current_app as app
from flask.ext.script import Manager
from tabutils.fntools import chunk

from app import create_app, db, utils, __title__
from app.models import BaseMixin


manager = Manager(create_app)
manager.add_option('-m', '--mode', default='Development')
manager.main = manager.run

_basedir = p.dirname(__file__)


@manager.command
def check():
    """Check staged changes for lint errors"""
    call(p.join(_basedir, 'bin', 'check-stage'), shell=True)


@manager.command
def lint():
    """Check style with flake8"""
    call('flake8')


@manager.command
def pipme():
    """Install requirements.txt"""
    call('sudo pip install -r requirements.txt', shell=True)


@manager.command
def require():
    """Create requirements.txt"""
    cmd = 'pip freeze -l | grep -vxFf dev-requirements.txt > requirements.txt'
    call(cmd, shell=True)


@manager.command
def test():
    """Run nose and script tests"""
    call('nosetests -xv', shell=True)


@manager.command
def createdb():
    """Creates database if it doesn't already exist"""

    with app.app_context():
        db.create_all()
        print('Database created')


@manager.command
def cleardb():
    """Removes all content from database"""

    with app.app_context():
        db.drop_all()
        print('Database cleared')


@manager.command
def setup():
    """Removes all content from database and creates new tables"""

    with app.app_context():
        cleardb()
        createdb()


def populate():
    """Populates db with most recent data"""
    with app.app_context():
        row_limit = app.config['ROW_LIMIT']
        chunk_size = min(row_limit or 'inf', app.config['CHUNK_SIZE'])
        debug, test = app.config['DEBUG'], app.config['TESTING']

        if test:
            createdb()

        data = utils.gen_data(app.config)
        keyfunc = itemgetter('year_month')

        for ym, group in it.groupby(sorted(data, key=keyfunc), keyfunc):
            count = 0
            name = 'YM%s' % ym
            table_name = name.lower()

            # dynamically create sqlalchemy table
            attrs = {'__tablename__': table_name}
            table = type(str(name), (db.Model, BaseMixin), attrs)

            if debug:
                print('Respawning table %s' % table_name)

            table.__table__.drop(db.engine, checkfirst=True)
            table.__table__.create(db.engine)

            for records in chunk(group, chunk_size):
                in_count = len(records)
                count += in_count

                if debug:
                    print(
                        'Inserting %s records into table `%s`...' % (
                            in_count, table_name))

                if test:
                    pprint(records)

                db.engine.execute(table.__table__.insert(), records)

                if row_limit and count >= row_limit:
                    break

            if debug:
                print(
                    'Successfully inserted %s records into table `%s`!' % (
                        count, table_name))


@manager.command
def run():
    """Populates all tables in db with most recent data"""
    with app.app_context():
        logfile = app.config['LOGFILE']
        open(logfile, 'w').close() if not p.exists(logfile) else None
        args = (config.RECIPIENT, logfile, __title__)
        exception_handler = swutils.ExceptionHandler(*args).handler
        swutils.run_or_schedule(populate, app.config['SW'], exception_handler)


@manager.command
def migrate():
    """Adds datasets to a CKAN instance"""
    call(p.join(_basedir, 'bin', 'migrate'))

if __name__ == '__main__':
    manager.run()
