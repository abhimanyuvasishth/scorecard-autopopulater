from dataclasses import dataclass, field

from scorecard_autopopulater.player_stats.player_stats import PlayerStats


@dataclass(kw_only=True)
class Player:
    id: int
    name: str
    long_name: str
    fielding_name: str
    player_stats: list[PlayerStats] = field(default_factory=list[PlayerStats])

    def __post_init__(self):
        setattr(self, 'player_stats', [PlayerStats(), PlayerStats()])

    @property
    def stat_row(self):
        return self.player_stats[0].stat_row
