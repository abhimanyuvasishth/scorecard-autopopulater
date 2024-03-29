from urllib.request import urlopen

from bs4 import BeautifulSoup


class Squad:

    def __init__(self, series_id):
        self.series_id = series_id
        self.base_url = 'https://www.espncricinfo.com'
        self.full_url = f'{self.base_url}/ci/content/squad/index.html?object={self.series_id}'
        self.soup = self.get_soup()
        self.content = self.get_content()
        self.players = {}
        if self.content:
            self.scrape_page()

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
        for elem in self.content:
            team_url = f'{self.base_url}{elem["href"]}'
            team = elem.text.replace('Squads', '').replace('Squad', '').replace('squad', '').strip()
            team = team.replace('T20I', '').replace('T20', '').strip()
            self.players[team] = []
            self.extract_players(team_url, team)

    def extract_players(self, team_url, team_name):
        page = urlopen(team_url)
        soup = BeautifulSoup(page, 'html.parser')
        class_name = 'ds-flex ds-flex-row ds-items-center ds-justify-between'
        player_soups = soup.find_all(class_=class_name)
        for player_soup in player_soups:
            name = player_soup.find_all('a')[0].text.replace(u'\xa0', u' ').strip()
            tag = player_soup.find(class_='ds-text-tight-s ds-font-regular')
            if tag and tag.text == 'Withdrawn player':
                continue
            self.players[team_name].append({
                'name': name,
                'id': player_soup.find('a')['href'].split('-')[-1]
            })
