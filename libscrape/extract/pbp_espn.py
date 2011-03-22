from libscrape.config import constants

from BeautifulSoup import BeautifulSoup
import logging
import logging.config
import csv
import re

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("extract")

LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

class Extract:

    def __init__(self, html, filename, game_name, away_team, home_team):
        self.html = html
        self.game_name = game_name
        self.filename = filename
        self.soup = BeautifulSoup(self.html)
        
        self.table = self.soup.find(attrs={'class':'mod-data'})
        self.numberedrows = [(i,row) for i,row in enumerate(self.table.findAll('tr'))]
        self.rows = [row for i, row in self.numberedrows]

        self.backup_periods = self.makeBackupPeriodRanges()
        self.periods = self.getPeriodIndexes()

        self.home_team = home_team
        self.away_team = away_team

    def extractAndDump(self):
        plays = self.extractAll()
        self.dumpToFile(plays)


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


    def getTeamNames(self):
        home = [row.findAll('th')[3].renderContents() for i, row in self.numberedrows if len(row.findAll('td')) == 0]
        away = [row.findAll('th')[1].renderContents() for i, row in self.numberedrows if len(row.findAll('td')) == 0]

        if len(set(away)) > 1:
            logger.warn("Multiple away team names found") 
        if len(set(home)) > 1:
            logger.warn("Multiple home team names found") 

        return (list(set(away))[0], list(set(home))[0])


    def getPeriodIndexes(self):
        cells = [[i] + map(lambda x: x.renderContents(),row.findAll('td')) for i,row in self.numberedrows if len(row.findAll('td')) == 2]
        periods = [line for line in cells if 'Start of the' in line[2] or 'End of the' in line[2] or 'End Game' in line[1]]

        dict_periods = {}
        for (i, cell1, cell2) in periods:
            match = re.search('((?P<startorend>(Start|End)))\s+of\s+the\s+(?P<quarter>[0-9])(st|nd|rd|th)\s+(?P<period>(Quarter|Overtime))',cell2)
            if match:
                period_name = '%s %s' % (match.group('quarter'), match.group('period'))
                if period_name not in dict_periods.keys():
                    dict_periods[period_name] = {match.group('startorend').lower():i}
                else:
                    dict_periods[period_name][match.group('startorend').lower()] = i
     
        cleaned = self.cleanMissingPeriodRanges(dict_periods)
        return cleaned


    def cleanMissingPeriodRanges(self, periods):
        cleaned_periods = {}
        for period, vals in periods.items():
            cleaned = {'start': 0, 'end': 0}
            if 'start' not in vals.keys(): 
                logger.warn("%s - Could not find quarter start index -- using backup" % self.game_name)
                cleaned['start'] = self.backup_periods[period]['start']
            if 'end' not in vals.keys():
                logger.warn("%s - Could not find quarter end index -- using backup" % self.game_name)
                cleaned['end'] = self.backup_periods[period]['end']

            cleaned.update(vals)
            cleaned_periods[period] = cleaned
            del cleaned

        return cleaned_periods


    def getPeriodRanges(self):
        period_index = [sorted((index,key)) for key,vals in self.periods.items() for index in range(vals['start'],vals['end']+1)]
 
        return period_index

        
    def makeBackupPeriodRanges(self):
        periods = []
        dict_periods = {}

        rows = [(i, t.renderContents()) for i, row in self.numberedrows for t in row.findAll('td') if len(row.findAll('td')) == 1]
        for i,row in rows:
            match = re.search('.*(?P<num>\d)(st|nd|rd|th)\s+(?P<period_type>(Quarter|Overtime))\s+Summary.*',row)
            if match:
                period_name = "%s %s" % (match.group('num'), match.group('period_type'))
                period_id = constants.PERIODS.index(period_name)
                periods.append((period_id, i, period_name))

        for (period_id, idx, period_name) in sorted(periods):
            dict_periods[period_name] = {'start':idx}
            try:
                dict_periods[period_name]['end'] = [itm[1] for itm in sorted(periods) if itm[0] == period_id + 1][0] - 1
            except:
                dict_periods[period_name]['end'] = idx + 300

        return dict_periods

 
    def getTimeouts(self):
        cells = [[i] + map(lambda x: x.renderContents(),row.findAll('td')) for i,row in self.numberedrows if len(row.findAll('td')) == 2]
        timeouts = [line for line in cells if 'timeout' in line[2]]
        
        cleaned_timeouts = []
        for (counter, time_left, action) in timeouts:
            if self.home_team.lower() in action.lower():
                cleaned_timeouts.append((counter, time_left,'','','',action.replace(self.home_team.capitalize(),'')))
       
            if self.away_team.lower() in action.lower():
                cleaned_timeouts.append((counter, time_left,'','',action.replace(self.away_team.capitalize(),''),''))

        if len(timeouts) == 0: 
            logger.info("No timeouts found") 

        return cleaned_timeouts


    def getPlayData(self):
        rows = [[i] + [t.renderContents() for t in row.findAll('td')] for i, row in self.numberedrows if len(row.findAll('td')) == 4]
        if len(rows) == 0:
            logger.error("No play by play data found") 

        newrows = []        
        for (index, time_left, away, score, home) in rows:
            # Split into away-home score
            (away_score, home_score) = score.split('-')
            newrows.append((index, time_left, away_score, home_score, away, home))

        return newrows


    def examineRowLengths(self):
        lengths = [len(row.findAll('td')) for row in self.rows]
        return list(set([(a, lengths.count(a)) for a in lengths]))


    def dumpToFile(self, list_data):
        writer = csv.writer(open(LOGDIR_EXTRACT + self.filename,'wb'),delimiter=',',lineterminator='\n')
        writer.writerows(list_data)

        """
        f = open(LOGDIR_EXTRACT + self.filename,'w')
        writer.writerow([str(itm) for itm in list_data])
        """

""" 
    def examineRowLengths(self):
        lengths = [len(row.findAll('td')) for row in self.rows]
        return list(set([(a, lengths.count(a)) for a in lengths]))
    
    def examineOneCell(self):
        cells = [t.renderContents() for i, row in self.numberedrows for t in row.findAll('td') if len(row.findAll('td')) == 1]
        return list(set([(a, cells.count(a)) for a in cells]))

    def examineZeroCells(self):
        cells = [[i] + [t.renderContents() for t in row.findAll('th')] for i, row in self.numberedrows if len(row.findAll('td')) == 0]
        return cells

    def makeBackupPeriodRanges(self, period, vals, all_data):
        PERIODS = constants.PERIODS
        newvals = {}

        if 'start' not in vals.keys():
            prior_period = PERIODS.index(period) - 1
            if prior_period >= 0:
                try:
                    newvals['start'] = all_data[PERIODS[prior_period]]['end'] + 1
                except:
                    newvals['start'] = 0
            else:
                newvals['start'] = 0
        else:
            newvals['start'] = vals['start']
  
        if 'end' not in vals.keys():
            next_period = PERIODS.index(period) + 1
            newvals['end'] = max([field for key,idx in all_data for field in ids.values()])
        else:
            newvals['end'] = vals['end']

        return newvals
"""
