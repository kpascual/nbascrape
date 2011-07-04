from libscrape.config import constants
from BeautifulSoup import BeautifulSoup
import csv
import re


LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

class Extract():

    def __init__(self, html, filename, game_name, away_team, home_team):
        self.html = html
        self.game_name = game_name
        self.filename = filename
        self.soup = BeautifulSoup(self.html)
        
        obj = self.soup.find(attrs={'id':'nbaGIPBP'})
        self.table = obj.find('table') 
        self.rows = self.table.findAll('tr')
        self.numberedrows = [(i,row) for i,row in enumerate(self.table.findAll('tr'))]

        self.home_team = home_team
        self.away_team = away_team

    
    def extract(self):
        plays = self.splitRowsIntoPlays()
        row_indexes = self.getPeriodIndexes()
        indexed_plays = self.combinePlaysWithPeriodIndexes(row_indexes, plays)
        self.dumpToFile(indexed_plays)

    
    def splitRowsIntoPlays(self):
        plays = []
        for i,r in self.numberedrows:
            cells = r.findAll('td')
            if len(cells) == 1:
                #print cells[0] 
                try:
                    if cells[0]['id'] == 'nbaGIPbPJBall':
                        jumpball = cells[0].find(attrs={'class':'gameEvent'}).renderContents()
                        match = re.search("\((?P<time_left>[0-9:]+)\)\s+(?P<jumpball>.*)",jumpball)

                        time_left = ''
                        play_description = ''
                        if match: 
                            match_dict = match.groupdict()
                            time_left = match_dict['time_left']
                            play_description = match_dict['jumpball']

                        plays.append([i, time_left,'','', play_description, ''])
                except:
                    pass
            elif len(cells) == 3:
                away, scoretime, home = [td.renderContents() for td in cells]
                time_left = scoretime.replace('\n','')
                home_score = ''
                score = ''
                away_score = ''
                if "<br />" in scoretime:
                    time_left, score = scoretime.replace('\n','').split("<br />")
            
                    match = re.search("\[(?P<team_code>[A-Z]+)\s+(?P<score1>\d+)\-(?P<score2>\d+)\]\s+", score)
                    if match:
                        if away == '&nbsp;':
                            home_score = match.groupdict()['score1']
                            away_score = match.groupdict()['score2']
                        else:
                            home_score = match.groupdict()['score2']
                            away_score = match.groupdict()['score1']

                plays.append([i, time_left, away_score, home_score, away, home])
            elif len(cells) == 2:
                pass


        return plays


    def getPeriodIndexes(self):
        periods = []
        for i,r in self.numberedrows:
            cells = r.findAll('td')

            if len(cells) == 1:
                try:
                    has_id = cells[0]['id']
                except:
                    match = re.search('.*(?P<startorend>(Start|End))\s+of\s+(?P<num>\d)(st|nd|rd|th)\s+(?P<period_type>(Quarter|Overtime)).*',cells[0].renderContents())
                    if match:
                        matches = match.groupdict()
                        periods.append((i, matches['startorend'], '%s %s' % (matches['num'], matches['period_type'])))

        # Now throw into a dictionary
        dict_periods = {}
        for line in periods:
            if line[2] not in dict_periods.keys():
                dict_periods[line[2]] = [line[:2]]
            else:
                dict_periods[line[2]].append(line[:2])

        # Order the periods
        ordered_periods = [[period_number+1] + [idx[0] for idx in dict_periods[period_name]] for period_number,period_name in enumerate(constants.PERIODS) if period_name in dict_periods.keys()]
        
        # Check if last item in list has a start index, but no end index
        if len(ordered_periods[-1]) == 2:
            ordered_periods[-1].append(5000)

        return ordered_periods


    def combinePlaysWithPeriodIndexes(self, ordered_periods, plays):

        indexed_plays = []
        for line in plays:
            chosen_period = ''
            for period, start_index, end_index in ordered_periods:
                if line[0] >= start_index and line[0] <= end_index:
                    chosen_period = period
                    indexed_plays.append([chosen_period] + line)
                    break
    
            if not chosen_period: indexed_plays.append([0] + line)

        #print indexed_plays        
        return indexed_plays 


    def dumpToFile(self, list_data):
        writer = csv.writer(open(LOGDIR_EXTRACT + self.filename + '_pbp_nbacom','wb'),delimiter=',',lineterminator='\n')
        writer.writerows(list_data)


if __name__ == '__main__':
    f = '2010-10-26_MIA@BOS_pbp_nbacom'
    #f = '2011-02-26_UTA@DET_pbp_nbacom'
    obj = Extract(open('../../logs/source/' + f,'r').read(),f, f.replace('pbp_nbacom',''),'MIA','BOS')
    #obj.printRows()
    print obj.extract()




