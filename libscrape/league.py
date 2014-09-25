from config import db
from config import config

class League:

    def __init__(self, dbobj, name):
        self.dbobj = dbobj
        self.name = name
        self.obj = self._getLeague()
        if self.obj:
            self.league_season = self._getLeagueSeason()
        else:
            self.league_season = False


    def getGames(self, dt):
        return self.dbobj.query_dict("""
            SELECT g.*, home_team.city home_team_city, away_team.city away_team_city 
            FROM game g 
                INNER JOIN team home_team on home_team.id = g.home_team_id
                INNER JOIN team away_team on away_team.id = g.away_team_id
            WHERE g.date_played = '%s'
                AND g.should_fetch_data = 1
                AND g.league_season_id = %s
        """ % (dt, self.league_season['id']))


    def getSeason(self, dt):
        data = self.dbobj.query_dict("""
            SELECT *
            FROM dim_season
            WHERE start_date <= '%s'
                AND end_date >= '%s'
        """ % (dt, dt))
        return data[0] if data else {}


    def getTeams(self, season):
        return self.dbobj.query_dict("""
            SELECT *
            FROM team
            WHERE season = '%s'
        """ % (season))


    def matchTeam(self, team_name, teams):
        print team_name
        for team in teams:
            if team_name == team['name']:
                return team
            elif team_name == team['nickname']:
                return team
            elif team_name == team['alternate_nickname']:
                return team
            elif team_name == team['alternate_nickname2']:
                return team
            elif team_name == team['city']:
                return team
            elif team_name == team['alternate_city'] + ' ' + team['nickname']:
                return team
            elif team_name == team['alternate_city'] + ' ' + team['alternate_nickname']:
                return team
            elif team_name == team['alternate_city'] + ' ' + team['alternate_nickname2']:
                return team

        return False



    def _getLeague(self):
        query = self.dbobj.query_dict("SELECT * FROM league WHERE name = '%s'" % (self.name))
        if query:
            return query[0]
        else:
            return False


    def _getLeagueSeason(self):
        query = self.dbobj.query_dict("SELECT * FROM league_season WHERE league_id = %s AND is_current = 1" % (self.obj['id']))
        if query:
            return query[0]
        else:
            return False


    def getModules(self):
        module_map = {
            'nba': [
                'boxscore_nbacom',
                'boxscore_cbssports',
                'playbyplay_espn',
                'playbyplay_nbacom',
                'shotchart_cbssports',
                'shotchart_espn',
                'shotchart_nbacom',
                'playbyplay_statsnbacom',
                'shotchart_statsnbacom',
                'boxscore_statsnbacom'
            ],
            'wnba': [
                'boxscore_wnbacom',
                'playbyplay_espn_wnba',
                'playbyplay_wnbacom',
                'shotchart_espn_wnba',
                'shotchart_wnbacom'
            ]    
            
        }

        return module_map[self.obj['slug']]



def main():
    dbobj = db.Db(config.config['db'])
    lgobj = League(dbobj)
    season = lgobj.getSeason('2014-04-19')
    print season



if __name__ == '__main__':
    main()


