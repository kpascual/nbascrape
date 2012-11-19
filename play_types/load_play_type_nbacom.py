
from libscrape.config import db
from libscrape.config import constants 

dbobj = db.Db(db.dbconn_nba)


def main():

    patterns = [
        {'re':'play\s+not\s+identified','priority':5},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\s*End\s+Period(\]\]&gt;)*','priority':5,'is_period_startend':1,'name':'End Period'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\s*Start\s+Period(\]\]&gt;)*','priority':5,'is_period_startend':1,'name':'Start Period'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+Team\s+Rebound(\]\]&gt;)*','priority':5,'is_rebound':1,'is_team_play':1,'name':'Team Rebound'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+Team\s+Timeout\s+:\s+(Regular|Short)(\]\]&gt;)*','priority':5,'is_timeout':1,'name':'Team Timeout'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\s*Timeout\s+:\s+(Official|Regular)(\]\]&gt;)*','priority':5,'is_timeout':1,'name':'Official Timeout'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Rebound\s+\(Off:\d+\s+Def:\d+\)(\]\]&gt;)*','priority':5,'is_rebound':1,'name':'<player_id> Rebound'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+(?P<shot_type>(Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Missed(\]\]&gt;)*','priority':5,'is_shot':1,'is_shot_made':0,'name':'<player_id> <shot_type>: Missed'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+(?P<shot_type>(Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Missed\s+Block:\s*(?P<player2_id>[a-zA-Z-\.\'\s]+)\s*\(\d+\s+BLK\)(\]\]&gt;)*','priority':5,'is_shot':1,'is_shot_made':0,'is_block':1,'name':'<player_id> <shot_type>: Missed Block: <player2_id>'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*(?P<ft_count>\d)\s+of\s+(?P<ft_total>\d)\s+Missed(\]\]&gt;)*','priority':5,'is_freethrow':1,'is_freethrow_made':0,'name':'<player_id> Free Throw: x of x: Missed'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*(?P<ft_count>\d)\s+of\s+(?P<ft_total>\d)\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':5,'is_freethrow':1,'is_freethrow_made':1,'name':'<player_id> Free Throw: x of x: Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*\(\d+\s+PTS\)(\]\]&gt;)*','priority':5,'is_freethrow':1,'is_freethrow_made':1,'name':'<player_id> Free Throw: x of x: Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player2_id>[a-zA-Z-\.\'\s]+)\s+Substitution\s+replaced\s+by\s+(?P<player_id>[a-zA-Z-\.\'\s]+)(\]\]&gt;)*','priority':5,'name':'<player2_id> Substition replaced by <player1_id>'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+(?P<shot_type>(Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Made\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':5,'is_shot':1,'is_shot_made':1,'name':'<player_id> <shot_type>: Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+(?P<shot_type>(Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Made\s+\(\d+\s+PTS\)\s+Assist:\s+(?P<player2_id>[a-zA-Z-\.\'\s]+)\s+\(\d+\s+AST\)(\]\]&gt;)*','priority':5,'is_shot':1,'is_shot_made':1,'is_assist':1,'name':'<player_id> <shot_type>: Made Assist: <player2_id>'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Foul:\s+(Shooting|Personal|Loose Ball|Offensive|Personal Block|Personal Take|Offensive Charge|Flagrant Type \d)\s+\(\d+\s+PF\)(\]\]&gt;)*','priority':5,'is_foul':1,'name':'<player_id> Foul: <foul_type>'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Turnover\s+:\s+(Bad Pass|Traveling|Lost Ball|Foul|Step Out of Bounds Turnover|Out of Bounds Lost Ball Turnover|Poss Lost Ball Turnover)\s+\(\d+\s+TO\)(\]\]&gt;)*','priority':5,'is_turnover':1,'name':'<player_id> Turnover: <turnover_type>'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Turnover\s+:\s+(Bad Pass|Traveling|Lost Ball|Foul|Step Out of Bounds Turnover|Out of Bounds Lost Ball Turnover|Poss Lost Ball Turnover)\s+\(\d+\s+TO\)\s+Steal\s*:\s*(?P<player2_id>[a-zA-Z-\.\'\s]+)\s+\(\d+\s+ST\)(\]\]&gt;)*','priority':5,'is_turnover':1,'is_steal':1,'name':'<player_id> Turnover: <turnover_type> Steal: <player2_id>'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\s*Jump\s+Ball\s+(?P<player1_id>[a-zA-Z-\.\'\s]+)\s+vs\s+(?P<player2_id>[a-zA-Z-\.\'\s]+)\s+\((?P<player_id>[a-zA-Z-\.\'\s]+)\s+gains\s+possession\)(\]\]&gt;)*','priority':5,'name':'Jump Ball: <player1_id> <player2_id> (<player_id> gains possession)'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Violation:\s*(Defensive Goaltending|Kicked Ball)(\]\]&gt;)*','priority':5,'name':'<player_id> Violation: <violation>'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Technical(\]\]&gt;)*','priority':5, 'name':'<player_id> Technical'},


        # Three pointers
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+3pt\s+(s|S)hot:\s+Missed(\]\]&gt;)*','priority':1,'name':'<player_id> 3pt Shot: Missed','is_3pt':1,'is_3pt_made':0,'is_shot':1,'is_shot_made':0},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+3pt\s+(s|S)hot:\s+Missed\s+Block:\s*(?P<player2_id>[a-zA-Z-\.\'\s]+)\s*\(\d+\s+BLK\)(\]\]&gt;)*','priority':1,'name':'<player_id> 3pt Shot: Missed Block: <player2_id>','is_3pt':1,'is_3pt_made':0,'is_shot':1,'is_shot_made':0},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+3pt\s+(s|S)hot:\s+Made\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':1,'name':'<player_id> 3pt Shot: Made  PTS','is_3pt':1,'is_3pt_made':1,'is_shot':1,'is_shot_made':1},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+3pt\s+(s|S)hot:\s+Made\s+\(\d+\s+PTS\)\s+Assist:\s+(?P<player2_id>[a-zA-Z-\.\'\s]+)\s+\(\d+\s+AST\)(\]\]&gt;)*','priority':1,'name':'<player_id> 3pt Shot: Made  PTS Assist: <player2_id>','is_3pt':1,'is_3pt_made':1,'is_shot':1,'is_shot_made':1,'is_assist':1},

        # Free throws
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*1\s+of\s+1\s+Missed(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':0,'is_freethrow_last':1,'name':'<player_id> Free Throw 1 of 1 Missed'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*1\s+of\s+2\s+Missed(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':0,'name':'<player_id> Free Throw 1 of 2 Missed'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*2\s+of\s+2\s+Missed(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':0,'is_freethrow_last':1,'name':'<player_id> Free Throw 2 of 2 Missed'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*1\s+of\s+3\s+Missed(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':0,'name':'<player_id> Free Throw 1 of 3 Missed'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*2\s+of\s+3\s+Missed(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':0,'name':'<player_id> Free Throw 2 of 3 Missed'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*3\s+of\s+3\s+Missed(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':0,'is_freethrow_last':1,'name':'<player_id> Free Throw 3 of 3 Missed'},

        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*1\s+of\s+1\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':1,'is_freethrow_last':1,'name':'<player_id> Free Throw 1 of 1 Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*1\s+of\s+2\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':1,'name':'<player_id> Free Throw 1 of 2 Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*2\s+of\s+2\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':1,'is_freethrow_last':1,'name':'<player_id> Free Throw 2 of 2 Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*1\s+of\s+3\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':1,'name':'<player_id> Free Throw 1 of 3 Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*2\s+of\s+3\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':1,'name':'<player_id> Free Throw 2 of 3 Made'},
        {'re':'(&lt;\!\[CDATA\[)*(\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\.\'\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*3\s+of\s+3\s+\(\d+\s+PTS\)(\]\]&gt;)*','priority':1,'is_freethrow':1,'is_freethrow_made':1,'is_freethrow_last':1,'name':'<player_id> Free Throw 3 of 3 Made'},
    ]

    # Destroy old table, create new one
    dbobj.query("DROP TABLE IF EXISTS play_type_nbacom")
    dbobj.query("""
        CREATE TABLE `play_type_nbacom` (
          `id` int(11) NOT NULL,
          `re` varchar(500) DEFAULT NULL,
          `name` varchar(200) DEFAULT NULL,
          `is_rebound` tinyint(4) DEFAULT '0',
          `is_freethrow` tinyint(4) DEFAULT '0',
          `is_shot` tinyint(4) DEFAULT '0',
          `is_shot_made` tinyint(4) DEFAULT '0',
          `is_turnover` tinyint(4) DEFAULT '0',
          `is_foul` tinyint(4) DEFAULT '0',
          `is_period_startend` tinyint(4) DEFAULT '0',
          `is_team_play` tinyint(4) DEFAULT '0',
          `is_timeout` tinyint(4) DEFAULT '0',
          `is_freethrow_made` tinyint(4) DEFAULT '0',
          `priority` tinyint(4) DEFAULT '5',
          `is_3pt` tinyint(4) DEFAULT '0',
          `is_3pt_made` tinyint(4) DEFAULT '0',
          `is_freethrow_last` tinyint(4) DEFAULT '0',
          `is_block` tinyint(4) DEFAULT '0',
          `is_assist` tinyint(4) DEFAULT '0',
          `is_steal` tinyint(4) DEFAULT '0',
          PRIMARY KEY (`id`)
        ) ENGINE=MyISAM
    """)

    for idx, line in enumerate(patterns):

        line['id'] = idx
        line['re'] = line['re'].replace("\\","\\\\")
        fields = [key for key, val in sorted(line.items())]
        values = ['"%s"' % (val) for key, val in sorted(line.items())]
        
        update_values = ['%s = "%s"' % (key,val) for key, val in sorted(line.items())]
        
        sql = """
            INSERT INTO play_type_nbacom (%s)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE %s
        """ % (','.join(fields), ','.join(values), ','.join(update_values))
        dbobj.query(sql)
        



if __name__ == '__main__':
    main()
