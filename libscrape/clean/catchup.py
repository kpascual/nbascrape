import sys
import datetime
import os

import pbp_espn
import shotchart_cbssports
import main

LOGDIR_SOURCE = '../../logs/source/'
LOGDIR_EXTRACT = '../../logs/extract/'
LOGDIR_CLEAN = '../../logs/clean/'


def mainfunc():
    files_exist = [f for f in os.listdir(LOGDIR_CLEAN)]
    files_playbyplay = [f for f in os.listdir(LOGDIR_EXTRACT) if 'pbp_espn' in f and f not in files_exist]
    files_shotchart = list(set([f.replace('_players','').replace('_shots','') for f in os.listdir(LOGDIR_EXTRACT) if 'shotchart_cbssports' in f and f not in files_exist]))

    """
    print "%s New Play By Play files found" % len(files_playbyplay)
    for f in files_playbyplay:
        # Scrape ESPN play by play data
        print f
        list_plays = pbp_espn.Extract(open(LOGDIR_SOURCE + f,'r').read(), f).extractAll()
        main.writeToFile(f,list_plays) 
    """

    print "%s New Shot Chart files found" % len(files_shotchart)
    for f in files_shotchart:
        # Scrape CBS Sports Shot Chart data
        print f
        obj_shot = shotchart_cbssports.CleanShots(f)
        obj_shot.clean()



if __name__ == '__main__':
    mainfunc()

