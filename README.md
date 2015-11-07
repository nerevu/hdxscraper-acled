# ACLED Realtime Data Collector

Collector for [ACLED Realtime Data](http://www.acleddata.com/data/realtime-data-2015/).

## Introduction

This collector operates in the following way:

- downloads the most recent `acled-all-africa` xls file by navigating the [uploads directory](http://www.acleddata.com/wp-content/uploads/)
- groups the rows by year-month
- dynamically creates a separate table for each group

## Requirements

hdxscraper-acled has been tested on the following configuration:

- MacOS X 10.9.5
- Python 2.7.10

hdxscraper-acled requires the following in order to run properly:

- [Python >= 2.7](http://www.python.org/download) (MacOS X comes with python preinstalled)

## Setup

*local*

(You are using a [virtualenv](http://www.virtualenv.org/en/latest/index.html), right?)

    git clone https://github.com/reubano/hdxscraper-acled.git
    pip install -r requirements.txt
    manage setup

*ScraperWiki Box*

    make setup

## Usage

*local*

    manage run

*ScraperWiki Box*

    cd tool
    source venv/bin/activate
    screen manage -m Scraper run
    Now press `Ctrl-a d`

The results will be stored in a SQLite database `scraperwiki.sqlite`.

## Upload tables to HDX/CKAN

*upload to production site*

    manage upload

*upload to staging site*

    manage upload -s

## Configuration

hdxscraper-acled will use the following [Environment Variables](http://www.cyberciti.biz/faq/set-environment-variable-linux/) if set:

Environment Variable|Description
--------------------|-----------
CKAN_API_KEY|Your CKAN API Key
CKAN_PROD_URL|Your CKAN instance remote production url
CKAN_REMOTE_URL|Your CKAN instance remote staging url
CKAN_USER_AGENT|Your user agent

## Contributing

1. fork
2. commit
3. submit PR
4. ???
5. PROFIT!!!

## License

hdxscraper-acled is distributed under the [MIT License](http://opensource.org/licenses/MIT).
