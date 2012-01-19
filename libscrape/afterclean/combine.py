from libscrape.config import db


def combine(game_id = 342):
    shots = list(db.nba_query_dict("""
        SELECT sh.*, s.name as shot_name, s.is_freethrow 
        FROM shottest sh INNER JOIN cbsshot s ON s.id = sh.shot_type_id WHERE sh.game_id = %s
    """ % game_id))
    pbp = list(db.nba_query_dict("""
        SELECT pbp.id as 'playbyplay_id', pbp.*, p.is_shot, p.name 'play_name', p.is_freethrow, p.is_shot_made
        FROM pbp2 pbp INNER JOIN play p ON pbp.play_id = p.id 
        WHERE pbp.game_id = %s
    """ % game_id))
 
    counter = 0 
    combined = []
    for play_info in pbp:
        # Get list of shots that may qualify
        if play_info['is_shot'] == 1:

            possible_matched_shots = _identifyPossibleShotMatches(play_info, shots) 
            foundShot = len(possible_matched_shots) >= 1

            if foundShot:
                if len(possible_matched_shots) == 1:
                    matched_shot = possible_matched_shots[0]

                    # Remove shot data from pool of unmatched shots
                    del shots[matched_shot['shot_index']]

                elif len(possible_matched_shots) > 1: 
                    
                    if play_info['is_freethrow'] == 1:
                        new_possible = [line for line in possible_matched_shots if line['shot_data']['is_freethrow'] == 1]
                        # Assume the first free throw item is sufficient
                        if new_possible:
                            matched_shot = new_possible[0]
                            del shots[new_possible[0]['shot_index']]
                        else:
                            print "something went wrong here... no matched free throw found! play number %s" % play_info['play_num']
                    else:
                    
                        # Just take the first item
                        matched_shot = possible_matched_shots[0]
                        del shots[matched_shot['shot_index']]

                play_info['x'] = matched_shot['shot_data']['x']
                play_info['y'] = matched_shot['shot_data']['y']
                play_info['distance_shotchart'] = matched_shot['shot_data']['distance']
                play_info['cbs_shot_type_id'] = matched_shot['shot_data']['shot_type_id']
                play_info['shot_num_shotchart'] = matched_shot['shot_data']['shot_num']
                play_info['sec_elapsed_game_shotchart'] = matched_shot['shot_data']['sec_elapsed_game']

        del play_info['is_freethrow']
        del play_info['is_shot_made']
        del play_info['is_shot']
        del play_info['play_name']
        del play_info['id'] # already in data structure as 'playbyplay_id' within SQL query

        combined.append(play_info)
    
    return combined


def _getPotentialShotMatches():
    pass

def _identifyPossibleShotMatches(play_data, all_shot_data):

    possible_shots = []
    for shot_index, shot_data in enumerate(all_shot_data):
        isSameTeam = shot_data['team_code'] == play_data['team_code']
        isSamePlayer = shot_data['player_id'] == play_data['player_id']
        isSameShotResult = play_data['is_shot_made'] == shot_data['result']

        time_diff = (play_data['sec_elapsed_game'] - shot_data['sec_elapsed_game'])
        isWithinTimeFrame = time_diff <= 30 and time_diff >= -10

        if isSameTeam and isSamePlayer and isWithinTimeFrame and isSameShotResult:
            possible_shots.append({'shot_index':shot_index,'shot_data':shot_data})



    return possible_shots


def insert(data):
    for itm in data:
        fields = ','.join(map(str,sorted(itm.keys())))
        values = "\"" + "\",\"".join(map(str,[v for k,v in sorted(itm.items())])) + "\""
        sql = """INSERT INTO combined (%s) VALUES (%s) """  % (fields, values)
        db.nba_query(sql)


def main(game_id = 715):
    result = combine(game_id)

    all_keys = []
    for line in result:
        #all_keys.extend(line.keys())
        #print line['play_desc']
        pass

    insert(result)


def fillAllGames():
    sql = "SELECT * FROM game WHERE date_played <= '2011-02-24' and id >= 451"
    result = db.nba_query_dict(sql)

    for row in result:
        print row['id']
        main(row['id'])


if __name__ == '__main__':
    #main()
    fillAllGames()
