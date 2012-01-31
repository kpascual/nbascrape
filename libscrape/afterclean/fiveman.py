from libscrape.config import db
import json

class FiveMan:
    def __init__(self, gamedata):
        self.gamedata = gamedata
        self.game_id = self.gamedata['id']
        self.away_team = self.gamedata['away_team_id']
        self.home_team = self.gamedata['home_team_id']
        self.date_played = self.gamedata['date_played']


    def go(self):
        home_units = self.getHomeFiveManUnit()
        away_units = self.getAwayFiveManUnit()

        #print json.dumps(home_units)

        #self._saveToDatabase(away_units, home_units)

        print "Successfully identified five man units!"
        return True


    def getHomeFiveManUnit(self):
        result = db.nba_query_dict("""
            SELECT * 
            FROM playbyplay_espn 
            WHERE game_id = %s  
            ORDER BY period ASC, sec_elapsed_game ASC, play_num ASC
        """ % self.game_id)
        players = self._getCurrentPlayers(self.home_team) 
        total_periods = self._getNumberOfPeriods()

        print players
        fiveman = self._guessFiveManUnits(result, total_periods, self.home_team, players)        
        return fiveman


    def getAwayFiveManUnit(self):
        result = db.nba_query_dict("""
            SELECT * 
            FROM playbyplay_espn 
            WHERE game_id = %s  
            ORDER BY period ASC, sec_elapsed_game ASC, play_num ASC
        """ % self.game_id)
        players = self._getCurrentPlayers(self.away_team) 
        total_periods = self._getNumberOfPeriods()
       
        fiveman = self._guessFiveManUnits(result, total_periods, self.away_team, players) 
        return fiveman


    def _getCurrentPlayers(self, team_id):
        sql = """ 
            SELECT p.id
            FROM player_nbacom_by_game nbacom
                INNER JOIN player_resolved_test p ON p.nbacom_player_id = nbacom.nbacom_player_id
            WHERE nbacom.team = %s AND nbacom.game_id = %s
        """ % (team_id, self.game_id)
        return [itm[0] for itm in db.nba_query(sql)]


    def _getNumberOfPeriods(self):
        return db.nba_query("""
            SELECT MAX(period) FROM playbyplay_espn 
            WHERE game_id = %s  and period <= 4
        """ % self.game_id)[0][0]


    def _guessFiveManUnits(self, data, period_count, team_id, known_players):

        PLAY_ID_PLAYER_ENTERS   = 48
        PLAY_ID_FOUL            = 93

        # Split data into respective periods
        data_by_periods = []
        for i in range(1,period_count+1):
            data_by_periods.append([play_data for play_data in data if play_data['period'] == i])


        all_units = []
        for data_in_period in data_by_periods:
            units_in_period = [] 
            
            # Go through every play in each period, and identify the five man unit
            for play_data in data_in_period: 
                switches = {}
                
                if units_in_period and play_data['period'] == units_in_period[-1]['period']:
                    fiveman_unit = [p for p in units_in_period[-1]['unit']]
                else:
                    fiveman_unit = []
       

                # Check if any players found in the play description aren't already in the 
                # five man unit
                players_in_play = [
                    play_data['player_id'],
                    play_data['player1_id'],
                    play_data['player2_id'],
                    play_data['assist_player_id']
                ] 
                for player in players_in_play:
                    if player in known_players and player not in fiveman_unit and play_data['play_id'] != PLAY_ID_FOUL:
                        fiveman_unit.append(player)

                        # Additionally, if they didn't just enter, backfill the prior plays with the player
                        if play_data['play_id'] != PLAY_ID_PLAYER_ENTERS:
                            units_in_period = self._backfillPlayerInPriorPlays(player, units_in_period)


                # Play Id for players entering & exiting game
                # Handle enter/exits
                if play_data['play_id'] == PLAY_ID_PLAYER_ENTERS and play_data['team_id'] == team_id: 
                
                    try:
                        fiveman_unit.remove(play_data['player2_id']) 
                        
                        units_in_period = self._backfillPlayerInPriorPlays(play_data['player2_id'], units_in_period)
                        """
                        for play_index, prev_data in enumerate(reversed(units_in_period)):
                            if play_data['player2_id'] not in prev_data['unit']: 
                                idx = len(units_in_period) - 1 - play_index
                                units_in_period[idx]['unit'].append(play_data['player2_id'])
                            else:
                                break 
                        """
                        switches = {'enter':play_data['player_id'], 'exit':play_data['player2_id']}
                    except:
                        print "Couldn't find player %s.  Should this person be added into prior list?" % play_data['player2_id']	
                new_data = {
                    'play_number':play_data['play_num'],
                    'period':play_data['period'],
                    'unit':fiveman_unit,
                    'switches':switches
                }
                units_in_period.append(new_data)
                
            all_units.append(units_in_period)

        return all_units


    def _switchOutPlayers(self):
        pass    


    def _backfillPlayerInPriorPlays(self, player_id, list_units):
        for play_index, prev_data in enumerate(reversed(list_units)):
            if player_id in prev_data['unit'] or (prev_data['switches'] and player_id ==  prev_data['switches']['enter']):
                break
            else:
                idx = len(list_units) - 1 - play_index
                list_units[idx]['unit'].append(player_id)
        
        return list_units


    def _removePlayerFromPriorPlays(self, player_id, units_in_period):

        for play_index, prev_data in enumerate(reversed(units_in_period)):
            if player_id not in prev_data['unit']: 
                idx = len(units_in_period) - 1 - play_index
                units_in_period[idx]['unit'].append(play_data['player2_id'])
            else:
                break 
        switches = (play_data['player_id'],play_data['player2_id'])


    def _saveToDatabase(self, away_fiveman, home_fiveman):

        # Away fiveman unit
        for quarter_row in away_fiveman:
            for row in quarter_row:
                db.nba_query("""
                    UPDATE pbp2 SET away_fiveman = '%s' WHERE game_id = %s AND play_num = %s AND period = %s
                """ % (','.join(map(str,row['unit'])), self.game_id, row['play_number'], row['period']))

        # home fiveman unit
        for quarter_row in home_fiveman:
            for row in quarter_row:
                db.nba_query("""
                    UPDATE pbp2 SET home_fiveman = '%s' WHERE game_id = %s AND play_num = %s AND period = %s
                """ % (','.join(map(str,row['unit'])), self.game_id, row['play_number'], row['period']))


def main(game_id = 1500):
    gamedata = db.nba_query_dict("SELECT * FROM game WHERE id = %s" % game_id)
    obj = FiveMan(gamedata[0])
    
    obj.go()

if __name__ == '__main__':
    main()
