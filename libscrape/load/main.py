from libscrape.config import db
from libscrape.config import constants

def loadShots(f):
   
    str_fields = open(constants.LOGDIR_CLEAN + f, 'r').readline()
    sql = """
        LOAD DATA LOCAL INFILE '%s' REPLACE
        INTO TABLE %s
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (%s)
    """ % (constants.LOGDIR_CLEAN + f, 'shottest', str_fields)
    db.nba_query(sql)


def loadPlayByPlay(f):

    str_fields = open(constants.LOGDIR_CLEAN + f, 'r').readline()
    sql = """
        LOAD DATA LOCAL INFILE '%s' REPLACE
        INTO TABLE %s
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (%s)
    """ % (constants.LOGDIR_CLEAN + f, 'pbptest', str_fields)
    db.nba_query(sql)


def loadInitialBoxScore(f):

    str_fields = open(constants.LOGDIR_CLEAN + f + '_boxscore', 'r').readline()
    sql = """
        LOAD DATA LOCAL INFILE '%s' REPLACE
        INTO TABLE %s
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (%s)
    """ % (constants.LOGDIR_CLEAN + f + '_boxscore', 'boxscore', str_fields)
    db.nba_query(sql)


def go(tuple_games_and_files):
    for (gamedata,(file_cbssports, file_espn)) in tuple_games_and_files:
        loadShots(file_cbssports)
        loadPlayByPlay(file_espn)
        loadInitialBoxScore(file_cbssports)




