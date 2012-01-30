from libscrape.config import constants
from BeautifulSoup import BeautifulStoneSoup
import csv
import re


LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

class Extract():

    def __init__(self, xml, filename, game_name, away_team, home_team):
        self.xml = xml
        self.game_name = game_name
        self.filename = filename
        self.soup = BeautifulStoneSoup(self.xml)
        
        self.home_team = home_team
        self.away_team = away_team

    
    def extract(self):
        plays = self.splitRowsIntoPlays()
        row_indexes = self.getPeriodIndexes()
        indexed_plays = self.combinePlaysWithPeriodIndexes(row_indexes, plays)
        self.dumpToFile(indexed_plays)

    def getGameData(self):
        gamedata = self.soup.find("game")
        print gamedata.attrs

    def getPlayByPlayData(self):
        playbyplaydata = self.soup.findAll("event")

        for play in playbyplaydata:
            print dict(play.attrs)
    
    def dumpToFile(self, list_data):
        writer = csv.writer(open(LOGDIR_EXTRACT + self.filename + '_pbp_nbacom','wb'),delimiter=',',lineterminator='\n')
        writer.writerows(list_data)


if __name__ == '__main__':
    f = '2011-12-17_SAC@GS_pbp_nbacom'
    obj = Extract(open('../../logs/source/' + f,'r').read(),f, f.replace('pbp_nbacom',''),'SAC','GS')
    
    print obj.getGameData()
    print obj.getPlayByPlayData()




