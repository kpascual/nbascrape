import json
from libscrape.config import constants

LOGDIR_CLEAN = constants.LOGDIR_CLEAN

def run(filename, dbobj):
    shots = json.loads(open(LOGDIR_CLEAN + filename, 'r').readline())

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

    dbobj.insert_or_update('shotchart_espn', newshots)
