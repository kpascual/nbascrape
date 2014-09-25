import json
from libscrape.config import constants

LOGDIR_CLEAN = constants.LOGDIR_CLEAN

def run(filename, dbobj):
    shots = json.loads(open(LOGDIR_CLEAN + filename,'r').readline())

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

    dbobj.insert_or_update('shotchart_nbacom', newshots)
