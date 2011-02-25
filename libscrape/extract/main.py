import sys
import datetime
import os
import MySQLdb
import pbp_espn
import shotchart_cbssports

from libscrape.config import constants

LOGDIR_SOURCE = constants.LOGDIR_SOURCE
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


def getDate():
    try:
        dt =  sys.argv[1]
    except:
        dt = datetime.date.today() - datetime.timedelta(days=1)
        dt = dt.isoformat()
    
    return dt


def writeToFile(filename, list_plays):
    f = open(LOGDIR_EXTRACT + filename, 'w')
    f.write('\n'.join([','.join([str(point) for point in play]) for play in list_plays]))
    f.close()


def go(sourcedocs):

    for (gamedata,(file_cbssports, file_espn)) in sourcedocs:
        print "Extracting data from %s" % file_cbssports 
        shotvars = {
            'html': open(LOGDIR_SOURCE + file_cbssports,'r').read(),
            'filename':  file_cbssports,
            'home_team': gamedata['home_team'],
            'away_team': gamedata['away_team'],
            'game_name': gamedata['abbrev']
        }
        shotchart_cbssports.ShotExtract(**shotvars).extractAndDump()
        print "Success"

        print "Extracting data from %s" % file_espn
        pbpvars = {
            'html': open(LOGDIR_SOURCE + file_espn,'r').read(),
            'filename':  file_espn,
            'home_team': gamedata['home_team'],
            'away_team': gamedata['away_team'],
            'game_name': gamedata['abbrev']
        }
        pbp_espn.Extract(**pbpvars).extractAndDump()
        print "Success"


if __name__ == '__main__':
    sys.exit(main())
