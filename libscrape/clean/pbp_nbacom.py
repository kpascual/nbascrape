import re
import datetime
import csv
from BeautifulSoup import BeautifulStoneSoup

from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class Clean:

    def __init__(self, xml):
        self.xml = xml


    def getPlayByPlayData(self):
        soup = BeautifulStoneSoup(self.xml)
        playbyplaydata = soup.findAll("event")
        for play in playbyplaydata:
            playdata = dict(play.attrs)
            playdata['text'] = play.contents[0]
            playdata['seconds_left'] = self._transformTimeToTenthSeconds(playdata['game_clock'])
            print playdata


    def getShotChartData(self):
        pass


    def _transformTimeToTenthSeconds(self, game_clock):

        mins, secs = game_clock.split(':')
        total_secs = int(mins)*60*10 + int(float(secs) * 10)

        return total_secs


    def _getPlayerId(self, player_code):
        pass


def main():
    f = '2011-12-17_SAC@GS_pbp_nbacom'
    obj = Clean(open('../../logs/source/' + f,'r').read())
    
    print obj.getPlayByPlayData()


if __name__ == '__main__':
    main()
