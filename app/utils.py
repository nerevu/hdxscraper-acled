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

import requests
import itertools as it

from tempfile import SpooledTemporaryFile
from datetime import datetime as dt

from dateutil.parser import parse
from bs4 import BeautifulSoup
from tabutils import io


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

    if files:
        ftups = [(f.split('.')[0].split('-')[5], f) for f in files]
        filename = sorted(ftups)[-1][1]
        url += filename

        # download the file
        r = requests.get(url)
        f = SpooledTemporaryFile()  # wrap to access `fileno`
        f.write(r.content)

        records = io.read_xls(f, sanitize=True, encoding=r.encoding)
        year = dt.now().year
        filtered = it.ifilter(lambda r: int(float(r['year'])) == year, records)

        for record in filtered:
            month = parse(record['event_date']).month
            month = '0%s' % month if month < 10 else month
            record['year_month'] = '%s%s' % (year, month)
            yield record
