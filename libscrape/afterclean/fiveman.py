from libscrape.config import db


class FiveMan:
    def __init__(self, game_id, away_team, home_team, date_played):
        self.game_id = game_id
        self.away_team = away_team 
        self.home_team = home_team
        self.date_played = date_played


    def go(self):
        self.getHomeFiveManUnit()
        self.getAwayFiveManUnit()


    def getHomeFiveManUnit(self):
        result = db.nba_query_dict("SELECT * FROM pbptest WHERE game_id = %s  ORDER BY period ASC, sec_elapsed_game ASC, play_num ASC" % self.game_id)
        players = self._getCurrentPlayers(self.home_team) 
        total_periods = self._getNumberOfPeriods()

        fiveman = self._guessFiveManUnits(result, total_periods, self.home_team, players)        
        return fiveman


    def getAwayFiveManUnit(self):
        result = db.nba_query_dict("SELECT * FROM pbptest WHERE game_id = %s  ORDER BY period ASC, sec_elapsed_game ASC, play_num ASC" % self.game_id)
        players = self._getCurrentPlayers(self.away_team) 
        total_periods = self._getNumberOfPeriods()
       
        fiveman = self._guessFiveManUnits(result, total_periods, self.away_team, players) 
        return fiveman


    def _getCurrentPlayers(self, team):
        sql = """ 
            SELECT id
            FROM player 
            WHERE start_date <= '%s' and (end_date >= '%s' OR end_date IS NULL) AND team_code = '%s'
        """ % (self.date_played, self.date_played, team)
        return [itm[0] for itm in db.nba_query(sql)]


    def _getNumberOfPeriods(self):
        return db.nba_query("SELECT MAX(period) FROM pbptest WHERE game_id = %s  and period <= 4" % self.game_id)[0][0]


    def _guessFiveManUnits(self, data, periods, team_code, players):

        # Split data into respective periods
        data_by_periods = []
        for i in range(1,periods+1):
            data_by_periods.append([itm for itm in data if itm['period'] == i])

        print "Number of periods: %s,%s" % (periods, len(data_by_periods))

        all_units = []
        for per in data_by_periods:
            list_units = [] 
            
            # Create unit list for every quarter/period
            for itm in per: 
                switches = ()
                if not list_units or itm['period'] != list_units[-1][1]:
                    this_unit = []
                else:
                    this_unit = [p for p in list_units[-1][2]]
        
                for player in [itm['player_id'],itm['player1_id'],itm['player2_id'],itm['assist_player_id']]:
                    
                    if player in players and player not in this_unit:
                        this_unit.append(player)
                        if itm['play_id'] != 48:
                            list_units = self._backfillIfPlayerDoesntExist(player, list_units)

                # Play Id for players entering & exiting game
                # Handle enter/exits
                if itm['play_id'] == 48 and itm['team_code'] == team_code: 
                
                    try:
                        this_unit.remove(itm['player2_id']) 

                        for i,prev_data in enumerate(reversed(list_units)):
                            if itm['player2_id'] not in prev_data[2]: 
                                idx = len(list_units) - 1 - i
                                list_units[idx][2].append(itm['player2_id'])
                            else:
                                break 
                        switches = (itm['player_id'],itm['player2_id'])
                    except:
                        print "Couldn't find player %s.  Should this person be added into prior list?" % itm['player2_id']	
                list_units.append((itm['play_num'],itm['period'],this_unit[:],switches))

            all_units.append(list_units)

        return all_units


    def _switchOutPlayers(self):
        pass    


    def _backfillIfPlayerDoesntExist(self, player, list_units):
        for i, prev_data in enumerate(reversed(list_units)):
            if player in prev_data[2] or (prev_data[3] and player ==  prev_data[3][0]):
                break
            else:
                idx = len(list_units) - 1 - i
                list_units[idx][2].append(player)
        
        return list_units


def main(game_id = 10):
    gamedata = db.nba_query("SELECT id, away_team, home_team, date_played FROM game WHERE id = %s" % game_id)
    obj = FiveMan(*gamedata[0])
    
    obj.go()

if __name__ == '__main__':
    main()
