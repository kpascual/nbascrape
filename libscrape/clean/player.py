from BeautifulSoup import BeautifulStoneSoup
import csv
import os
import logging
from libscrape.config import db
from libscrape.config import constants 


logging.basicConfig(format='%(asctime)s %(message)s',filename='player.log')
# Script to resolve player differences between NBA.com, CBSSports.com, and ESPN.com sources
# Use NBA.com and CBSSports first, because they're more well-defined


# Take the new files provided, and look them up in the master player table

LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class PlayerNbaCom:

    def __init__(self, filename):
        self.xml = open(filename,'r').read()
        self.soup = BeautifulStoneSoup(self.xml)


    def resolveNewPlayers(self):
        players = self.getPlayers()
        self.checkStaging(players)


    def getPlayers(self):
        soup = self.soup
        playbyplaydata = soup.findAll("pl")

        home_team = soup.find("htm")
        away_team = soup.find("vtm")

        all_players = []
        for team_name, team in [('home',home_team), ('away',away_team)]:
            
            players = team.findAll("pl")
            team_data = team['tm'].split('|')[-1]


            for player in players:
                player_data = player['name'].split('|')
                player_data.append(team_data)
                all_players.append(player_data)

        return all_players


    def checkStaging(self, players):
        for row in players:
            nbacom_player_id    = row[0]
            player_tag          = row[1]
            last_name           = row[2].split(',')[0].strip()
            first_name          = ' '.join(row[2].split(',')[1:]).strip()
            jersey_number       = row[5]
            team                = row[6]


            if nbacom_player_id:
                result = db.nba_query("SELECT * FROM nba_staging.player_nbacom WHERE nbacom_player_id = '%s'" % (nbacom_player_id))
                if not result:
                    print "cannot find %s.  inserting into db" % (row[2])
                    sql = """
                        INSERT INTO nba_staging.player_nbacom 
                            (nbacom_player_id, player_tag, last_name, first_name, jersey_number) 
                        VALUES ("%s","%s","%s","%s",%s)
                    """ % (nbacom_player_id, player_tag, last_name, first_name, jersey_number)
                    
                    db.nba_query(sql)
                    logging.debug("Found new player in NBA.com files: %s" % (row[2]))
                else:
                    # we found a matching record, skip.
                    pass
       

class PlayerCbsSports: 
    def __init__(self, filename):
        reader = csv.reader(open(filename,'r'),delimiter=',',lineterminator='\n')
        self.data = [row for row in reader]

    def checkStaging(self):
        for row in self.data:
            cbssports_player_id = row[1]
            full_name           = row[2].replace('&nbsp;',' ').strip()
            jersey_number       = row[3]
            cbs_team_code       = row[0]
            position            = row[4]
            

            if cbssports_player_id:
                result = db.nba_query("SELECT * FROM nba_staging.player_cbssports WHERE cbssports_player_id = '%s'" % (cbssports_player_id))

                if not result:
                    print "cannot find.  inserting into db"
                    db.nba_query("""
                        INSERT INTO nba_staging.player_cbssports
                            (cbssports_player_id, full_name, jersey_number, cbs_team_code, position) 
                        VALUES ("%s","%s","%s","%s","%s")
                    """ % (cbssports_player_id, full_name, jersey_number, cbs_team_code, position))
                    print "cannot find %s.  inserting into db" % (full_name)
                    logging.debug("Found new player in CBSSports.com files: %s" % (full_name))


def populateOldPlayers():
    nbacom_files = sorted([f for f in os.listdir(LOGDIR_EXTRACT) if 'boxscore_nbacom' in f])
    cbssports_files = sorted([f for f in os.listdir(LOGDIR_EXTRACT) if 'cbssports_players' in f])
   
    for f in nbacom_files:
        print f
        obj = PlayerNbaCom(LOGDIR_EXTRACT + f)
        obj.resolveNewPlayers()

    for f in cbssports_files:
        print f
        obj = PlayerCbsSports(LOGDIR_EXTRACT + f)
        obj.checkStaging()    


def main():

    #files = [f for f in os.listdir(LOGDIR_EXTRACT) if '2011-12' in f and 'boxscore' in f]
    f = '2011-12-22_CHA@ATL_shotchart_cbssports_players'
    f = '2011-12-22_CHA@ATL_boxscore_nbacom'

    obj = PlayerNbaCom(LOGDIR_EXTRACT + f)
    obj.resolveNewPlayers()


if __name__ == '__main__':
    populateOldPlayers()
    #main()
