from datetime import date, datetime, timedelta

from dateutil import parser

from scorecard_autopopulater.constants import out_date_fmt
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.scraper.schedule_scraper import ScheduleScraper


class CricketScheduleScraper(ScheduleScraper):
    def __init__(self, url):
        self.base_url = 'https://www.espncricinfo.com'
        self.team_counts = {}
        super().__init__(url)

    @property
    def content(self):
        class_name = 'ds-px-4 ds-py-3'
        return self.soup.find_all(class_=class_name, recursive=True)

    def generate_match_rows(self) -> list[MatchRow]:
        for i, elem in enumerate(self.content):
            team_0, team_1, status = [team.text for team in elem.find_all('p')]
            if 'TBA' in [team_0, team_1]:
                continue

            yield MatchRow(
                team_0=team_0,
                team_1=team_1,
                url=self.extract_url(elem),
                start_time=self.extract_start(elem),
                match_num=i,
                game_0=self.get_and_update_game_count(team_0),
                game_1=self.get_and_update_game_count(team_1)
            )

    def extract_url(self, element):
        path_parts = element.find('a')['href'].split('/')
        path_parts[-1] = 'full-scorecard'
        return f"{self.base_url}{'/'.join(path_parts)}"

    @staticmethod
    def extract_start(element):
        raw_start = element.find('span').text\
            .lower()\
            .replace('tues', 'tue')\
            .replace('today', date.today().isoformat())\
            .replace('tomorrow', (date.today() + timedelta(days=1)).isoformat())

        try:
            return datetime.fromisoformat(parser.parse(raw_start).strftime(out_date_fmt))
        except parser.ParserError:
            return datetime.now().isoformat()

    def get_and_update_game_count(self, team):
        try:
            count = self.team_counts[team]
        except KeyError:
            count = 0
        self.team_counts[team] = count + 1
        return count + 1
