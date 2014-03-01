import MySQLdb
import sys
import datetime
import urllib2
import os

from libscrape.config import db
from libscrape.config import constants


LOGDIR_SOURCE = constants.LOGDIR_SOURCE


def chooseGames(date_played):
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    curs.execute("SELECT * FROM game WHERE date_played = '%s'" % (date_played))
    return curs.fetchall()


def saveToFile(filename, body):
    f = open('%s%s' % (LOGDIR_SOURCE, filename),'w')
    f.write(body)
    f.close()

def getSourceDoc(url):
    response = urllib2.urlopen(url)
    return response.read()


def func_boxscore_cbssports(game, league):
    # Data comes from shotchart_cbssports file
    return False


def func_shotchart_cbssports(game, league):
    return getSourceDoc(constants.URL[league]['SHOTCHART_CBSSPORTS'] + game['cbssports_game_id']) 


def func_playbyplay_nbacom(game, league):
    return getSourceDoc(constants.URL[league]['PLAYBYPLAY_NBACOM'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_shotchart_nbacom(game, league):
    return getSourceDoc(constants.URL[league]['SHOTCHART_NBACOM'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_boxscore_nbacom(game, league):
    return getSourceDoc(constants.URL[league]['BOXSCORE_NBACOM'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_playbyplay_espn(game, league):
    return getSourceDoc(constants.URL[league]['PLAYBYPLAY_ESPN'].replace('<game_id>',str(game['espn_game_id']))) 


def func_shotchart_espn(game, league):
    return getSourceDoc(constants.URL[league]['SHOTCHART_ESPN'].replace('<game_id>',str(game['espn_game_id']))) 


def func_shotchart_wnbacom(game, league):
    return getSourceDoc(constants.URL[league]['SHOTCHART_NBACOM'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_playbyplay_statsnbacom(game, league):
    return getSourceDoc(constants.URL[league]['PLAYBYPLAY_STATSNBACOM'].replace('<game_id>',str(game['statsnbacom_game_id']))) 


def func_shotchart_statsnbacom(game, league):
    return getSourceDoc(constants.URL[league]['SHOTCHART_STATSNBACOM'].replace('<game_id>',str(game['statsnbacom_game_id']))) 


def func_boxscore_statsnbacom(game, league):
    return getSourceDoc(constants.URL[league]['BOXSCORE_STATSNBACOM'].replace('<game_id>',str(game['statsnbacom_game_id']))) 


def getAndSaveFiles(game, files, league='nba'):

    print "+++ SOURCE: %s - %s" % (game['id'], game['abbrev'])

    filenames = {}
    for f in files:
        filename = '%s_%s' % (game['abbrev'],f)
        if not doesFileExist(filename):
            body = globals()["func_" + f](game, league)
            if body is not False:
                saveToFile(filename, body)
                print '  + %s saved ' % (f)
            else:
                print '  + %s passed' % (f)
        else:
            print '  + %s found. Skipping.' % (f)
        filenames[f] = filename

    return filenames



def doesFileExist(filename):
    if filename in os.listdir(LOGDIR_SOURCE):
        return True
    else:
        return False


def go(games, files, league='nba'):
    return [(gamedata,getAndSaveFiles(gamedata, files, league)) for gamedata in games]


def main(dt = None):
    
    date_played = datetime.date.today() - datetime.timedelta(days=1)
    if dt:
        date_played = dt

    games = chooseGames(date_played)
    if games:
        print '--- Found %s games for %s. Now parsing...' % (len(games),date_played) 

        for game in games:
            getAndSaveFiles(game)


if __name__ == '__main__':
    sys.exit(main())
