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
        

def main():

    last = datetime.date(2012,2,11)

    first = datetime.date(2012,2,4)

    while first < last:
        #master.restartFromExtract(first)
        master.getAll(first)
        first = first + datetime.timedelta(days=1)


if __name__ == '__main__':
    updateBoxScoreTeamIds()

