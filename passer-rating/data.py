from bs4 import BeautifulSoup
import time
import requests
import json
import re

data_capsule = {
    'seasons': {},
    'weeks': {},
    'teams': {},
    'games': {}
}

class Season:

    def __init__(self, year):
        self.year = year

        self.id = year

        self.weeks = {}

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
        return f'Season in {self.season.year}'

    def __repr__(self):
        return f'Season in {self.season.year}'
    
class Player:

    def __init__(self):
        return None

class Team:

    def __init__(self, team_id, team_name):
        self.team_id = team_id
        self.team_name = team_name

        self.id = team_id

    def __str__(self):
        return f'Team {self.team_name} with id {self.id}'

    def __repr__(self):
        return f'Team {self.team_name} with id {self.id}'

class Game:

    def __init__(self, game_id, game_href, teams, week):
        self.game_id = game_id
        self.game_href = game_href
        self.teams = teams
        self.week = week

        self.id = game_id

    def __str__(self):
        return f'Game between {self.teams} with id {self.id}'

    def __repr__(self):
        return f'Game between {self.teams} with id {self.id}'

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




season_url_template = 'https://www.pro-football-reference.com/years/{year}/games.htm'
game_url_template = 'https://www.pro-football-reference.com/{game_href}'

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

def decode_game_id_from_href(game_href):
    #Take href from game <a> element and return game id
    #   '/boxscores/202201170ram.htm' -> '202201170ram' for game between Rams and Cardinals on 2022-01-17

    game_href = game_href.replace('.', '/')
    href_split = game_href.split('/')
    #   '/boxscores/202201170ram.htm' -> ['', 'boxscores', '202201170ram', 'htm']

    return href_split[2]


def scrape_season_page(season_url_template, data_capsule, season):

    url = eval_template(template = season_url_template, key_val = {'year': season.year})
    source = requests.get(url)
    soup = BeautifulSoup(source.content,'html.parser')

    for tr in soup.select('#games tbody tr:not(.thead)'):
        print('class', tr.get('class'))
        cells = tr.find_all('td')
        cells += tr.find_all('th')
        print(cells)
        cells_by_data_stat = {}
        for cell in cells:
            cells_by_data_stat[cell['data-stat']] = cell

        if cells_by_data_stat['game_date'].find('strong') and cells_by_data_stat['game_date'].find('strong').text == 'Playoffs':
            #This is to catch an empty row in the table for playoffs, so skip
            continue

        print('cells_by_data_stat', cells_by_data_stat)
        week_cell = cells_by_data_stat['week_num']
        week_name = week_cell.text
        if week_name not in season.weeks:
            week = Week(season, week_name)
            season.weeks[week.id] = week
            data_capsule['weeks'][week.id] = week

        team_cells = (cells_by_data_stat['winner'], cells_by_data_stat['loser'])
        teams = []
        for team_cell in team_cells:
            team_anchor = team_cell.find('a')
            team_href = team_anchor['href']
            team_id = decode_team_id_from_href(team_href = team_href)
            print('team_id', team_id)

            if team_id not in data_capsule['teams']:
                print('team_id not in data_capsule')
                team = Team(team_id = team_id, team_name = team_anchor.text)
                data_capsule['teams'][team_id] = team
            else:
                team = data_capsule['teams'][team_id]

            teams.append(team)
        
        game_cell = cells_by_data_stat['boxscore_word']
        game_anchor = game_cell.find('a')
        game_href = game_anchor['href']
        game_id = decode_game_id_from_href(game_href)
        game = Game(game_id = game_id, game_href = game_href, teams = teams, week = week)
        data_capsule['games'][game_id] = game

        #print(cells_by_data_stat)


def scrape_game_page(game, data_capsule):
    url = eval_template(template = game_url_template, key_val = {'game_href': game.game_href})
    source = requests.get(url)
    soup = BeautifulSoup(source.content,'html.parser')

    stat_table_ids = ['player_offense']
    for stat_table_id in stat_table_ids:

        for tr in soup.select(f'#{stat_table_id} tbody tr:not(.thead)'):
            cells = tr.find_all('td')
            cells += tr.find_all('th')
            cells_by_data_stat = {}
            for cell in cells:
                cells_by_data_stat[cell['data-stat']] = cell.text

            

            print(cells_by_data_stat)


for year in range(2021, 2021 + 1):
    season = Season(year = year)
    data_capsule['seasons'][year] = season
    scrape_season_page(season_url_template = season_url_template, data_capsule = data_capsule, season = season)

for game_id, game in data_capsule['games'].items():
    scrape_game_page(game, data_capsule)

    time.sleep(.5)

print(data_capsule)

#scrape_game_list(mock_url_template, 2021)