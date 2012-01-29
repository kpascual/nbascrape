from libscrape.config import db
import json
import datetime

import libscrape.config.constants

LOGDIR_AFTERCLEAN = libscrape.config.constants.LOGDIR_AFTERCLEAN

class Combine:
    def __init__(self, gamedata):
        self.gamedata = gamedata
        self.filename = self.gamedata['abbrev'] + '_combined'
        self.game_id = self.gamedata['id']


    def appendCbsSportsShotsToEspnPlayByPlay(self):
        shots_cbssports = self._getCbsSportsShots()
        playbyplay_espn = self._getEspnPlayByPlay()
        
        combined = self._appendShots(shots_cbssports, playbyplay_espn)
        self._writeToFile(LOGDIR_AFTERCLEAN + self.filename + '_cbssports', combined)
        

    def appendEspnShotsToEspnPlayByPlay(self):
        shots_espn = self._getEspnShots()
        playbyplay_espn = self._getEspnPlayByPlay()

        combined = self._appendShots(shots_espn, playbyplay_espn)
        self._writeToFile(LOGDIR_AFTERCLEAN + self.filename + '_espn', combined)
        

    def appendNbaComShotsToEspnPlayByPlay(self):
        shots_nbacom = self._getNbaComShots()
        playbyplay_espn = self._getEspnPlayByPlay()

        combined = self._appendShots(shots_nbacom, playbyplay_espn)
        self._writeToFile(LOGDIR_AFTERCLEAN + self.filename + '_nbacom', combined)


    def _appendShots(self, shots, playbyplay):
    
        suggested_matches = []
        combined = []
        for play_info in playbyplay:

            # Get list of shots that may qualify
            if play_info['is_shot'] == 1:

                possible_matched_shots = self._findShotMatches(play_info, shots) 

                foundShot = len(possible_matched_shots) >= 1
                play_info['shot_matches'] = []
                if foundShot:
                    # Log which shots got matched to which plays
                    play_info['shot_matches'] = possible_matched_shots                    
                    suggested_matches.append(play_info)

                    match = self._chooseBestMatch(possible_matched_shots, shots, play_info)
                    shots = match['shots']
                    play_info['best_shot_match'] = match['matched_shot'] 

                    """
                    play_info['x'] = match['matched_shot']['shot_data']['x']
                    play_info['y'] = match['matched_shot']['shot_data']['y']
                    #play_info['distance_shotchart'] = match['matched_shot']['shot_data']['distance']
                    #play_info['cbs_shot_type_id'] = match['matched_shot']['shot_data']['shot_type_id']
                    #play_info['shot_num_shotchart'] = match['matched_shot']['shot_data']['shot_num']
                    play_info['sec_elapsed_game_shotchart'] = match['matched_shot']['shot_data']['deciseconds_left']
                    """

            del play_info['is_freethrow']
            #del play_info['is_shot_made']
            #del play_info['is_shot']
            del play_info['play_name']
            del play_info['id'] # already in data structure as 'playbyplay_id' within SQL query

            combined.append(play_info)
       
        # Temporary -- log the suggested play-shot matches
        self._dumpSuggestedMatches(suggested_matches)
     
        return combined


    def _chooseBestMatch(self, matched_shots, shots, play):
        if len(matched_shots) == 1:
            matched_shot = matched_shots[0]

            # Remove shot data from pool of unmatched shots
            del shots[matched_shot['shot_index']]

        elif len(matched_shots) > 1: 
            matched_shot = matched_shots[0]
            # Create a new routine to determine best match                        
            if 'is_freethrow' in play.keys() and play['is_freethrow'] == 1:
                    new_possible = []
                    try:
                        new_possible = [line for line in matched_shots if line['shot_data']['is_freethrow'] == 1]
                        # Assume the first free throw item is sufficient
                        matched_shot = new_possible[0]
                        del shots[new_possible[0]['shot_index']]
                    except:
                        print "something went wrong here... no matched free throw found! play number %s" % play['play_num']
            else:
            
                # Just take the first item
                matched_shot = matched_shots[0]
                del shots[matched_shot['shot_index']]

        return {'matched_shot': matched_shot, 'shots': shots}

    def matchEspnPlayByPlayToNbaComShotChart(self):
        pass

    
    def matchEspnPlayByPlayToEspnShotChart(self):
        pass


    def _dumpSuggestedMatches(self, data):
        f = open('suggested_matches.txt','w')
        shot_json = json.dumps(data, indent=2, sort_keys=True)
        f.write(shot_json)


    def _getPotentialShotMatches(self):
        pass

    def _findShotMatches(self, play_data, shot_data):

        possible_shots = []
        for shot_index, shot_data in enumerate(shot_data):
            isSameTeam = play_data['team_id'] == shot_data['team_id']
            isSamePlayer = play_data['player_id'] == shot_data['player_id'] 
            isSameShotResult = play_data['is_shot_made'] == shot_data['is_shot_made']

            time_diff = (play_data['sec_elapsed_game'] - shot_data['deciseconds_left'])
            isWithinTimeFrame = time_diff <= 300 and time_diff >= -100 and play_data['period'] == shot_data['period']

            if isSameTeam and isSamePlayer and isWithinTimeFrame and isSameShotResult:
                possible_shots.append({'shot_index':shot_index,'shot_data':shot_data})

        return possible_shots


    def _getCbsSportsShots(self):
        return list(db.nba_query_dict("""
            SELECT sh.*, s.name as shot_name, s.is_freethrow 
            FROM nba_staging.shotchart_cbssports sh INNER JOIN shot_cbs s ON s.id = sh.shot_type_id WHERE sh.game_id = %s
        """ % self.game_id))


    def _getNbaComShots(self):
        return list(db.nba_query_dict("""
            SELECT s.*
            FROM nba_staging.shotchart_nbacom s
            WHERE s.game_id = %s
        """ % self.game_id))


    def _getEspnShots(self):
        return list(db.nba_query_dict("""
            SELECT s.*
            FROM nba_staging.shotchart_espn s
            WHERE s.game_id = %s
        """ % self.game_id))


    def _getEspnPlayByPlay(self):
        return list(db.nba_query_dict("""
            SELECT pbp.id as 'playbyplay_id', pbp.*, 
                p.is_shot, p.name 'play_name', p.is_freethrow, p.is_shot_made
            FROM nba_staging.playbyplay_espn pbp 
                INNER JOIN play_espn p ON pbp.play_id = p.id 
            WHERE pbp.game_id = %s
        """ % self.game_id))


    def _writeToFile(self, filename, data):
        f = open(filename,'w')
        shot_json = json.dumps(data, indent=2, sort_keys=True)
        f.write(shot_json)

        
    def insert(self, data):
        for itm in data:
            fields = ','.join(map(str,sorted(itm.keys())))
            values = "\"" + "\",\"".join(map(str,[v for k,v in sorted(itm.items())])) + "\""
            sql = """INSERT INTO combined (%s) VALUES (%s) """  % (fields, values)
            db.nba_query(sql)


def main(game_id = 1499):
    gamedata = db.nba_query_dict("SELECT * FROM game WHERE id = %s" % (game_id))[0]
    obj = Combine(gamedata)

    obj.appendCbsSportsShotsToEspnPlayByPlay()
    obj.appendEspnShotsToEspnPlayByPlay()
    obj.appendNbaComShotsToEspnPlayByPlay()



def catchup():
    last = datetime.date(2012,1,24)
    first = datetime.date(2011,12,25)
    
    while first < last:
        
        games = db.nba_query_dict("SELECT * FROM game WHERE date_played = '%s'" % (first)) 
        for gamedata in games:
            print gamedata['abbrev']
            obj = Combine(gamedata)

            obj.appendCbsSportsShotsToEspnPlayByPlay()
            obj.appendEspnShotsToEspnPlayByPlay()
            obj.appendNbaComShotsToEspnPlayByPlay()

        first = first + datetime.timedelta(days=1)



if __name__ == '__main__':
    catchup()
    #fillAllGames()
