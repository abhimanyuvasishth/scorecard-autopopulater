import csv
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

from constants import in_date_fmt, out_date_fmt, Teams

class Squad:

    def __init__(self):
        self.series_id = '1249214'
        self.base_url = 'https://www.espncricinfo.com'
        self.full_url = f'{self.base_url}/ci/content/squad/index.html?object={self.series_id}'
        self.soup = self.get_soup()
        self.content = self.get_content()
        assert len(self.content) == 8
        self.abbrev_lookup = {k.get_full_name(): k.get_abbrev() for k in Teams}
        self.players = []
        if self.content:
            self.scrape_page()
            self.convert_to_csv()

    def get_soup(self):
        page = urlopen(self.full_url)
        return BeautifulSoup(page, 'html.parser')

    def get_content(self):
        class_name = 'squads_list'
        return self.soup.find(class_=class_name, recursive=True).find_all('a')

    def scrape_page(self):
        for i, elem in enumerate(self.content):
            team_url = f'{self.base_url}{elem["href"]}'
            team_name = elem.text.replace('Squad', '').strip()
            print(team_name, team_url)
            self.extract_players(team_url, team_name)

    def extract_players(self, team_url, team_name):
        page = urlopen(team_url)
        soup = BeautifulSoup(page, 'html.parser')
        player_soups = soup.find(class_='squads_main').find_all('a')
        abbrev = self.abbrev_lookup[team_name]
        for player_soup in player_soups:
            name = player_soup.text.strip()
            if not name:
                continue
            player = {'name': name, 'team': team_name, 'abbrev': abbrev}
            self.players.append(player)

    def convert_to_csv(self):
        header = ['name', 'team', 'abbrev']
        with open(f'squads.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for player in self.players:
                writer.writerow(player)


if __name__ == '__main__':
    Squad()
