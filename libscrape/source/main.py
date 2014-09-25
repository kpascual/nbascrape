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


def func_boxscore_cbssports(game):
    # Data comes from shotchart_cbssports file
    return False


def func_shotchart_cbssports(game):
    return getSourceDoc(constants.URL['shotchart_cbssports'] + game['cbssports_game_id']) 


def func_playbyplay_nbacom(game):
    return getSourceDoc(constants.URL['playbyplay_nbacom'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_shotchart_nbacom(game):
    return getSourceDoc(constants.URL['shotchart_nbacom'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_boxscore_nbacom(game):
    return getSourceDoc(constants.URL['boxscore_nbacom'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_playbyplay_espn(game):
    return getSourceDoc(constants.URL['playbyplay_espn'].replace('<game_id>',str(game['espn_game_id']))) 


def func_shotchart_espn(game):
    return getSourceDoc(constants.URL['shotchart_espn'].replace('<game_id>',str(game['espn_game_id']))) 


def func_shotchart_wnbacom(game):
    return getSourceDoc(constants.URL['shotchart_nbacom'].replace('<game_id>',str(game['nbacom_game_id']))) 


def func_playbyplay_statsnbacom(game):
    return getSourceDoc(constants.URL['playbyplay_statsnbacom'].replace('<game_id>',str(game['statsnbacom_game_id']))) 


def func_shotchart_statsnbacom(game):
    return getSourceDoc(constants.URL['shotchart_statsnbacom'].replace('<game_id>',str(game['statsnbacom_game_id']))) 


def func_boxscore_statsnbacom(game):
    return getSourceDoc(constants.URL['boxscore_statsnbacom'].replace('<game_id>',str(game['statsnbacom_game_id']))) 


def getAndSaveFiles(game, files):

    print "+++ SOURCE: %s - %s" % (game['id'], game['abbrev'])

    filenames = {}
    for f in files:
        filename = '%s_%s' % (game['abbrev'],f)
        if not _doesFileExist(filename):
            body = globals()["func_" + f](game)
            if body is not False:
                saveToFile(filename, body)
                print '  + %s saved ' % (f)
            else:
                print '  + %s passed' % (f)
        else:
            print '  + %s found. Skipping.' % (f)
        filenames[f] = filename

    return filenames



def _doesFileExist(filename):
    if filename in os.listdir(LOGDIR_SOURCE):
        return True
    else:
        return False


def go(games, files):
    return [(gamedata, getAndSaveFiles(gamedata, files)) for gamedata in games]


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
