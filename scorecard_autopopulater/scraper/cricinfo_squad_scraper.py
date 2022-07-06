from urllib.request import urlopen

from bs4 import BeautifulSoup

from scorecard_autopopulater.player_row import PlayerRow
from scorecard_autopopulater.scraper.squad_scraper import SquadScraper
from scorecard_autopopulater.constants import abbrev_lookup


class CricinfoSquadScraper(SquadScraper):
    def __init__(self, url):
        self.base_url = 'https://www.espncricinfo.com'
        super().__init__(url)

    @property
    def content(self):
        class_name = 'ds-flex lg:ds-flex-row sm:ds-flex-col lg:ds-items-center ' \
                     'lg:ds-justify-between ds-py-2 ds-px-4 ds-flex-wrap ' \
                     'odd:ds-bg-fill-content-alternate'
        content = []
        for element in self.soup.find_all(class_=class_name):
            content.append(element.find_all('a')[0])
        return content

    @staticmethod
    def generate_player_soups(url):
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        class_name = 'ds-relative ds-flex ds-flex-row ds-space-x-4 ds-p-4 lg:ds-px-6'
        return soup.find_all(class_=class_name)

    def generate_player_rows(self) -> list[PlayerRow]:
        for i, elem in enumerate(self.content):
            team_url = f"{self.base_url}{elem['href']}"
            team_name = elem.text.replace('Squads', '').replace('Squad', '').strip()
            abbrev = abbrev_lookup[team_name]

            for player_soup in self.generate_player_soups(team_url):
                name = player_soup.find_all('a')[1].text.replace(u'\xa0', u' ').strip()
                tag = player_soup.find(class_='ds-text-tight-s ds-font-regular')
                withdrawn = (tag is not None and tag.text == 'Withdrawn player')
                yield PlayerRow(name=name, team=team_name, abbrev=abbrev, withdrawn=withdrawn)
