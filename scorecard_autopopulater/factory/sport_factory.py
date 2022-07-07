from abc import ABC, abstractmethod
from typing import Type

from scorecard_autopopulater.match.match import Match
from scorecard_autopopulater.scraper.scorecard_scraper import ScorecardScraper


class SportFactory(ABC):
    @abstractmethod
    def get_match_type(self) -> Type[Match]:
        ...

    @abstractmethod
    def get_scorecard_scraper_type(self) -> Type[ScorecardScraper]:
        ...
