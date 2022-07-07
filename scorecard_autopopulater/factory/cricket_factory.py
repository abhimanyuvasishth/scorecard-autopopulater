from typing import Type

from scorecard_autopopulater.factory.sport_factory import SportFactory
from scorecard_autopopulater.match.cricket_match import CricketMatch
from scorecard_autopopulater.match.match import Match
from scorecard_autopopulater.scraper.cricinfo_scorecard_scraper import CricinfoScorecardScraper
from scorecard_autopopulater.scraper.scorecard_scraper import ScorecardScraper


class CricketFactory(SportFactory):
    def get_match_type(self) -> Type[Match]:
        return CricketMatch

    def get_scorecard_scraper_type(self) -> Type[ScorecardScraper]:
        return CricinfoScorecardScraper
