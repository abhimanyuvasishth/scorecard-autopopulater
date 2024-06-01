import requests
from bs4 import BeautifulSoup


class Stats:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()
        self.content = self.get_content()

    def get_soup(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
        response = requests.get(self.url, headers=headers)
        return BeautifulSoup(response.text, 'html.parser')

    def get_content(self):
        data = self.soup.find_all('td', style='white-space: nowrap;')[1:]
        matches = [elem.find('a')['href'] for elem in data]
        match_ids = [match.split('/')[-1].split('.')[0] for match in matches]
        return match_ids
