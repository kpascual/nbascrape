import sys
import time
import datetime
import MySQLdb
import os
import logging

from libscrape.config import constants
from libscrape.config import db
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
            print "No source NBA.com box score doc found for %s" % g['abbrev']


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

def loadOnly(dt):
    dbobj = db.Db(db.dbconn_nba)
    games = chooseGames(dt)
    gamedata = getExistingSourceDocs(games)
 
    load.main.go(gamedata, dbobj)


def aftercleanOnly(dt):
    dbobj = db.Db(db.dbconn_nba)
    games = chooseGames(dt)
    gamedata = source.main.go(games)
    afterclean2.main.go(gamedata, dbobj)


def getAll(dt, files = None):
    db_credentials = db.dbconn_nba_prod
    dbobj = db.Db(db_credentials)
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


def fixOld():
    dbobj = db.Db(db.dbconn_nba)
    games = dbobj.query_dict("""
        SELECT g.*, home_team.city home_team_city, away_team.city away_team_city 
        FROM game g 
            INNER JOIN team home_team on home_team.id = g.home_team_id
            INNER JOIN team away_team on away_team.id = g.away_team_id
        WHERE 
            g.id IN (321,596,866,1074,1249,1263,1436,1526,1653,1654,1655,1656,1657,1658,1659,1660,1661,1662,1663,1664,1673,1674,1675,1676,1677,1678,1679,1680,1681,1682,1683,1684,1685,1686,1687,1688,1689,1690,1691,1692,1693,1694,1695,1696,1697,1698,1699,1700,1701,1702,1703,1704,1705,1706,1707,1708,1709,1710,1711,1712,1713,1714,1715,1716,1717,1718,1719,1720,1721,1722,1723,1724,2071);
    """)
    files = ['boxscore_nbacom','boxscore_cbssports','playbyplay_espn','playbyplay_nbacom','shotchart_cbssports','shotchart_espn','shotchart_nbacom']
    gamedata = source.main.go(games, files)

    extract.main.go(gamedata)
    clean.main.go(gamedata, dbobj)
    load.main.go(gamedata, dbobj)

    afterclean2.main.go(gamedata, dbobj)



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
    getAll(dt,files)
    #fixOld()
    

if __name__ == '__main__':
    main()
