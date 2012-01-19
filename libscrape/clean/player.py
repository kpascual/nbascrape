from BeautifulSoup import BeautifulStoneSoup
import csv
import os
import logging
import datetime
import difflib
from libscrape.config import db
from libscrape.config import constants 


logging.basicConfig(format='%(asctime)s %(message)s',filename='player.log',level=logging.DEBUG)
# Script to resolve player differences between NBA.com, CBSSports.com, and ESPN.com sources
# Use NBA.com and CBSSports first, because they're more well-defined


# Take the new files provided, and look them up in the master player table

LOGDIR_CLEAN = constants.LOGDIR_CLEAN
LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT


class PlayerNbaCom:

    def __init__(self, filename, game_data = None):
        self.xml = open(filename,'r').read()
        self.soup = BeautifulStoneSoup(self.xml)
        self.date_played = filename.replace(LOGDIR_EXTRACT,'')[:10]
        self.game_data = game_data


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
                db.nba_query("""
                    INSERT INTO nba_staging.player_nbacom_by_game
                        (nbacom_player_id, game_id, player_tag, last_name, first_name, jersey_number, team) 
                    VALUES ("%s","%s","%s","%s","%s","%s", "%s")
                """ % (nbacom_player_id, self.game_data['id'], player_tag, last_name, first_name, jersey_number, team))

                result = db.nba_query("SELECT * FROM nba_staging.player_nbacom WHERE nbacom_player_id = '%s'" % (nbacom_player_id))
                if not result:
                    print "cannot find %s.  inserting into db" % (row[2])
                    sql = """
                        INSERT INTO nba_staging.player_nbacom 
                            (nbacom_player_id, player_tag, last_name, first_name, date_found) 
                        VALUES ("%s","%s","%s","%s","%s")
                    """ % (nbacom_player_id, player_tag, last_name, first_name, self.date_played)
                    
                    db.nba_query(sql)

                    # Add to resolved player table
                    result = db.nba_query("""
                        INSERT INTO nba_staging.player_resolved_test
                            (nbacom_player_id, last_name, first_name, date_found) 
                        VALUES ("%s","%s","%s","%s")
                    """ % (nbacom_player_id, last_name, first_name, self.date_played))

                    logging.debug("Found new player in NBA.com files: %s" % (row[2]))

                else:
                    # we found a matching record, skip.
                    pass

                self.managePlayerTeamHistory(nbacom_player_id, team)
    
    
    def managePlayerTeamHistory(self, nbacom_player_id, nbacom_team_code): 

        player_id = db.nba_query("""
            SELECT p.id
            FROM 
                nba_staging.player_resolved_test p 
            WHERE 
                p.nbacom_player_id = "%s"
        """ % (nbacom_player_id))[0][0]
       
        team_id = '' 
        team_id = db.nba_query("""
            SELECT id
            FROM team
            WHERE nbacom_code = "%s"
        """ % (nbacom_team_code))[0][0]
        
        # Add to team-player history table if it isn't already existing
        check_team = db.nba_query("""
            SELECT id FROM nba_staging.player_team_history
            WHERE player_id = %s AND team_id = "%s" AND end_date IS NULL
        """ % (player_id, team_id)) 

        if not check_team:
            # If exists, close out most recent record
            player_team_history = db.nba_query("""
                SELECT id FROM nba_staging.player_team_history
                WHERE player_id = %s AND end_date IS NULL
            """ % (player_id))
           
            if player_team_history:
                player_team_history_id = player_team_history[0][0] 
                db.nba_query("""
                    UPDATE nba_staging.player_team_history SET end_date = "%s" WHERE id = %s
                """ % (self.date_played, player_team_history_id))
                logging.info("""
                    Closing out player team history for player_id: %s, player_team_history_id: %s
                """ % (player_id, player_team_history_id))

            # Add new record
            db.nba_query("""
                INSERT IGNORE INTO nba_staging.player_team_history
                (player_id, team_id, start_date)
                SELECT id, %s, "%s"
                FROM
                    nba_staging.player_resolved_test p
                WHERE
                    p.id = "%s"
            """ % (team_id, self.date_played, player_id))
            logging.info("""
                Added new player team history for player_id %s; date: %s; team: %s
            """ % (player_id, self.date_played, team_id))


class PlayerCbsSports: 
    def __init__(self, filename, game_data = None):
        reader = csv.reader(open(filename,'r'),delimiter=',',lineterminator='\n')
        self.data = [row for row in reader]
        self.date_played = filename.replace(LOGDIR_EXTRACT,'')[:10]
        self.game_data = game_data


    def resolveNewPlayers(self):
        for row in self.data:
            cbssports_player_id = row[1]
            full_name           = row[2].replace('&nbsp;',' ').strip()
            first_name          = full_name.split(' ')[0]
            last_name           = ' '.join(full_name.split(' ')[1:])
            jersey_number       = row[3]
            cbs_team_code       = row[0]
            position            = row[4]

            if cbssports_player_id:
                db.nba_query("""
                    INSERT INTO nba_staging.player_cbssports_by_game
                    (game_id, cbssports_player_id, full_name, first_name, last_name, cbs_team_code, jersey_number, position)
                    VALUES
                    (%s,"%s", "%s", "%s", "%s", "%s", "%s", "%s")
                """ % (self.game_data['id'], cbssports_player_id, full_name, first_name, last_name, cbs_team_code, jersey_number, position))

                result = db.nba_query("SELECT * FROM nba_staging.player_cbssports WHERE cbssports_player_id = '%s'" % (cbssports_player_id))

                if not result:
                    print "cannot find.  inserting into db"
                    db.nba_query("""
                        INSERT INTO nba_staging.player_cbssports
                            (cbssports_player_id, full_name, first_name, last_name, date_found) 
                        VALUES ("%s","%s","%s","%s","%s")
                    """ % (cbssports_player_id, full_name, first_name, last_name, self.date_played))
                    print "cannot find %s.  inserting into db" % (full_name)
                    logging.debug("Found new player in CBSSports.com files: %s" % (full_name))

                self.matchWithResolvedPlayer(cbssports_player_id, full_name, cbs_team_code, self.game_data['id'])


    def matchWithResolvedPlayer(self, cbssports_player_id, full_name, cbs_team_code, game_id):
        existing_player = db.nba_query("""
            SELECT * FROM nba_staging.player_resolved_test
            WHERE cbssports_player_id = %s
        """ % (cbssports_player_id))

        if not existing_player:
            team_codes = db.nba_query("SELECT nbacom_code, code, id FROM team WHERE id = '%s'" % (cbs_team_code))[0]
            nbacom_team_code = team_codes[0]
            team_code = team_codes[1]
            team_id = team_codes[2]

            # Get list of possible matches from nba.com names
            result = db.nba_query("""
                SELECT nbacom_player_id, first_name, last_name
                FROM nba_staging.player_nbacom_by_game
                WHERE game_id = '%s' AND team = '%s'
            """ % (game_id, nbacom_team_code))

            names = [' '.join(row[1:]) for row in result]
            match = difflib.get_close_matches(full_name, names, 1, 0.8)

            if match:
                best_match = match[0]
                matched_nbacom_player_id = result[names.index(best_match)][0]
                
                db.nba_query("""
                    UPDATE nba_staging.player_resolved_test
                    SET cbssports_player_id = "%s"
                    WHERE nbacom_player_id = "%s"
                        AND cbssports_player_id IS NULL
                """ % (cbssports_player_id, matched_nbacom_player_id))
            else:
                logging.debug("Could not match player %s.  Skipping." % (full_name))
                print "Could not match player %s, %s. Skipping" % (full_name, cbssports_player_id)
                
            # Else, check by first name/last name, game_id


class ResolvePlayer:
    def __init__(self, dt):
        self.dt = dt


    def addNbaComPlayers(self):
        pass

    def resolveCbsSportsPlayers(self):
        result = db.nba_query("""
            SELECT nbacom_player_id, last_name, first_name, jersey_number, date_found
            FROM nba_staging.player_nbacom WHERE date_found = '%s'
        """ % (self.dt))

        for player_data in result:
            matched_players = db.nba_query("""
                SELECT nbacom_player_id
                FROMa
            """)


def populateOldPlayers():
    nbacom_files = sorted([f for f in os.listdir(LOGDIR_EXTRACT) if 'boxscore_nbacom' in f])
    cbssports_files = sorted([f for f in os.listdir(LOGDIR_EXTRACT) if 'cbssports_players' in f])
  
    """
    for f in nbacom_files:
        print f
        game_data = db.nba_query_dict("SELECT * FROM nba.game WHERE abbrev = '%s'" % (f.replace('_boxscore_nbacom','')))[0]
        obj = PlayerNbaCom(LOGDIR_EXTRACT + f, game_data)
        obj.resolveNewPlayers()
    """

    for f in cbssports_files:
        print f
        game_data = db.nba_query_dict("SELECT * FROM nba.game WHERE abbrev = '%s'" % (f.replace('_shotchart_cbssports_players','')))[0]
        obj = PlayerCbsSports(LOGDIR_EXTRACT + f, game_data)
        obj.resolveNewPlayers()    


def main():

    #files = [f for f in os.listdir(LOGDIR_EXTRACT) if '2011-12' in f and 'boxscore' in f]
    f = '2011-12-26_PHI@POR_shotchart_cbssports_players'
    f2 = '2011-12-26_PHI@POR_boxscore_nbacom'

    game_data = db.nba_query_dict("SELECT * FROM game WHERE id = 1279")[0]
    dt = datetime.date(2011, 12, 20)
    #obj = ResolvePlayer(dt)
    #obj.addNbaComPlayers()

    obj = PlayerNbaCom(LOGDIR_EXTRACT + f2, game_data)
    obj.resolveNewPlayers()
    obj = PlayerCbsSports(LOGDIR_EXTRACT + f, game_data)
    obj.resolveNewPlayers()


if __name__ == '__main__':
    #populateOldPlayers()
    main()
