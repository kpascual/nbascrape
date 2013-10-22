from config import db
from config import config

class League:

    def __init__(self, dbobj):
        self.dbobj = dbobj


    def getGames(self, dt):
        return self.dbobj.query_dict("""
            SELECT g.*, home_team.city home_team_city, away_team.city away_team_city 
            FROM game g 
                INNER JOIN team home_team on home_team.id = g.home_team_id
                INNER JOIN team away_team on away_team.id = g.away_team_id
            WHERE g.date_played = '%s'
                AND g.should_fetch_data = 1
        """ % (dt))


    def getSeason(self, dt):
        data = self.dbobj.query_dict("""
            SELECT *
            FROM dim_season
            WHERE start_date <= '%s'
                AND end_date >= '%s'
        """ % (dt, dt))
        return data[0] if data else {}


def main():
    dbobj = db.Db(config.config['db'])
    lgobj = League(dbobj)
    season = lgobj.getSeason('2013-10-20')



if __name__ == '__main__':
    main()


