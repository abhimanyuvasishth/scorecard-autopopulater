from dataclasses import dataclass, field

from scorecard_autopopulater.schema.team import Team


@dataclass
class Match:
    id: int
    start_time: str
    teams: list[Team] = field(default_factory=list[Team])
    team_lookup: dict[int, Team] = field(default_factory=dict[int, Team])

    def add_team(self, team: Team):
        self.teams.append(team)
        self.team_lookup[team.id] = team

    def get_team(self, team_id: int) -> Team:
        return self.team_lookup[team_id]
