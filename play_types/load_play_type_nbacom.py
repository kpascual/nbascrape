
from libscrape.config import db
from libscrape.config import constants 

dbobj = db.Db(db.dbconn_nba)


def main():

    patterns = [
        'fake\s+pattern',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\s*End\s+Period(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\s*Start\s+Period(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+Team\s+Rebound(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+Team\s+Timeout\s+:\s+(Regular|Short)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\s*Timeout\s+:\s+(Official|Regular)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Rebound\s+\(Off:\d+\s+Def:\d+\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Missed(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Missed\s+Block:\s*(?P<player2_id>[a-zA-Z-\s]+)\s*\(\d+\s+BLK\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*(?P<ft_count>\d)\s+of\s+(?P<ft_total>\d)\s+Missed(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*(?P<ft_count>\d)\s+of\s+(?P<ft_total>\d)\s+\(\d+\s+PTS\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Free\s+Throw\s+(Flagrant|Technical)*\s*\(\d+\s+PTS\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player2_id>[a-zA-Z-\s]+)\s+Substitution\s+replaced\s+by\s+(?P<player_id>[a-zA-Z-\s]+)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Made\s+\(\d+\s+PTS\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\s+\d+\-\d+\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+(?P<shot_type>(3pt|Jump|Tip|Layup|Jump Hook|Turnaround Jump|Putback Dunk|Dunk|Pullup Jump|Jump Bank|Running Bank|Running Bank Hook|Hook|Turnaround Fadeaway))\s+(s|S)hot:\s+Made\s+\(\d+\s+PTS\)\s+Assist:\s+(?P<player2_id>[a-zA-Z-\s]+)\s+\(\d+\s+AST\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Foul:\s+(Shooting|Personal|Loose Ball|Offensive|Personal Block|Personal Take|Offensive Charge|Flagrant Type \d)\s+\(\d+\s+PF\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Turnover\s+:\s+(Bad Pass|Traveling|Lost Ball|Foul|Step Out of Bounds Turnover|Out of Bounds Lost Ball Turnover|Poss Lost Ball Turnover)\s+\(\d+\s+TO\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Turnover\s+:\s+(Bad Pass|Traveling|Lost Ball|Foul|Step Out of Bounds Turnover|Out of Bounds Lost Ball Turnover|Poss Lost Ball Turnover)\s+\(\d+\s+TO\)\s+Steal\s*:\s*(?P<player2_id>[a-zA-Z-\s]+)\s+\(\d+\s+ST\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\s*Jump\s+Ball\s+(?P<player1_id>[a-zA-Z-\s]+)\s+vs\s+(?P<player2_id>[a-zA-Z-\s]+)\s+\((?P<player_id>[a-zA-Z-\s]+)\s+gains\s+possession\)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Violation:\s*(Defensive Goaltending|Kicked Ball)(\]\]&gt;)*',
        '(&lt;\!\[CDATA\[)*\(\d{2}:\d{2}(\.\d)*\)\[[a-zA-Z]{2,3}\]\s+(?P<player_id>[a-zA-Z-\s]+)\s+Technical(\]\]&gt;)*',
    ]

    for idx, pattern in enumerate(patterns):

        newpattern = pattern.replace("\\","\\\\")
        sql = """UPDATE play_type_nbacom SET re = "%s" WHERE id = %s""" % (newpattern,idx)
        dbobj.query(sql)
        



if __name__ == '__main__':
    main()
