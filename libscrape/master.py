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
import afterclean.main
import findgames


LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


def chooseGames(date_played):
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("""
        SELECT g.*, home_team.city home_team_city, away_team.city away_team_city 
        FROM game g 
            INNER JOIN team home_team on home_team.id = g.home_team_id
            INNER JOIN team away_team on away_team.id = g.away_team_id
        WHERE g.date_played = '%s'
    """ % (date_played))
    return curs.fetchall()


def getExistingSourceDocs(games):
    gamedata = []
    for g in games:
        filenames = {}
        try:
            filenames['playbyplay_espn'] = [f for f in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in f and 'playbyplay_espn' in f][0]
        except:
            filenames['playbyplay_espn'] = ''
            print "No source espn play by play doc found for %s" % g['abbrev']

        try:
            filenames['shotchart_espn'] = [f for f in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in f and 'shotchart_espn' in f][0]
        except:
            filenames['shotchart_espn'] = ''
            print "No source espn shotchart doc found for %s" % g['abbrev']

        try: 
            filenames['shotchart_cbssports'] = [itm for itm in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in itm and 'shotchart_cbssports' in itm][0]
            filenames['boxscore_cbssports'] = '%s_boxscore_cbssports' % (g['abbrev'])
        except:
            filenames['shotchart_cbssports'] = ''
            filenames['boxscore_cbssports'] = ''
            print "No source cbs sports shot chart doc found for %s" % g['abbrev']

        try: 
            filenames['shotchart_nbacom'] = [itm for itm in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in itm and 'shotchart_nbacom' in itm][0]
        except:
            filenames['shotchart_nbacom'] = ''
            print "No source NBA.com shot chart doc found for %s" % g['abbrev']

        try: 
            filenames['playbyplay_nbacom'] = [itm for itm in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in itm and 'playbyplay_nbacom' in itm][0]
        except:
            filenames['playbyplay_nbacom'] = ''
            print "No source NBA.com play by play doc found for %s" % g['abbrev']

        try: 
            filenames['boxscore_nbacom'] = [itm for itm in os.listdir(LOGDIR_SOURCE) if g['abbrev'] in itm and 'boxscore_nbacom' in itm][0]
        except:
            filenames['boxscore_nbacom'] = ''
            print "No source NBA.com play by play doc found for %s" % g['abbrev']

        if len(filenames.items()) == 7:
            gamedata.append((g,filenames))

    return gamedata


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


def getAll(dt):

    dbobj = db.Db(db.dbconn_nba)

    # Choose games
    games = chooseGames(dt)

    # MAIN ETL PROCESS
    # Get source
    gamedata = source.main.go(games)

    extract.main.go(gamedata)
    clean.main.go(gamedata, dbobj)
    load.main.go(gamedata, dbobj)

    afterclean.main.go(gamedata, dbobj)


def main():

    dbobj = db.Db(db.dbconn_nba)

    try:
        dt = sys.argv[1]
        dt = datetime.date(*map(int,dt.split('-')))
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)

    print dt
    getAll(dt)
    

if __name__ == '__main__':
    main()
