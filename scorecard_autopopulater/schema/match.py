from dataclasses import dataclass, field

from scorecard_autopopulater.constants import Format, Stages
from scorecard_autopopulater.schema.team import Team
from scorecard_autopopulater.scraper.cricket_scraper import CricketScraper


@dataclass
class Match:
    id: int
    series_id: int
    start_time: str
    stage: Stages = Stages.FINISHED
    format: Format = Format.T20
    teams: list[Team] = field(default_factory=list[Team])
    team_lookup: dict[int, Team] = field(default_factory=dict[int, Team])

    def __post_init__(self):
        self.scraper = CricketScraper(self.id, self.series_id)
        for inning, team in enumerate(self.scraper.generate_teams()):
            self.add_team(team)

        self.scraper.add_players(self.teams)
        self.scraper.add_match_numbers(self.teams)
        self.scraper.add_statistics(self.teams, self.team_lookup)

        if self.stage == Stages.FINISHED:
            self.scraper.add_potm_statistics(self.team_lookup)

    def add_team(self, team: Team):
        self.teams.append(team)
        self.team_lookup[team.id] = team

    def get_team(self, team_id: int) -> Team:
        return self.team_lookup[team_id]
