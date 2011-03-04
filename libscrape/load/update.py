from libscrape.config import db
from libscrape.config import constants



def updatePlayByPlay(f = ''):
    curs = db.nba_curs()
    curs.execute("CREATE TEMPORARY TABLE tmp LIKE pbptest")

    str_fields = open(constants.LOGDIR_CLEAN + f, 'r').readline()
    sql = """
        LOAD DATA LOCAL INFILE '%s' REPLACE
        INTO TABLE tmp 
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (%s)
    """ % (constants.LOGDIR_CLEAN + f,  str_fields)
    curs.execute(sql)

    curs.execute("""UPDATE pbptest p 
                  INNER JOIN tmp ON tmp.game_id = p.game_id AND tmp.play_num = p.play_num
                  SET p.player_id = tmp.player_id, p.player1_id = tmp.player1_id, p.player2_id = tmp.player2_id,
                    p.play_id = tmp.play_id""")


def go(tuple_games_and_files):
    for (gamedata,(file_cbssports, file_espn)) in tuple_games_and_files:
        loadShots(file_cbssports)
        loadPlayByPlay(file_espn)


if __name__ == '__main__':
    updatePlayByPlay()

