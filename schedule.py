import csv
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

from constants import in_date_fmt, out_date_fmt, Teams

class Schedule:

    def __init__(self):
        self.series_id = '1249214'
        self.base_url = f'https://www.espncricinfo.com'
        self.series_url = f'{self.base_url}/series/ipl-2021-{self.series_id}'
        self.full_url = f'{self.series_url}/match-schedule-fixtures'
        self.soup = self.get_soup()
        self.content = self.get_content()
        self.abbrev_lookup = {k.get_full_name(): k.get_abbrev() for k in Teams}
        self.team_counts = {}
        self.matches = []
        if self.content:
            self.scrape_page()
            assert len(self.matches) == 56
            self.convert_to_csv()

    def get_soup(self):
        page = urlopen(self.full_url)
        return BeautifulSoup(page, 'html.parser')

    def get_content(self):
        class_name = 'match-info-link-FIXTURES'
        return self.soup.find_all(class_=class_name, recursive=True)

    def scrape_page(self):
        for i, elem in enumerate(self.content):
            team_1, team_2 = self.extract_teams(elem)
            if 'TBA' in [team_1, team_2]:
                continue
            url = f'{self.base_url}{self.extract_url(elem)}'
            self.matches.append({
                'match_num': i + 1,
                'team_1': team_1,
                'abbrev_1': self.abbrev_lookup[team_1],
                'game_1': self.get_and_update_game_count(team_1),
                'team_2': team_2,
                'abbrev_2': self.abbrev_lookup[team_2],
                'game_2': self.get_and_update_game_count(team_2),
                'start': self.extract_start(elem),
                'series_id': self.series_id,
                'match_id': self.extract_match_id(url),
                'url': url,
                'status': self.extract_status(elem)
            })

    @staticmethod
    def extract_url(elem):
        return elem['href']

    @staticmethod
    def extract_match_id(url):
        return url.split('/')[5].split('-')[-1]

    @staticmethod
    def extract_teams(elem):
        return [team.text for team in elem.find_all('p')]

    @staticmethod
    def extract_start(elem):
        raw_start = elem.find('span').text
        return datetime.strptime(raw_start, in_date_fmt).strftime(out_date_fmt)

    @staticmethod
    def extract_status(elem):
        return elem.find(class_='status-text').text

    def get_and_update_game_count(self, team):
        try:
            count = self.team_counts[team]
        except KeyError:
            count = 0
        self.team_counts[team] = count + 1
        return count + 1

    def convert_to_csv(self):
        header = [
            'match_num', 'team_1', 'abbrev_1', 'game_1', 'team_2', 'abbrev_2',
            'game_2', 'start', 'series_id', 'match_id', 'url', 'status'
        ]
        with open(f'schedule.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for match in self.matches:
                writer.writerow(match)


if __name__ == '__main__':
    Schedule()
