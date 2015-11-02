## ACLED Realtime Data Collector

Collector for [ACLED Realtime Data](http://www.acleddata.com/data/realtime-data-2015/).

## Setup

*local*

(You are using a [virtualenv](http://www.virtualenv.org/en/latest/index.html), right?)

    pip install -r requirements.txt
    manage setup

*ScraperWiki Box*

    make setup

## Usage

*local*

    manage run

*ScraperWiki Box*

    source venv/bin/activate
    screen manage -m Scraper run
    Now press `Ctrl-a d`

The results will be stored in a SQLite database `scraperwiki.sqlite`.
