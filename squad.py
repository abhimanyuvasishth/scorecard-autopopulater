import csv
from urllib.request import urlopen

from bs4 import BeautifulSoup

from constants import abbrev_lookup


class Squad:

    def __init__(self):
        self.series_id = '1298423'
        self.base_url = 'https://www.espncricinfo.com'
        self.full_url = f'{self.base_url}/ci/content/squad/index.html?object={self.series_id}'
        self.soup = self.get_soup()
        self.content = self.get_content()
        assert len(self.content) == 10
        self.players = []
        if self.content:
            self.scrape_page()
            self.convert_to_csv()

    def get_soup(self):
        page = urlopen(self.full_url)
        return BeautifulSoup(page, 'html.parser')

    def get_content(self):
        class_name = 'ds-flex lg:ds-flex-row sm:ds-flex-col lg:ds-items-center ' \
                     'lg:ds-justify-between ds-py-2 ds-px-4 ds-flex-wrap ' \
                     'odd:ds-bg-fill-content-alternate'
        elems = []
        for elem in self.soup.find_all(class_=class_name):
            elems.append(elem.find_all('a')[0])
        return elems

    def scrape_page(self):
        for i, elem in enumerate(self.content):
            team_url = f'{self.base_url}{elem["href"]}'
            team_name = elem.text.replace('Squads', '').replace('Squad', '').strip()
            self.extract_players(team_url, team_name)

    def extract_players(self, team_url, team_name):
        page = urlopen(team_url)
        soup = BeautifulSoup(page, 'html.parser')
        class_name = 'ds-relative ds-flex ds-flex-row ds-space-x-4 ds-p-4 lg:ds-px-6'
        player_soups = soup.find_all(class_=class_name)
        abbrev = abbrev_lookup[team_name]
        for player_soup in player_soups:
            name = player_soup.find_all('a')[1].text.replace(u'\xa0', u' ').strip()
            tag = player_soup.find(class_='ds-text-tight-s ds-font-regular')
            if tag and tag.text == 'Withdrawn player':
                continue
            player = {'name': name, 'team': team_name, 'abbrev': abbrev}
            self.players.append(player)

    def convert_to_csv(self):
        header = ['name', 'team', 'abbrev']
        with open('squads.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for player in self.players:
                writer.writerow(player)


if __name__ == '__main__':
    Squad()
