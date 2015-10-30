#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
utils
~~~~~

Provides miscellaneous utility methods
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import time
import schedule as sch
import smtplib
import logging
import scraperwiki
import requests
import itertools as it

from os import environ, path as p
from email.mime.text import MIMEText
from tempfile import SpooledTemporaryFile
from datetime import datetime as dt

from dateutil.parser import parse
from bs4 import BeautifulSoup

from config import _project
from tabutils import io

_basedir = p.dirname(__file__)
_parentdir = p.dirname(_basedir)
_schedule_time = '10:30'
_recipient = 'reubano@gmail.com'

logging.basicConfig()
logger = logging.getLogger(_project)


def send_email(_to, _from=None, subject=None, text=None):
    user = environ.get('user')
    _from = _from or '%s@scraperwiki.com' % user
    subject = subject or 'scraperwiki box %s failed' % user
    text = text or 'https://scraperwiki.com/dataset/%s' % user
    msg = MIMEText(text)
    msg['Subject'], msg['From'], msg['To'] = subject, _from, _to

    # Send the message via our own SMTP server, but don't include the envelope
    # header.
    s = smtplib.SMTP('localhost')
    s.sendmail(_from, [_to], msg.as_string())
    s.quit()


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(str(e))
            scraperwiki.status('error', 'Error collecting data')

            with open(p.join(_parentdir, 'http', 'log.txt'), 'rb') as f:
                send_email(_recipient, text=f.read())
        else:
            scraperwiki.status('ok')

    return wrapper


def run_or_schedule(job, schedule=False, exception_handler=None):
    if exception_handler:
        job = exception_handler(job)

    job()

    if schedule:
        sch.every(1).day.at(_schedule_time).do(job)

        while True:
            sch.run_pending()
            time.sleep(1)


def gen_data(config):
    """Fetches realtime data and generates records"""
    url = config['BASE_URL']

    # find the newest year
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    year = sorted(filter(lambda l: l.startswith('2'), links))[-1]
    url += year

    # find the newest month
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    month = sorted(filter(lambda l: l[0] in {'0', '1'}, links))[-1]
    url += month

    # find the newest file
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    name = 'acled-all-africa-file'
    filterer = lambda l: l.lower().startswith(name) and 'xls' in l
    files = sorted(filter(filterer, links))
    ftups = [(f.split('.')[0].split('-')[5], f) for f in files]
    filename = sorted(ftups)[-1][1]
    url += filename

    # download the file
    r = requests.get(url)
    f = SpooledTemporaryFile()  # wrap to access `fileno`
    f.write(r.content)

    records = io.read_xls(f, sanitize=True, encoding=r.encoding)
    year = dt.now().year

    for record in records:
        month = parse(record['event_date']).month
        month = '0%s' % month if month < 10 else month
        record['year_month'] = '%s%s' % (year, month)
        yield record
