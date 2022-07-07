from typing import Type

from scorecard_autopopulater.factory.sport_factory import SportFactory
from scorecard_autopopulater.match.cricket_match import CricketMatch
from scorecard_autopopulater.match.cricket_test_match import CricketTestMatch
from scorecard_autopopulater.match.match import Match
from scorecard_autopopulater.scraper.cricket_scorecard_scraper import CricketScorecardScraper
from scorecard_autopopulater.scraper.scorecard_scraper import ScorecardScraper


class CricketFactory(SportFactory):
    def __init__(self, test_match=False):
        self.test_match = test_match

    def get_match_type(self) -> Type[Match]:
        return CricketTestMatch if self.test_match else CricketMatch

    def get_scorecard_scraper_type(self) -> Type[ScorecardScraper]:
        return CricketScorecardScraper
