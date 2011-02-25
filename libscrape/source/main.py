import MySQLdb
import sys
import datetime
import urllib2

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


def extractPlayByPlayAndShotChart(game):
    (game_id, away, home, dt, abbrev, espn_id, cbs_id) = game

    # CBS Sports
    cbs_filename = '%s_shotchart_cbssports' % game['abbrev']
    str_body = getSourceDoc(constants.URL_SHOTCHART_CBSSPORTS + game['cbssports_game_id']) 
    saveToFile(cbs_filename, str_body)
    print '--- CBS Sports file for %s saved ' % game['abbrev']

    # ESPN
    espn_filename = '%s_pbp_espn' % game['abbrev']
    str_body = getSourceDoc(constants.URL_PLAYBYPLAY_ESPN.replace('<game_id>',str(game['espn_game_id']))) 
    saveToFile(espn_filename, str_body)
    print '--- ESPN file for %s saved ' % game['abbrev']

    return (cbs_filename, espn_filename)


def get(games):
    return [(gamedata,extractPlayByPlayAndShotChart(gamedata)) for gamedata in games]


def main(dt = None):
    
    date_played = datetime.date.today() - datetime.timedelta(days=1)
    if dt:
        date_played = dt

    games = chooseGames(date_played)
    if games:
        print '--- Found %s games for %s. Now parsing...' % (len(games),date_played) 

        for game in games:
            extractPlayByPlayAndShotChart(game)


if __name__ == '__main__':
    sys.exit(main())
