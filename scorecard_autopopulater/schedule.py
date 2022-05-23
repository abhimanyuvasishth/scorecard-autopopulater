import csv
import logging
from urllib.request import urlopen

from bs4 import BeautifulSoup
from dateutil import parser

from scorecard_autopopulater.constants import abbrev_lookup, out_date_fmt


class Schedule:

    def __init__(self, year, url):
        self.series_id = '1298423'
        self.series_name = 'indian-premier-league-2022'

        self.base_url = 'https://www.espncricinfo.com'
        self.series_url = f'{self.base_url}/series/{self.series_name}-{self.series_id}'
        # self.full_url = f'{self.series_url}/match-schedule-fixtures'

        self.year = year
        self.full_url = url

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
        class_name = 'ds-flex ds-flex-wrap'
        return self.soup.find_all(class_=class_name, recursive=True)

    def scrape_page(self):
        for i, elem in enumerate(list(self.content[0])[::-1]):
            team_1, team_2, result = self.extract_teams(elem)
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
        terms = elem.find('a')['href'].split('/')
        return '/'.join(terms[:len(terms) - 1] + ['match-impact-player'])

    @staticmethod
    def extract_match_id(url):
        return url.split('/')[5].split('-')[-1]

    @staticmethod
    def extract_teams(elem):
        return [team.text for team in elem.find_all('p')]

    @staticmethod
    def extract_start(match_num, elem):
        class_name = 'ds-text-tight-xs ds-truncate ds-text-ui-typo-mid'
        raw_start = ''.join(elem.find(class_=class_name).text.split(',')[2:4]).strip()
        try:
            return parser.parse(raw_start).strftime(out_date_fmt)
        except Exception:
            logging.warning(f'{match_num} could not extract start: {raw_start}')

    @staticmethod
    def extract_status(elem):
        return ''
        # return elem.find(class_='status-text').text

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
        with open(f'data/raw/past_schedules/schedule_{self.year}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for match in self.matches:
                writer.writerow(match)


if __name__ == '__main__':
    import time
    years = list(range(2008, 2023))
    urls = [
        'https://www.espncricinfo.com/series/indian-premier-league-2007-08-313494/match-results',
        'https://www.espncricinfo.com/series/indian-premier-league-2009-374163/match-results',
        'https://www.espncricinfo.com/series/indian-premier-league-2009-10-418064/match-results',
        'https://www.espncricinfo.com/series/indian-premier-league-2011-466304/match-results',
        'https://www.espncricinfo.com/series/indian-premier-league-2012-520932/match-results',
        'https://www.espncricinfo.com/series/indian-premier-league-2013-586733/match-results',
        'https://www.espncricinfo.com/series/pepsi-indian-premier-league-2014-695871/match-results',
        'https://www.espncricinfo.com/series/pepsi-indian-premier-league-2015-791129/match-results',
        'https://www.espncricinfo.com/series/ipl-2016-968923/match-results',
        'https://www.espncricinfo.com/series/ipl-2017-1078425/match-results',
        'https://www.espncricinfo.com/series/ipl-2018-1131611/match-results',
        'https://www.espncricinfo.com/series/ipl-2019-1165643/match-results',
        'https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results',
        'https://www.espncricinfo.com/series/ipl-2021-1249214/match-results',
        'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/match-results',
    ]
    for year, url in zip(years, urls):
        print(year)
        Schedule(year, url)
        time.sleep(2)
