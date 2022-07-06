from abc import abstractmethod

from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.scraper.scraper import Scraper


class ScheduleScraper(Scraper):

    @abstractmethod
    def generate_match_rows(self) -> list[MatchRow]:
        ...
