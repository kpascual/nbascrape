from libscrape.config import constants

from BeautifulSoup import BeautifulSoup
import csv
import re
import logging


LOGDIR_EXTRACT = constants.LOGDIR_EXTRACT

class Extract:

    def __init__(self, html, filename, gamedata):
        self.html = html
        self.gamedata = gamedata
        self.game_name = self.gamedata['abbrev']
        self.filename = filename

        self.home_team_city = self.gamedata['home_team_city']
        self.away_team_city = self.gamedata['away_team_city']


    def extractAndDump(self):
        plays = self.extractAll()
        self.dumpToFile(plays)
        logging.info("EXTRACT - playbyplay_espn - game_id: %s - plays extracted: %s" % (self.gamedata['id'], len(plays)))


    def extractAll(self):
        data = self._getData()

        timeouts = self._getTimeouts(data)
        plays = self._getPlayData(data) 
        periods = self._getPeriodRanges(data)
        allplays = sorted(timeouts + plays)

        plays_with_quarters = []
        for line in allplays:
            try:
                plays_with_quarters.append([periods[line[0]]] + list(line))
            except:
                plays_with_quarters.append(["check quarter"] + list(line))

        return plays_with_quarters 


    def _getData(self):
        self.soup = BeautifulSoup(self.html)
        
        table = self.soup.find(attrs={'class':'mod-data'})
        if table:
            rows = table.findAll('tr')
            if rows:
                numberedrows = [(i,row) for i,row in enumerate(table.findAll('tr'))]
                return numberedrows

        return []


    def _getPeriodIndexes(self, rows):
        period_data = [[play_number] + map(lambda tablecell: tablecell.renderContents(),row.findAll('td')) for play_number, row in rows if len(row.findAll('td')) == 2]
        periods = [line for line in period_data if 'Start of the' in line[2] or 'End of the' in line[2] or 'End Game' in line[1]]

        # Get the start and ending play numbers for each period in the game
        # Ex. for the 1st quarter, get the play indexes 2 and 140
        period_startend = {}
        for (play_number, cell1, cell2) in periods:
            match = re.search('((?P<startorend>(Start|End)))\s+of\s+the\s+(?P<quarter>[0-9])(st|nd|rd|th)\s+(?P<period>(Quarter|Overtime))',cell2)
            if match:
                period_name = '%s %s' % (match.group('quarter'), match.group('period'))
                #period_number = constants.PERIODS.index(period_name)
                period_number = constants.PERIODS[period_name]

                # This variable will be either 'start' or 'end'
                startorend = match.group('startorend').lower()
                if period_number not in period_startend.keys():
                    period_startend[period_number] = {startorend: play_number}
                else:
                    period_startend[period_number][startorend] = play_number
     
        cleaned = self.cleanMissingPeriodRanges(period_startend, rows)
        return cleaned


    def cleanMissingPeriodRanges(self, periods, rows):
        backup_periods = self._makeBackupPeriodRanges(rows)

        cleaned_periods = {}
        for period_number, vals in periods.items():
            cleaned = {'start': 0, 'end': 0}
            if 'start' not in vals.keys(): 
                cleaned['start'] = backup_periods[period_number]['start']
            if 'end' not in vals.keys():
                cleaned['end'] = backup_periods[period_number]['end']

            cleaned.update(vals)
            cleaned_periods[period_number] = cleaned
            del cleaned

        return cleaned_periods


    def _getPeriodRanges(self, rows):

        periods = self._getPeriodIndexes(rows)
        newdata = []
        for key, vals in periods.items():
            for play_index in range(vals['start'], vals['end'] + 1):
                newdata.append((play_index, key))
 
        return dict(newdata)

        
    def _makeBackupPeriodRanges(self, rows):
        periods = []
        dict_periods = {}

        rows = [(play_number, t.renderContents()) for play_number, row in rows for t in row.findAll('td') if len(row.findAll('td')) == 1]
        for play_number,row in rows:
            match = re.search('.*(?P<num>\d)(st|nd|rd|th)\s+(?P<period_type>(Quarter|Overtime))\s+Summary.*',row)
            if match:
                period_name = "%s %s" % (match.group('num'), match.group('period_type'))
                #period_number = constants.PERIODS.index(period_name)
                period_number = constants.PERIODS[period_name]
                periods.append((period_number, play_number, period_name))

        for period_number, play_number, period_name in sorted(periods):

            dict_periods[period_number] = {'start': play_number}
            try:
                dict_periods[period_number]['end'] = [itm[1] for itm in sorted(periods) if itm[0] == period_number + 1][0] - 1
            except:
                dict_periods[period_number]['end'] = play_number + 300

        return dict_periods

 
    def _getTimeouts(self, rows):
        cells = [[i] + map(lambda x: x.renderContents(),row.findAll('td')) for i,row in rows if len(row.findAll('td')) == 2]
        timeouts = [line for line in cells if 'timeout' in line[2]]
        
        cleaned_timeouts = []
        for (counter, time_left, action) in timeouts:
            if self.home_team_city.lower() in action.lower():
                cleaned_timeouts.append((counter, time_left,'','','',action.replace(self.home_team_city.capitalize(),'')))
       
            elif self.away_team_city.lower() in action.lower():
                cleaned_timeouts.append((counter, time_left,'','',action.replace(self.away_team_city.capitalize(),''),''))
            else:
                cleaned_timeouts.append((counter, time_left,'','',action,''))


        return cleaned_timeouts


    def _getPlayData(self, rows):
        rows = [[play_number] + [t.renderContents() for t in row.findAll('td')] for play_number, row in rows if len(row.findAll('td')) == 4]

        newrows = []        
        for (index, time_left, away, score, home) in rows:

            # Split into away-home score
            away_score, home_score = score.split('-')

            newrows.append((index, time_left, away_score, home_score, away, home))

        return newrows


    def dumpToFile(self, list_data):
        writer = csv.writer(open(LOGDIR_EXTRACT + self.filename,'wb'),delimiter=',',lineterminator='\n')
        writer.writerows(list_data)

