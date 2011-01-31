import MySQLdb
import sys
import datetime
import urllib2
from libscrape.config import db
from libscrape.config import constants


LOGDIR_SOURCE = constants.LOGDIR_SOURCE


def chooseGames(date_played):
    conn = MySQLdb.connect(**db.dbconn_nba)
    curs = conn.cursor()

    curs.execute("SELECT * FROM game WHERE date_played = '%s'" % (date_played))
    return curs.fetchall()


def saveToFile(filename, body):
    f = open('%s%s' % (LOGDIR_SOURCE, filename),'w')
    f.write(body)
    f.close()

def getSourceDoc(url):
    response = urllib2.urlopen(url)
    return response.read()


def main(dt = None):
    
    date_played = datetime.date.today() - datetime.timedelta(days=1)
    if dt:
        date_played = dt

    gms = chooseGames(date_played)
    if gms:
        print '--- Found %s games for %s. Now parsing...' % (len(gms),date_played) 

        for (game_id, away, home, dt, abbrev, espn, cbs) in gms:
            # CBS Sports
            filename = '%s_shotchart_cbssports' % abbrev
            str_body = getSourceDoc(constants.URL_SHOTCHART_CBSSPORTS + cbs) 
            saveToFile(filename, str_body)
            print '--- CBS Sports file for %s saved ' % abbrev

            # ESPN
            filename = '%s_pbp_espn' % abbrev
            str_body = getSourceDoc(constants.URL_PLAYBYPLAY_ESPN.replace('<game_id>',str(espn))) 
            saveToFile(filename, str_body)
            print '--- ESPN file for %s saved ' % abbrev



if __name__ == '__main__':
    sys.exit(main())
