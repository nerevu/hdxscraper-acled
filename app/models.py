# -*- coding: utf-8 -*-
"""
    app.models
    ~~~~~~~~~~

    Provides the SQLAlchemy models
"""
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

from datetime import datetime as dt
from app import db


class BaseMixin(object):
    # auto keys
    id = db.Column(db.Integer, primary_key=True)
    utc_created = db.Column(db.DateTime, nullable=False, default=dt.utcnow())
    utc_updated = db.Column(
        db.DateTime, nullable=False, default=dt.utcnow(), onupdate=dt.utcnow())

    # other keys
    event_type = db.Column(db.String(128), nullable=False)
    fatalities = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    year_month = db.Column(db.String(8), nullable=False)
    geo_precision = db.Column(db.String(128), nullable=False)
    source = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.Numeric, nullable=False)
    longitude = db.Column(db.Numeric, nullable=False)
    event_date = db.Column(db.String(10), nullable=False)
    adm_level_1 = db.Column(db.String(128), nullable=False)
    event_id_cnty = db.Column(db.String(128), nullable=False)
    inter1 = db.Column(db.String(128), nullable=False)
    adm_level_3 = db.Column(db.String(128), nullable=False)
    adm_level_2 = db.Column(db.String(128), nullable=False)
    gwno = db.Column(db.String(128), nullable=False)
    inter2 = db.Column(db.String(128), nullable=False)
    ally_actor_1 = db.Column(db.String(128), nullable=False)
    ally_actor_2 = db.Column(db.String(128), nullable=False)
    time_precision = db.Column(db.String(128), nullable=False)
    interaction = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    notes = db.Column(db.String(1024), nullable=False)
    actor2 = db.Column(db.String(128), nullable=False)
    actor1 = db.Column(db.String(128), nullable=False)
