import re
import datetime
import sys
from BeautifulSoup import BeautifulSoup
from libscrape.config import constants
import time
import logging

logger = logging.getLogger("extract")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("extract_espn_pbp.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(module)s - Line %(lineno)d - %(message)s"))
logger.addHandler(fh)

LOGDIR_EXTRACT = '../../logs/extract/'

class Extract():

    def __init__(self, str_html, game_name):
        self.html = str_html
        self.game_name = game_name
        self.soup = BeautifulSoup(self.html)
        self.table = self.soup.find(attrs={'class':'mod-data'})
        self.numberedrows = [(i,row) for i,row in enumerate(self.table.findAll('tr'))]
        self.rows = [row for i, row in self.numberedrows]
        self.quarters = self.getPeriodIndexes()
        (self.home_team, self.away_team) = self.getTeamNames()


    def extractAll(self):
        timeouts = self.getTimeouts()
        plays = self.getPlayData() 
        periods = dict(self.getPeriodRanges())
        allplays = sorted(timeouts + plays)

        plays_with_quarters = []
        for line in allplays:
            try:
                plays_with_quarters.append([periods[line[0]]] + list(line))
            except:
                plays_with_quarters.append(["check quarter"] + list(line))
                logger.warn("%s: quarter not identified: %s" % (self.game_name, line[0]))


        return plays_with_quarters 
        #for line in plays:
        #    print ','.join([str(field) for field in line])

    def examineRowLengths(self):
        lengths = [len(row.findAll('td')) for row in self.rows]
        return list(set([(a, lengths.count(a)) for a in lengths]))


    def getTeamNames(self):
        home = [row.findAll('th')[3].renderContents() for i, row in self.numberedrows if len(row.findAll('td')) == 0]
        away = [row.findAll('th')[1].renderContents() for i, row in self.numberedrows if len(row.findAll('td')) == 0]

        logging.warn("Multiple away team names found") if len(set(away)) > 1 else None 
        logging.warn("Multiple home team names found") if len(set(home)) > 1 else None

        return (list(set(away))[0], list(set(home))[0])


    def examineZeroCells(self):
        cells = [[i] + [t.renderContents() for t in row.findAll('th')] for i, row in self.numberedrows if len(row.findAll('td')) == 0]
        return cells


    def examineOneCell(self):
        cells = [t.renderContents() for i, row in self.numberedrows for t in row.findAll('td') if len(row.findAll('td')) == 1]
        return list(set([(a, cells.count(a)) for a in cells]))


    def getPeriodIndexes(self):
        cells = [[i] + map(lambda x: x.renderContents(),row.findAll('td')) for i,row in self.numberedrows if len(row.findAll('td')) == 2]
        periods = [line for line in cells if 'Start of the' in line[2] or 'End of the' in line[2] or 'End Game' in line[1]]
        #unknown = [line for line in cells if line not in timeouts and line not in periods]

        dict_periods = {}
        for (i, cell1, cell2) in periods:
            match = re.search('(Start|End)\s+of\s+the\s+(?P<quarter>[0-9])(st|nd|rd|th)\s+(?P<period>(Quarter|Overtime))',cell2)
            if match:
                period_name = '%s %s' % (match.group('quarter'), match.group('period'))
                if period_name not in dict_periods.keys():
                    dict_periods[period_name] = [i]
                else:
                    dict_periods[period_name].append(i)
      
        return dict_periods 


    def getPeriodRanges(self):
        quarter_index = [(index,key) for key,(mini,maxi) in self.quarters.items() for index in range(mini,maxi+1)]
        print self.quarters
 
        return quarter_index
        
    
    def getTimeouts(self):
        cells = [[i] + map(lambda x: x.renderContents(),row.findAll('td')) for i,row in self.numberedrows if len(row.findAll('td')) == 2]
        timeouts = [line for line in cells if 'timeout' in line[2]]
        
        cleaned_timeouts = []
        for (counter, time_left, action) in timeouts:
            if self.home_team.lower() in action.lower():
                cleaned_timeouts.append((counter, time_left,'','','',action.replace(self.home_team.capitalize(),'')))
       
            if self.away_team.lower() in action.lower():
                cleaned_timeouts.append((counter, time_left,'','',action.replace(self.away_team.capitalize(),''),''))

     
        logging.info("No timeouts found") if len(timeouts) == 0 else None 

        return cleaned_timeouts


    def getPlayData(self):
        rows = [[i] + [t.renderContents() for t in row.findAll('td')] for i, row in self.numberedrows if len(row.findAll('td')) == 4]
        logging.error("No play by play data found") if len(rows) == 0 else None 

        newrows = []        
        for (index, time_left, away, score, home) in rows:
            # Split into away-home score
            (away_score, home_score) = score.split('-')
            newrows.append((index, time_left, away_score, home_score, away, home))

        return newrows
 
