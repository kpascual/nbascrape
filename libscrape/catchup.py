import master
import datetime
import afterclean.fiveman
import clean.boxscore_nbacom
import load.main
from libscrape.config import db


def checkClean():
    dt = datetime.date(2010,10,26)
    master.restartFromClean(dt)


def fillFiveman():

    for i in range(1,860):
        try:
            afterclean.fiveman.main(i)
            print "Fiveman for game %s completed" % i
        except:
            print "Couldn't find game %s" % i


def updateBoxScoreTeamIds():
    dbobj = db.Db(db.dbconn_nba)
    allgames = dbobj.query_dict("SELECT * FROM game WHERE date_played <= '2012-02-27'")

    for game in allgames:
        filename = game['abbrev'] + '_boxscore_nbacom'
        print "+++ Creating NBA.com boxscore data %s " % (game['abbrev']) 
        clean.boxscore_nbacom.CleanBoxScore(filename,game,dbobj).clean()
        print "+++ Loading NBA.com boxscore data %s"  % (game['abbrev'])
        load.main.Load(dbobj).loadBoxScoreNbaCom(filename)
       

def dumpPlayByPlay():
    sql = """
        select g.abbrev, p.period, p.deciseconds_left, p.away_score, p.home_score, p.play_desc from playbyplay_espn p inner join game g on g.id = p.game_id where g.season = '2011-2012' and g.season_type IN ('REG','POST')
    """ 
    dbobj = db.Db(db.dbconn_nba)

    result = dbobj.query(sql)
    print result[:5]


def main():

    last = datetime.date(2012,4,26)

    first = datetime.date(2012,1,21)

    while first < last:
        #master.restartFromExtract(first)
        master.getAll(first)
        first = first + datetime.timedelta(days=1)


if __name__ == '__main__':
    dumpPlayByPlay()

