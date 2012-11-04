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
    return getSourceDoc(constants.URL_SHOTCHART_CBSSPORTS + game['cbssports_game_id']) 


def func_playbyplay_nbacom(game):
    return getSourceDoc(constants.URL_PLAYBYPLAY_NBACOM.replace('<game_id>',str(game['nbacom_game_id']))) 


def func_shotchart_nbacom(game):
    return getSourceDoc(constants.URL_SHOTCHART_NBACOM.replace('<game_id>',str(game['nbacom_game_id']))) 


def func_boxscore_nbacom(game):
    return getSourceDoc(constants.URL_BOXSCORE_NBACOM.replace('<game_id>',str(game['nbacom_game_id']))) 


def func_playbyplay_espn(game):
    return getSourceDoc(constants.URL_PLAYBYPLAY_ESPN.replace('<game_id>',str(game['espn_game_id']))) 


def func_shotchart_espn(game):
    return getSourceDoc(constants.URL_SHOTCHART_ESPN.replace('<game_id>',str(game['espn_game_id']))) 


def getAndSaveFiles(game, files):

    print "+++ SOURCE: %s - %s" % (game['id'], game['abbrev'])

    filenames = {}
    for f in files:
        filename = '%s_%s' % (game['abbrev'],f)
        if not doesFileExist(filename):
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

    """
    # CBS Sports Shot Chart and box score
    filename_shotchart_cbssports = '%s_shotchart_cbssports' % game['abbrev']
    filename_boxscore_cbssports = '%s_boxscore_cbssports' % game['abbrev']
    if not doesFileExist(filename_shotchart_cbssports):
        str_body = getSourceDoc(constants.URL_SHOTCHART_CBSSPORTS + game['cbssports_game_id']) 
        saveToFile(filename_shotchart_cbssports, str_body)
        print '  + CBS Sports shot chart saved '
    else:
        print '  + CBS Sports shot chart found. Skipping. '

    # ESPN Play by Play
    filename_playbyplay_espn = '%s_playbyplay_espn' % game['abbrev']
    if not doesFileExist(filename_playbyplay_espn):
        str_body = getSourceDoc(constants.URL_PLAYBYPLAY_ESPN.replace('<game_id>',str(game['espn_game_id']))) 
        saveToFile(filename_playbyplay_espn, str_body)
        print '  + ESPN Play by Play saved '
    else:
        print '  + ESPN Play by Play found. Skipping. '


    # ESPN Shot Chart
    filename_shotchart_espn = '%s_shotchart_espn' % game['abbrev']
    if not doesFileExist(filename_shotchart_espn):
        str_body = getSourceDoc(constants.URL_SHOTCHART_ESPN.replace('<game_id>',str(game['espn_game_id']))) 
        saveToFile(filename_shotchart_espn, str_body)
        print '  + ESPN Shot Chart saved '
    else:
        print '  + ESPN Shot Chart found. Skipping. '
        

    # NBA.com play by play
    filename_playbyplay_nbacom = '%s_playbyplay_nbacom' % game['abbrev']
    if not doesFileExist(filename_playbyplay_nbacom):
        str_body = getSourceDoc(constants.URL_PLAYBYPLAY_NBACOM.replace('<game_id>',str(game['nbacom_game_id']))) 
        saveToFile(filename_playbyplay_nbacom, str_body)
        print '  + NBA.com play by play saved '
    else:
        print '  + NBA.com play by play found. Skipping. '


    # NBA.com shot chart
    filename_shotchart_nbacom = '%s_shotchart_nbacom' % game['abbrev']
    if not doesFileExist(filename_shotchart_nbacom):
        str_body = getSourceDoc(constants.URL_SHOTCHART_NBACOM.replace('<game_id>',str(game['nbacom_game_id']))) 
        saveToFile(filename_shotchart_nbacom, str_body)
        print '  + NBA.com shot chart file saved '
    else:
        print '  + NBA.com shot chart file found. Skipping. '

    # NBA.com box score
    filename_boxscore_nbacom = '%s_boxscore_nbacom' % game['abbrev']
    if not doesFileExist(filename_boxscore_nbacom):
        str_body = getSourceDoc(constants.URL_BOXSCORE_NBACOM.replace('<game_id>',str(game['nbacom_game_id']))) 
        saveToFile(filename_boxscore_nbacom, str_body)
        print '  + NBA.com box score saved' 
    else:
        print '  + NBA.com box score found. Skipping. '

    return {
        'shotchart_cbssports'   : filename_shotchart_cbssports,
        'playbyplay_espn'       : filename_playbyplay_espn,
        'shotchart_espn'        : filename_shotchart_espn,
        'shotchart_nbacom'      : filename_shotchart_nbacom,
        'playbyplay_nbacom'     : filename_playbyplay_nbacom,
        'boxscore_nbacom'       : filename_boxscore_nbacom,
        'boxscore_cbssports'    : filename_boxscore_cbssports
    }
    """



def doesFileExist(filename):
    if filename in os.listdir(LOGDIR_SOURCE):
        return True
    else:
        return False


def go(games, files):
    return [(gamedata,getAndSaveFiles(gamedata, files)) for gamedata in games]


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
