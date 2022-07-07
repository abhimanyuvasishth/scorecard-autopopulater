from scorecard_autopopulater.player.cricket_player import CricketPlayer
from scorecard_autopopulater.player.player import Player
from scorecard_autopopulater.team.team import Team


class CricketTeam(Team):
    @property
    def active_players(self):
        return {name: player for name, player in self.players.items() if player.active}

    @property
    def subs(self):
        return {name: player for name, player in self.players.items() if not player.active}

    def generate_players(self) -> dict[str, Player]:
        player_rows = [row for row in self.squad_reader.generate_rows() if row.team == self.name]
        return {row.name: CricketPlayer(row.name, self.name, self.order) for row in player_rows}
