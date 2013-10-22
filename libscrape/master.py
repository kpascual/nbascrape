import sys
import time
import datetime
import MySQLdb
import os
import logging

from libscrape.config import constants
from libscrape.config import db
from libscrape.config import config
import league
import source.main
import extract.main
import clean.main
import load.main


LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

logging.basicConfig(filename='etl.log',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')



def scrapeDailyAuto(dt, files = None):
    step_time = time.time()

    dbobj = db.Db(config.config['db'])
    config_no_pw = config.config['db'].copy()
    del config_no_pw['passwd']
    
    if not files:
        files = [
            'boxscore_nbacom',
            'boxscore_cbssports',
            'playbyplay_espn',
            'playbyplay_nbacom',
            'shotchart_cbssports',
            'shotchart_espn',
            'shotchart_nbacom'
        ]

    # MAIN ETL PROCESS
    print "+++ MASTER ETL - files: %s - database: %s" % (str(files), config_no_pw)
    logging.info("MASTER - starting ETL job - date: %s - database: %s" % (dt, config_no_pw))

    scrape(dbobj, dt, files)

    tomorrow = dt + datetime.timedelta(days=1)

    time_elapsed = "Total time: %.2f sec" % (time.time() - step_time)
    logging.info(time_elapsed)


def scrape(dbobj, dt, files):
    # Choose games
    lgobj = league.League(dbobj)
    games = lgobj.getGames(dt)

    # Get source
    gamedata = source.main.go(games, files)

    # Scrape
    extract.main.go(gamedata)
    clean.main.go(gamedata, dbobj)
    load.main.go(gamedata, dbobj)


def main():

    files = []
    try:
        dt = sys.argv[1]
        dt = datetime.date(*map(int,dt.split('-')))

        if len(sys.argv) > 2:
            files = sys.argv[2:]
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)

    print dt
    scrapeDailyAuto(dt, files)
    

if __name__ == '__main__':
    main()
