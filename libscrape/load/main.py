import json
import os
import time
import logging
import csv

from libscrape.config import db
from libscrape.config import constants


LOGDIR_LOAD = constants.LOGDIR_LOAD
LOGDIR_CLEAN = constants.LOGDIR_CLEAN


class Load:

    def __init__(self, dbobj):
        self.db = dbobj


    def load_shotchart_cbssports(self, f):

        data = json.loads(open(constants.LOGDIR_CLEAN + f, 'r').read())
        self.db.insert_or_update('shotchart_cbssports',data)


    def load_playbyplay_nbacom(self, f):

        data = json.loads(open(constants.LOGDIR_CLEAN + f, 'r').read())
        self.db.insert_or_update('playbyplay_nbacom',data)


    def load_playbyplay_espn(self, f):

        data = json.loads(open(constants.LOGDIR_CLEAN + f, 'r').read())
        self.db.insert_or_update('playbyplay_espn',data)


    def load_boxscore_cbssports(self, f):

        data = open(constants.LOGDIR_CLEAN + f, 'r').readlines()
        data = list(csv.reader(open(constants.LOGDIR_CLEAN + f, 'r'),delimiter=',',lineterminator='\n'))
        fields = data[0]
        datapoints = data[1:]

        newdata = []
        for line in datapoints:
            newdata.append(dict(zip(fields,line)))
        
        self.db.insert_or_update('boxscore_cbssports',newdata)


    def load_shotchart_nbacom(self, f):
        shots = json.loads(open(LOGDIR_CLEAN + f,'r').readline())

        newshots = []
        for shot in shots:
            # Re-key shots
            shot['shot_type_nbacom_id'] = shot['act']
            shot['nbacom_play_num'] = shot['id']
            shot['period'] = shot['prd']
            shot['deciseconds_left'] = shot['time']
            shot['team_id'] = shot['tm']
            shot['is_shot_made'] = shot['result']

            del shot['act']
            del shot['id']
            del shot['prd']
            del shot['pid']
            del shot['s_clk']
            del shot['pts']
            del shot['time']
            del shot['tm']
            del shot['result']

            newshots.append(shot)

        self.db.insert_or_update('shotchart_nbacom',newshots)


    def load_boxscore_nbacom(self, f):
        data = json.loads(open(LOGDIR_CLEAN + f,'r').readline())

        newdata = []
        for line in data:
            line['personal_fouls'] = line['pfouls']
            del line['pfouls']
            del line['unknown13']

            newdata.append(line)

        self.db.insert_or_update('boxscore_nbacom',newdata)


    def load_shotchart_espn(self, f):
        shots = json.loads(open(LOGDIR_CLEAN + f,'r').readline())

        newshots = []
        for shot in shots:
            shot['espn_play_num'] = shot['id']
            shot['period'] = shot['qtr']
            shot['deciseconds_left'] = shot['time_left']
            shot['team_id'] = shot['t']
            shot['is_shot_made'] = shot['result']
            shot['shot_desc'] = shot['d']
            
            del shot['id']
            del shot['qtr']
            del shot['time_left']
            del shot['t']
            del shot['d']
            del shot['p']
            del shot['min']
            del shot['made']
            del shot['pid']
            del shot['sec']
            del shot['result']

            newshots.append(shot)

        self.db.insert_or_update('shotchart_espn',newshots)


    def load_game_stats(self, f):
        stats = json.loads(open(LOGDIR_CLEAN + f,'r').readline())
        self.db.insert_or_update('game_stats',[stats])


def go(tuple_games_and_files, dbobj):
    obj = Load(dbobj)

    """
    funcs = [
        (obj.loadCbsSportsShotData,'shotchart_cbssports',''),
        (obj.loadNbaComPlayByPlayData,'playbyplay_nbacom',''),
        (obj.loadEspnPlayByPlayData,'playbyplay_espn',''),
        (obj.loadCbsSportsBoxScore,'boxscore_cbssports',''),
        (obj.loadShotChartNbaCom,'shotchart_nbacom',''),
        (obj.loadShotChartEspn,'shotchart_espn',''),
        (obj.loadBoxScoreNbaCom,'boxscore_nbacom',''),
        (obj.loadBoxScoreNbaComGameStats,'boxscore_nbacom','_game_stats')

    ]
    """

    for gamedata, files in tuple_games_and_files:
        print "Loading %s" % (gamedata['abbrev'])
        s_time = time.time()

        for f in files.keys():
            step_time = time.time()
            getattr(obj,"load_" + f)(files[f])
            print "  Loaded %s: %.2f sec" % (f, time.time() - step_time)

            if f == 'boxscore_nbacom':
                getattr(obj,'load_game_stats')(files[f] + '_game_stats')



        """
        for func, filename, opt_extension in funcs:
            step_time = time.time()
            func(filenames[filename] + opt_extension)
            print "  Loaded %s: %.2f sec" % (func.__name__, time.time() - step_time)
        """

        logging.info("LOAD - game_id: %s - time_elapsed %.2f" % (gamedata['id'], time.time() - step_time))
        

def test():
    dbobj = db.Db(db.dbconn_nba)

    files = [f for f in os.listdir(LOGDIR_CLEAN) if 'game_stats' in f]
    
    obj = Load(dbobj)

    for f in files:
        obj.loadBoxScoreNbaComGameStats(f)


if __name__ == '__main__':
    test()
