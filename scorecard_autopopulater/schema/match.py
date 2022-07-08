from dataclasses import dataclass, field

from scorecard_autopopulater.schema.team import Team
from scorecard_autopopulater.scraper.cricket_scraper import CricketScraper


@dataclass
class Match:
    id: int
    series_id: int
    start_time: str
    teams: list[Team] = field(default_factory=list[Team])
    team_lookup: dict[int, Team] = field(default_factory=dict[int, Team])
    scraper: CricketScraper = field(default_factory=CricketScraper)

    def __post_init__(self):
        setattr(self, 'scraper', CricketScraper(self.id, self.series_id))
        for inning, team in enumerate(self.scraper.generate_teams()):
            self.add_team(team)

        self.scraper.add_players(self.teams)
        self.scraper.add_match_numbers(self.teams)
        self.scraper.add_statistics(self.teams, self.team_lookup)

        for potm_team_id, potm_player_id in self.scraper.add_potm_statistics():
            self.get_team(potm_team_id).get_player(potm_player_id).statistics[0].potm = 1

    def add_team(self, team: Team):
        self.teams.append(team)
        self.team_lookup[team.id] = team

    def get_team(self, team_id: int) -> Team:
        return self.team_lookup[team_id]
