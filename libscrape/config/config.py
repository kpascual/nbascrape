from libscrape.config import db

config = {}

# Database credential for main ETL run
config['db'] = db.dbconn_nba

# Current season and season type
config['season'] = '2012-2013'
config['season_type'] = 'REG'


season = '2012-2013'
season_type = 'REG'
