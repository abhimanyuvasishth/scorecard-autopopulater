from abc import abstractmethod

from scorecard_autopopulater.player_row import PlayerRow
from scorecard_autopopulater.scraper.scraper import Scraper


class SquadScraper(Scraper):

    @abstractmethod
    def generate_player_rows(self) -> list[PlayerRow]:
        ...
