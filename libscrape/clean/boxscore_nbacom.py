import re
import datetime
import csv
from BeautifulSoup import BeautifulStoneSoup
import os


from libscrape.config import db
from libscrape.config import constants 


LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class Clean:

    def __init__(self, filename, gamedata):
        self.xml = open(LOGDIR_EXTRACT + filename,'r').read()
        self.soup = BeautifulStoneSoup(self.xml)
        self.gamedata = gamedata


    def view(self):
        print self.soup.prettify()
        self.getStats()


    def getOfficials(self):
        soupofficials = self.soup.find("officials")
        
        officials = dict(soupofficials.attrs)['nm'].split('|')
        print officials


    def getPlayerLines(self):
        team_data = self.soup.find("vtm")
        players = team_data.findAll("pl")

        for p in players:
            print p.attrs
        

    def getTeamNames(self):
        soup = self.soup
        home_team = soup.find("htm")
        away_team = soup.find("vtm")
       
        print home_team['tm']
        print away_team['tm']


    def getStats(self):
        soup = self.soup
        playbyplaydata = soup.findAll("pl")

        home_team = soup.find("htm")
        away_team = soup.find("vtm")
        existing_players = self._getExistingPlayerIds()

        player_stats = []
        for team_name, team in [('home',home_team), ('away',away_team)]:
            players = team.findAll("pl")

            for p in players:
                player_stat_line = {}
                player_data = p['name'].split('|')
                nbacom_player_id = player_data[0]

                try:
                    player_stat_line['player_id'] = existing_players[nbacom_player_id]
                except:
                    player_stat_line['player_id'] = 0

                parsed_stats = self._parseStatLine(player_data['stat'])
                player_stat_line.update(parsed_stats)

                player_stats.append(player_stat_line)


        for stat in player_stats:
            print stat
        #print home_team.prettify()
        #print away_team.prettify()
        
    def _parseStatLine(raw_stats):
        time_played,fg,3pt,ft, = raw_stats.split('|')

    def getShotChartData(self):
        pass


    def _getExistingPlayerIds(self):
        players = db.nba_query_dict("SELECT * FROM nba_staging.player_resolved_test")
        # Index by nbacom_player_id
    
        players_indexed = {}
        for player in players:
            players_indexed[player['nbacom_player_id']] = player['id']

        return players_indexed


    def _transformTimeToTenthSeconds(self, game_clock):

        mins, secs = game_clock.split(':')
        total_secs = int(mins)*60*10 + int(float(secs) * 10)

        return total_secs


    def _getPlayerId(self, player_code):
        pass


def main():

    files = [f for f in os.listdir(LOGDIR_EXTRACT) if '2011-12' in f and 'boxscore' in f]
    f = '2011-12-21_LAL@LAC_boxscore_nbacom'

    gamedata = db.nba_query("SELECT * FROM game where id = 1263") 
    obj = Clean(f, gamedata)
    obj.view()
    

if __name__ == '__main__':
    main()
