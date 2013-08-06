from libscrape.config import db

config = {}

# Database credential for main ETL run
config['db'] = db.dbconn_prod

# Current season and season type
config['season'] = '2012-2013'
config['season_type'] = 'REG'
config['league'] = 'nba' # nba, wnba


season = '2012-2013'
season_type = 'REG'

league = {
    'nba': {
        'db': db.dbconn_prod,
        'season': '2012-2013',
        'season_type': 'REG',
        'league': 'nba'
    },
    'wnba': {
        'db': db.dbconn_wnba,
        'season': '2013',
        'season_type': 'REG',
        'league': 'wnba'
    }
}
