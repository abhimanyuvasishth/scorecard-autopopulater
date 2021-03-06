from dataclasses import dataclass, field

from scorecard_autopopulater.player.player import Player


@dataclass(kw_only=True)
class Team:
    id: int
    name: str
    long_name: str
    abbreviation: str
    match_number: int = 0
    players: list[Player] = field(default_factory=list[Player], repr=False)
    player_lookup: dict[int, Player] = field(default_factory=dict[int, Player], repr=False)

    def add_player(self, player: Player):
        self.players.append(player)
        self.player_lookup[player.id] = player

    def get_player(self, player_id: int) -> Player:
        return self.player_lookup[player_id]
