from dataclasses import dataclass
from enum import Enum, auto

from scorecard_autopopulater.match.match import Match
from scorecard_autopopulater.scraper.cricket_scraper import CricketScraper


class CricketMatchFormat(Enum):
    T2OI = auto()
    ODI = auto()
    T20 = auto()
    TEST = auto()
    HUNDRED_BALL = auto()


class CricketMatchStages(Enum):
    FINISHED = auto()
    RUNNING = auto()
    SCHEDULED = auto()


@dataclass(kw_only=True)
class CricketMatch(Match):
    stage: CricketMatchStages = CricketMatchStages.FINISHED
    format: CricketMatchFormat = CricketMatchFormat.T20

    def populate(self):
        self.scraper = CricketScraper(self.id, self.tournament_id)
        for team in self.scraper.generate_teams():
            self.add_team(team)

        self.scraper.add_match_numbers(self.teams)
        if self.stage == CricketMatchStages.SCHEDULED:
            return

        self.scraper.add_players(self.teams)
        self.scraper.add_statistics(self.teams, self.team_lookup)

        if self.stage == CricketMatchStages.FINISHED:
            self.scraper.add_potm_statistics(self.team_lookup)
