from libscrape.config import constants
from libscrape.config import db
import os
import csv


def main():

    files = [f for f in os.listdir(constants.LOGDIR_EXTRACT) if 'pbp_espn' in f]
    for f in files:
        print f
        game_id = db.nba_query("SELECT id FROM game WHERE abbrev = '%s'" % f.replace('_pbp_espn',''))[0][0]

        newfiledata = []
        newfiledata = [[game_id] + line.rstrip().split(',') for line in open(constants.LOGDIR_EXTRACT + f,'r')]
        writer = csv.writer(open(constants.LOGDIR_EXTRACT + 'tmpextract_ref','wb'),delimiter=',',lineterminator='\n')
        writer.writerows(newfiledata)

        sql = """
            LOAD DATA LOCAL INFILE '%s' REPLACE
            INTO TABLE extract_ref
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
            (game_id,period_name, play_num, time_left,away_score,home_score,away_play,home_play)
        """ % (constants.LOGDIR_EXTRACT + 'tmpextract_ref')
        db.nba_query(sql)


if __name__ == '__main__':
    main()
