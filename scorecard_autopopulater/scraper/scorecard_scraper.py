from abc import ABC, abstractmethod
from urllib.request import urlopen

from bs4 import BeautifulSoup


class ScorecardScraper(ABC):
    def __init__(self, url):
        self.url = url
        self.page = urlopen(self.url)
        self.soup = BeautifulSoup(self.page, 'html.parser')

    @property
    @abstractmethod
    def content(self):
        ...

    @property
    @abstractmethod
    def potm_name(self):
        ...

    @abstractmethod
    def generate_team_names(self):
        ...

    @abstractmethod
    def generate_batting_rows(self):
        ...

    @abstractmethod
    def generate_bowling_rows(self):
        ...
