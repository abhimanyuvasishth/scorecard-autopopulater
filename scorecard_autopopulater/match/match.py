from abc import ABC, abstractmethod

from scorecard_autopopulater.reader.data_row_reader import DataRowReader
from scorecard_autopopulater.scraper.scorecard_scraper import ScorecardScraper


class Match(ABC):
    def __init__(self, scraper: ScorecardScraper, squad_reader: DataRowReader, team_games=None):
        self.scraper = scraper
        self.squad_reader = squad_reader
        self.team_names = scraper.generate_team_names()
        self.team_games = team_games or {}
        self.teams = self.generate_teams()

    @abstractmethod
    def generate_teams(self):
        ...

    @abstractmethod
    def update_statistics(self):
        ...
