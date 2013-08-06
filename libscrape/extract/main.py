import sys
import datetime
import time
import os
import MySQLdb
import logging

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


def func_shotchart_cbssports(game, filename):
    params = {
        'html': open(LOGDIR_SOURCE + filename,'r').read(),
        'filename':  filename,
        'gamedata': game
    }
    shotchart_cbssports.ShotExtract(**params).extractAndDump()


def func_playbyplay_espn(game, filename):
    params = {
        'html': open(LOGDIR_SOURCE + filename,'r').read(),
        'filename':  filename,
        'gamedata':  game
    }
    pbp_espn.Extract(**params).extractAndDump()


def func_shotchart_espn(game, filename):
    shotchart_espn.copyFile(filename)


def func_shotchart_nbacom(game, filename):
    all_nbacom.copyFile(filename)


def func_playbyplay_nbacom(game, filename):
    all_nbacom.copyFile(filename)


def func_boxscore_nbacom(game, filename):
    all_nbacom.copyFile(filename)


def func_boxscore_cbssports(game, filename):
    pass


def func_shotchart_wnbacom(game, filename):
    all_nbacom.copyFile(filename)


def go(sourcedocs):

    for gamedata, files in sourcedocs:
        print "+++ EXTRACT: %s - %s" % (gamedata['id'], gamedata['abbrev'])

        for f in files.keys():
            print "  + %s" % (f)
            step_time = time.time()

            globals()["func_" + f](gamedata, files[f])

            logging.info("EXTRACT - %s - game_id: %s - : time_elapsed %.2f" % (f, gamedata['id'], time.time() - step_time))



if __name__ == '__main__':
    sys.exit(main())
