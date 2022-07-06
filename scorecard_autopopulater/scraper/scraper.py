from abc import ABC, abstractmethod
from urllib.request import urlopen

from bs4 import BeautifulSoup


class Scraper(ABC):
    def __init__(self, url):
        self.url = url
        self.page = urlopen(self.url)
        self.soup = BeautifulSoup(self.page, 'html.parser')

    @property
    @abstractmethod
    def content(self):
        ...
