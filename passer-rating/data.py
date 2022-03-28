from bs4 import BeautifulSoup
import time
import requests
import json
import re

data_capsule = {
    'seasons': {},
    'weeks': {},
    'teams': {}
}

class Season:

    def __init__(self, year):
        self.year = year
        self.id = year

    def __str__(self):
        return f'Season in {self.year}'

    def __repr__(self):
        return f'Season in {self.year}'

class Week: 

    def __init__(self, season, week_name):
        self.season = season
        self.week_name = week_name

        self.id = f'{self.season}-{self.week_name}'

    def __str__(self):
        return f'Season in {self.year}'

    def __repr__(self):
        return f'Season in {self.year}'
    
class Player:

    def __init__(self):
        return None

class Team:

    def __init__(self):
        return None

class Team_Game:

    def __init__(self):
        return None

class Team_Season:

    def __init__(self):
        return None

class Player_Game:

    def __init__(self):
        return None

class Player_Season:

    def __init__(self):
        return None




url_template = 'https://www.pro-football-reference.com/years/{year}/games.htm'

def eval_template(template, key_val):

    for key, val in key_val.items():
        template = template.replace('{'+key+'}', str(val))

    return template

def decode_team_id_from_href(team_href):
    #Take href from team <a> element and return team id
    #   '/teams/den/2021.htm' -> 'den' for Denver Broncos

    href_split = team_href.split('/')
    #   '/teams/den/2021.htm' -> ['', 'teams', 'den', '2021.htm']

    return href_split[2]


def scrape_game_list(url_template, year):

    url = eval_template(url_template, {'year': year})
    source = requests.get(url)
    print(source)
    print(source.url)    
    soup = BeautifulSoup(source.content,'html.parser')

    loop_count = 1
    for tr in soup.select('#games tbody tr:not(.thead)'):
        cells = tr.find_all('td')
        cells_by_data_stat = {}
        for cell in cells:
            cells_by_data_stat[cell['data-stat']] = cell

        team_cells = (cells_by_data_stat['winner'], cells_by_data_stat['loser'])
        for team_cell in team_cells:
            team_anchor = team_cell.find('a')
            team_href = team_anchor['href']

        print(cells_by_data_stat)


    time.sleep(1)



for year in range(2021, 2021 + 1):
    data_capsule['seasons'][year] = Season(year)
    scrape_game_list(url_template, data_capsule)

print(data_capsule)

#scrape_game_list(mock_url_template, 2021)