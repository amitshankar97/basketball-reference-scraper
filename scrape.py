import threading
from db import DB
BASE_URL = 'https://www.basketball-reference.com'
import requests
from bs4 import BeautifulSoup
import re

class Scraper (threading.Thread):
    def __init__(self, threadID, letter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.letter = letter
    
    def get_table(self, webpage, category):

        # div for category
        if category == 'totals':
            stats_div = webpage.find('div', id=("div_totals_clone"))
        else:
            stats_div = webpage.find('div', id=("all_" + category))
        
        # stats = stats_div.find_all('tr') # get all rows for category
        stats = stats_div.find_all('tr', id=re.compile(category)) # get all rows for category

        seasons = []

        for statRow in stats:
            season = {}
            season['season'] = statRow.find('th', {"data-stat" : "season"}).text

            stats = statRow.find_all('td')
            for stat in stats:
                statName = stat.attrs['data-stat']
                not_integers = ['team_id', 'lg_id', 'pos']

                if statName in not_integers or stat.text == '':
                    statValue = stat.text
                else:
                    statValue = float(stat.text)

                season[statName] = statValue

            seasons.append(season)

        return seasons


    def get_html(self, url):
        page = requests.get(url)
        html = BeautifulSoup(page.text, 'lxml')
        return html

    # Scrape players by letter
    def run(self):
        link = BASE_URL + '/players/' + self.letter
        html = self.get_html(link)

        if html:
            playersDiv = html.find('div', id='all_players')

            if(playersDiv == None):
                return []

            links = playersDiv.find_all('a')

            players = []

            for link in links:
                player = {}
                playerLink = link.get('href')

                if not playerLink.startswith('/players'):
                    continue

                player['name'] = link.text
                player['url'] = BASE_URL + playerLink
                webpage = self.get_html(player['url'])

                player['per_game'] = self.get_table(webpage, 'per_game')
                # player['totals'] = get_table(webpage, 'totals')
                # player['playoffs_per_game'] = get_table(webpage, 'playoffs_per_game')

                mongo = DB()
                success = mongo.addOrUpdatePlayer(player=player)
            
            # return players
            print(self.threadID + " exited.")