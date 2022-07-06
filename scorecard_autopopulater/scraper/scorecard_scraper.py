from abc import abstractmethod

from scorecard_autopopulater.scraper.scraper import Scraper


class ScorecardScraper(Scraper):
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
