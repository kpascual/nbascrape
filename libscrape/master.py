import sys
import time
import datetime
import MySQLdb
import os
import logging

from libscrape.config import constants
from libscrape.config import db
from libscrape.config import config
import source.main
import extract.main
import clean.main
import load.main
import afterclean2.main


LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

logging.basicConfig(filename='etl.log',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def _chooseGames(date_played, dbobj):
    return dbobj.query_dict("""
        SELECT g.*, home_team.city home_team_city, away_team.city away_team_city 
        FROM game g 
            INNER JOIN team home_team on home_team.id = g.home_team_id
            INNER JOIN team away_team on away_team.id = g.away_team_id
        WHERE g.date_played = '%s'
            AND g.should_fetch_data = 1
    """ % (date_played))


def getAll(dt, files = None):
    dbobj = db.Db(config.config['db'])
    step_time = time.time()

    config_no_pw = config.config['db']
    del config_no_pw['passwd']
    logging.info("MASTER - starting ETL job - date: %s - database: %s" % (dt, config_no_pw))
    # Default set of files/tables to populate
    if not files:
        files = ['boxscore_nbacom','boxscore_cbssports','playbyplay_espn','playbyplay_nbacom','shotchart_cbssports','shotchart_espn','shotchart_nbacom']

    # Choose games
    games = _chooseGames(dt, dbobj)

    # MAIN ETL PROCESS
    print "+++ MASTER ETL - files: %s - database: %s" % (str(files), config.config['db'])

    # Get source
    gamedata = source.main.go(games, files)

    extract.main.go(gamedata)
    clean.main.go(gamedata, dbobj)
    load.main.go(gamedata, dbobj)

    afterclean2.main.go(gamedata, dbobj)

    tomorrow = dt + datetime.timedelta(days=1)

    time_elapsed = "Total time: %.2f sec" % (time.time() - step_time)
    logging.info(time_elapsed)


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
    getAll(dt,files)
    

if __name__ == '__main__':
    main()
