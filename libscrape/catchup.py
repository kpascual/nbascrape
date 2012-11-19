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
import findgames


LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

logging.basicConfig(filename='etl.log',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def chooseGames(date_played, dbobj):
    return dbobj.query_dict("""
        SELECT g.*, home_team.city home_team_city, away_team.city away_team_city 
        FROM game g 
            INNER JOIN team home_team on home_team.id = g.home_team_id
            INNER JOIN team away_team on away_team.id = g.away_team_id
        WHERE g.date_played = '%s'
            AND g.should_fetch_data = 1
    """ % (date_played))


def restartFromExtract(dt):
    dbobj = db.Db(db.dbconn_nba)

    games = chooseGames(dt)
    gamedata = getExistingSourceDocs(games)
    
    extract.main.go(gamedata)
    clean.main.go(gamedata, dbobj)
    load.main.go(gamedata, dbobj)


def restartFromClean(dt):
    dbobj = db.Db(db.dbconn_nba)

    games = chooseGames(dt)
    gamedata = getExistingSourceDocs(games)
 
    clean.main.go(gamedata, dbobj)
    load.main.go(gamedata, dbobj)


def cleanOnly(dt):
    dbobj = db.Db(db.dbconn_nba_test)

    games = chooseGames(dt)
    gamedata = getExistingSourceDocs(games)
 
    clean.main.go(gamedata, dbobj)

def extractOnly(dt):

    games = chooseGames(dt)
    gamedata = getExistingSourceDocs(games)
 
    extract.main.go(gamedata)

def loadOnly(dt):
    dbobj = db.Db(db.dbconn_nba)
    games = chooseGames(dt)
    gamedata = getExistingSourceDocs(games)
 
    load.main.go(gamedata, dbobj)


def aftercleanOnly(dt, files = None):
    dbobj = db.Db(config.config['db'])

    if not files:
        files = ['boxscore_nbacom','boxscore_cbssports','playbyplay_espn','playbyplay_nbacom','shotchart_cbssports','shotchart_espn','shotchart_nbacom']
    games = chooseGames(dt, dbobj)
    gamedata = source.main.go(games, files)
    afterclean2.main.go(gamedata, dbobj)


def getAll(dt, files = None):
    dbobj = db.Db(config.config['db'])
    step_time = time.time()

    logging.info("MASTER - starting ETL job - date: %s - database: %s" % (dt, db_credentials['db']))
    # Default set of files/tables to populate
    if not files:
        files = ['boxscore_nbacom','boxscore_cbssports','playbyplay_espn','playbyplay_nbacom','shotchart_cbssports','shotchart_espn','shotchart_nbacom']

    # Choose games
    games = chooseGames(dt, dbobj)

    # MAIN ETL PROCESS
    print "+++ MASTER ETL - files: %s - database: %s" % (str(files), db_credentials['db'])
    # Get source
    gamedata = source.main.go(games, files)

    extract.main.go(gamedata)
    clean.main.go(gamedata, dbobj)
    load.main.go(gamedata, dbobj)

    afterclean2.main.go(gamedata, dbobj)

    tomorrow = dt + datetime.timedelta(days=1)
    #findgames.go(tomorrow)

    time_elapsed = "Total time: %.2f sec" % (time.time() - step_time)
    print time_elapsed
    logging.info(time_elapsed)


def main():

    dbobj = db.Db(db.dbconn_nba)

    files = []
    try:
        dt = sys.argv[1]
        dt = datetime.date(*map(int,dt.split('-')))

        if len(sys.argv) > 2:
            files = sys.argv[2:]
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)

    print dt
    aftercleanOnly(dt,files)
    

if __name__ == '__main__':
    main()
