import csv
from dateutil import parser
from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging

from constants import out_date_fmt, abbrev_lookup


class Schedule:

    def __init__(self):
        self.series_id = '1298423'
        self.series_name = 'indian-premier-league-2022'

        self.base_url = f'https://www.espncricinfo.com'
        self.series_url = f'{self.base_url}/series/{self.series_name}-{self.series_id}'
        self.full_url = f'{self.series_url}/match-schedule-fixtures'

        self.soup = self.get_soup()
        self.content = self.get_content()
        self.team_counts = {}
        self.matches = []
        self.start_index = 0
        if self.content:
            self.scrape_page()
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
            match_num = self.start_index + i
            self.matches.append({
                'match_num': match_num,
                'team_1': team_1,
                'abbrev_1': abbrev_lookup[team_1],
                'game_1': self.get_and_update_game_count(team_1),
                'team_2': team_2,
                'abbrev_2': abbrev_lookup[team_2],
                'game_2': self.get_and_update_game_count(team_2),
                'start': self.extract_start(match_num, elem),
                'series_id': self.series_id,
                'match_id': self.extract_match_id(url),
                'url': url,
                'status': self.extract_status(elem)
            })

    @staticmethod
    def extract_match_num(elem):
        return elem['href']

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
    def extract_start(match_num, elem):
        raw_start = elem.find('span').text.replace('tues', 'tue')
        try:
            return parser.parse(raw_start).strftime(out_date_fmt)
        except:
            logging.warning(f'{match_num} could not extract start: {raw_start}')

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
