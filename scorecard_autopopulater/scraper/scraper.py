from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class Scraper(ABC):
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page, 'html.parser')

    @property
    @abstractmethod
    def content(self):
        ...
