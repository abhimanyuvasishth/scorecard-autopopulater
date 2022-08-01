from abc import abstractmethod
from dataclasses import dataclass, field

from scorecard_autopopulater.team.team import Team


@dataclass(kw_only=True)
class Match:
    id: int
    tournament_id: int
    teams: list[Team] = field(default_factory=list[Team], repr=False)
    team_lookup: dict[int, Team] = field(default_factory=dict[int, Team], repr=False)

    @abstractmethod
    def populate(self):
        ...

    def add_team(self, team: Team):
        self.teams.append(team)
        self.team_lookup[team.id] = team

    def get_team(self, team_id: int) -> Team:
        return self.team_lookup[team_id]
