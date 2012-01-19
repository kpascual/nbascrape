import json

from libscrape.config import db
from libscrape.config import constants


tables = db.test_tables
LOGDIR_LOAD = constants.LOGDIR_LOAD
LOGDIR_CLEAN = constants.LOGDIR_CLEAN


def loadCbsSportsShotData(f):
   
    str_fields = open(constants.LOGDIR_CLEAN + f, 'r').readline()
    sql = """
        LOAD DATA LOCAL INFILE '%s' REPLACE
        INTO TABLE %s
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (%s)
    """ % (constants.LOGDIR_CLEAN + f, tables['shotchart_cbssports'], str_fields)
    db.nba_query(sql)


def loadEspnPlayByPlayData(f):

    str_fields = open(constants.LOGDIR_CLEAN + f, 'r').readline()
    sql = """
        LOAD DATA LOCAL INFILE '%s' REPLACE
        INTO TABLE %s
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (%s)
    """ % (constants.LOGDIR_CLEAN + f, tables['playbyplay_espn'], str_fields)
    db.nba_query(sql)


def loadCbsSportsBoxScore(f):

    str_fields = open(constants.LOGDIR_CLEAN + f, 'r').readline()
    sql = """
        LOAD DATA LOCAL INFILE '%s' REPLACE
        INTO TABLE %s
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (%s)
    """ % (constants.LOGDIR_CLEAN + f, tables['boxscore_cbssports'], str_fields)
    db.nba_query(sql)


def loadShotChartNbaCom(f):
    shots = json.loads(open(LOGDIR_CLEAN + f,'r').readline())
    for shot in shots:
        sql = """
            INSERT INTO nba_staging.shotchart_nbacom
            (game_id, player_id, x, y, nbacom_play_type_id, nbacom_play_num, period, deciseconds_left, team_id,  shot_made) VALUES
            (%s, %s, "%s", "%s", %s, %s, %s, %s, %s, %s)
        """ % (
            shot['game_id'], shot['player_id'], shot['x'], shot['y'], shot['act'], shot['id'],
            shot['prd'], shot['time'], shot['tm'], shot['result']
        )

        db.nba_query(sql)


def loadShotChartEspn(f):
    shots = json.loads(open(LOGDIR_CLEAN + f,'r').readline())
    for shot in shots:
        sql = """
            INSERT INTO nba_staging.shotchart_espn
            (game_id, player_id, x, y, shot_type, espn_play_num, period, deciseconds_left, team_id,  shot_made, distance)
            VALUES
            (%s, %s, "%s", "%s", "%s", %s, %s, %s, %s, %s, %s)
        """ % (
            shot['game_id'], shot['player_id'], shot['x'], shot['y'], shot['shot_type'], shot['id'],
            shot['qtr'], shot['time_left'], shot['t'], shot['result'], shot['distance']
        )

        db.nba_query(sql)


def go(tuple_games_and_files):
    for gamedata, filenames in tuple_games_and_files:
        loadCbsSportsShotData(filenames['shotchart_cbssports'])
        loadEspnPlayByPlayData(filenames['playbyplay_espn'])
        loadCbsSportsBoxScore(filenames['boxscore_cbssports'])
        loadShotChartNbaCom(filenames['shotchart_nbacom'])
        loadShotChartEspn(filenames['shotchart_espn'])
        

def test():
    f = '2011-12-25_LAC@GS_shotchart_espn'
    loadShotChartEspn(f)


if __name__ == '__main__':
    test()
