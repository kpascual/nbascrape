import sys
import datetime
import os
import player
from libscrape.config import db

LOGDIR_SOURCE = '../../logs/source/'
LOGDIR_EXTRACT = '../../logs/extract/'
LOGDIR_CLEAN = '../../logs/clean/'


def mainfunc():
    dbobj = db.Db(db.dbconn_nba_test)

    gamedata = dbobj.query_dict("SELECT * FROM game WHERE date_played <= '2012-02-01' ORDER BY date_played ASC")

    for g in gamedata:
        fnba = g['abbrev'] + '_boxscore_nbacom'
        fcbs = g['abbrev'] + '_shotchart_cbssports'
        if fnba in os.listdir(LOGDIR_EXTRACT):
            print g['abbrev']
            obj = player.PlayerNbaCom(LOGDIR_EXTRACT + fnba, g, dbobj)
            obj.resolveNewPlayers()
            obj = player.PlayerCbsSports(LOGDIR_EXTRACT + fcbs + '_players', g, dbobj)
            obj.resolveNewPlayers()


if __name__ == '__main__':
    mainfunc()

