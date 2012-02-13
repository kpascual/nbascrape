import sys
import datetime
import os

import pbp_espn
import shotchart_cbssports
import main
from libscrape.config import db

LOGDIR_SOURCE = '../../logs/source/'
LOGDIR_EXTRACT = '../../logs/extract/'
LOGDIR_CLEAN = '../../logs/clean/'


def mainfunc():


    f = '2010-10-27_MIL@NO_playbyplay_espn'
    print f
    dbobj = db.Db(db.dbconn_nba)

    gamedata = db.nba_query_dict("SELECT * FROM game where id = 6")[0]
    obj = pbp_espn.Clean(f,gamedata,dbobj)
    #returned = obj_shot.cleanAll()
    data = obj.cleanAll()


if __name__ == '__main__':
    mainfunc()

