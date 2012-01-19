import sys
import datetime
import os
import MySQLdb
import pbp_espn
import shotchart_cbssports
import shotchart_espn
import all_nbacom

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

    for gamedata,filenames in sourcedocs:
        print "Extracting CBSSports.com shot chart data from %s" % (filenames['shotchart_cbssports'])
        shotvars = {
            'html': open(LOGDIR_SOURCE + filenames['shotchart_cbssports'],'r').read(),
            'filename':  filenames['shotchart_cbssports'],
            'gamedata': gamedata
        }
        shotchart_cbssports.ShotExtract(**shotvars).extractAndDump()
        print "Success"

        print "Extracting ESPN.com play by play data from %s" % (filenames['playbyplay_espn'])
        pbpvars = {
            'html': open(LOGDIR_SOURCE + filenames['playbyplay_espn'],'r').read(),
            'filename':  filenames['playbyplay_espn'],
            'gamedata':  gamedata
        }
        pbp_espn.Extract(**pbpvars).extractAndDump()
        print "Success"

        print "Passing on ESPN shot chart file"
        shotchart_espn.copyFile(filenames['shotchart_espn'])
        print "Success"

        print "Passing on all NBA.com files (shot chart, play by play, box score)"
        for f in [filenames['shotchart_nbacom'],filenames['playbyplay_nbacom'],filenames['boxscore_nbacom']]:
            all_nbacom.copyFile(f)
        print "Success"


if __name__ == '__main__':
    sys.exit(main())
