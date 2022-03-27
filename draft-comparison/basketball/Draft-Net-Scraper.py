from bs4 import BeautifulSoup
import time
import requests
import json
import re

class Player:

    def __init__(self, data):

        self.data = data

        if not data['from_json']:
            year = data['year']
            tr = data['tr']
            self.rank = int(tr.select('.rank')[0].text)

            self.position = tr.select('.teamposition')[0].text
            self.team = tr.select('.team')[0].text
            self.age_class = tr.select('.class')[0].text

            self.profile_link = tr.select('a')[0]['href']

            self.first_name = tr.select('a span')[0].text
            self.last_name = tr.select('a span')[1].text
            self.image_link = tr.select('.name img')[0]['src']

            self.year = year


    def __repr__(self):
        return json.dumps(self.__dict__(), indent=2)

    def __dict__(self):
        return {
            'year': self.data['year'],
            'rank': self.data['rank'],
            'team': self.data['team'],
            'age_class': self.data['age_class'],
            'first_name': self.data['first_name'],
            'last_name': self.data['last_name'],
            'position': self.data['position'],
            'image_link': self.data['image_link'],
            'profile_link': self.data['profile_link'],
            'comparisons': self.data.get('comparisons', []),
        }

class Encoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

def scrape_big_board():
    base_big_board_url = 'https://www.nbadraft.net/ranking/bigboard/?year-ranking=$[year]'

    player_list = []

    for year in range(2008, 2022):
        print('Parsing', year)
        big_board_url  = base_big_board_url.replace('$[year]', str(year))

        source = requests.get(big_board_url)

        soup = BeautifulSoup(source.content,'html.parser')

        for tr in soup.select('.big-board-table tbody tr'):
            data = {'from_json': False, 'year': year, 'tr': tr}
            player_list.append(Player(data))

        time.sleep(10)

    return player_list


def scrape_players(player_list, player_graph):
    count = 0
    for player in player_list:
        if player.data['rank'] > 30 or len(player.data['profile_link']) == 0:
            continue

        player_name = f'{player.data["first_name"]} {player.data["last_name"]}'

        print(f'Scraping {player_name}, {player.data["profile_link"]}')
        source = requests.get(player.data['profile_link'])
        soup = BeautifulSoup(source.content,'html.parser')

        player.data['comparisons'] = []
        all_comparison_response = []
        all_comparison_response = soup(text=re.compile(r'NBA Comparison:', re.IGNORECASE))

        if len(all_comparison_response) == 0:
            all_comparison_response = soup(text=re.compile(r'NBA Comparison;', re.IGNORECASE))

        if len(all_comparison_response) == 0:
            all_comparison_response = soup(text=re.compile(r'NBA\u00A0Comparison:', re.IGNORECASE))

        if len(all_comparison_response) == 0:
            all_comparison_response = soup(text=re.compile(r'NBA Comparson:', re.IGNORECASE))

        if len(all_comparison_response) == 0:
            print(f'***** No comparisons for {player_name}, {player.data["profile_link"]}')

        for comparison_response in all_comparison_response:
            comparison = comparison_response.replace('NBA Comparison: ', '').replace('NBA comparison: ', '').strip()
            comparisons = comparison.split('/')
            player.data['comparisons'] = comparisons

        player_graph['comparisons'][player_name] = player.data['comparisons']

        #time.sleep(2)



def create_json(player_list, player_graph):
    player_list_json_string = json.dumps([player.__dict__() for player in player_list], indent=2)
    file = open("player_data.json", "w")
    file.write(player_list_json_string)

    file = open("player_graph_data.json", "w")
    file.write(json.dumps(player_graph, indent=2, cls=Encoder))




player_graph = {
    "comparisons": {

    }
}


run_big_board = False

if run_big_board:
    player_list = scrape_big_board()
else:
    player_list = []
    f = open('player_data.json', 'r')
    player_json = json.loads(f.read())

    for player_data in player_json:
        player_data['from_json'] = True

        player_list.append(Player(player_data))

scrape_players(player_list, player_graph)
create_json(player_list, player_graph)

print(player_graph)
