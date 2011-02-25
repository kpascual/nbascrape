import sys
import datetime
import MySQLdb
import os

from libscrape.config import constants
from libscrape.config import db
import source.main
import extract.main
import clean.main
import load.main


LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


def chooseGames(date_played):
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("SELECT * FROM game WHERE date_played = '%s'" % (date_played))
    return curs.fetchall()


def getExistingSourceDocs(games):
    gamedata = []
    for g in games:
        try:
            file_espn = [itm for itm in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in itm and 'pbp_espn' in itm][0]
        except:
            file_espn = ''
            print "No source espn doc found for %s" % g['abbrev']

        try: 
            file_cbs = [itm for itm in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in itm and 'shotchart_cbssports' in itm][0]
        except:
            file_cbs = ''
            print "No source cbs sports doc found for %s" % g['abbrev']

        if file_cbs and file_espn:
            gamedata.append((g,(file_cbs, file_espn)))

    return gamedata


def restartFromExtract(dt):
    games = chooseGames(dt)
    gamedata = getExistingSourceDocs(games)
 
    extract.main.go(gamedata)
    clean.main.go(gamedata)
    load.main.go(gamedata)


def getAll(dt):

    # Choose games
    games = chooseGames(dt)

    # MAIN ETL PROCESS
    # Get source
    gamedata = source.main.get(games)

    extract.main.go(gamedata)
    clean.main.go(gamedata)
    load.main.go(gamedata)


def main():
    try:
        dt = sys.argv[1]
        dt = datetime.date(*map(int,dt.split('-')))
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)

    print dt
    
    # Choose games
    games = chooseGames(dt)

    # MAIN ETL PROCESS
    # Get source
    gamedata = source.main.get(games)

    extract.main.go(gamedata)
    clean.main.go(gamedata)
    load.main.go(gamedata)
    

if __name__ == '__main__':
    main()
