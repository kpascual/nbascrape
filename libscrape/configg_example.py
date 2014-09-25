import db

prod = {
    'user': 'username_here',
    'passwd': 'password_here',
    'db': 'database_here'
}


# Database credential for main ETL run
dbobj = db.Db(prod)

# Current season and season type
config = {}
config['season'] = '2013-2014'
config['season_type'] = 'PRE'
config['league'] = 'nba' # nba, wnba


