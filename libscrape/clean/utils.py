from libscrape.config import config
from libscrape.config import db
from libscrape.config import constants 


class Utils:
    def __init__(self, dbobj):
        self.dbobj = dbobj


    def getAllPlayers(self):
        return self.dbobj.query_dict("""
            SELECT
                id, 
                full_name as name, 
                statsnbacom_player_id,
                nbacom_player_id,
                cbssports_player_id
            FROM
                player
        """)

