from dataclasses import dataclass, field

from scorecard_autopopulater.schema.statistics import Statistics


@dataclass
class Player:
    id: int
    name: str
    long_name: str
    fielding_name: str
    statistics: list[Statistics] = field(default_factory=list[Statistics])

    def __post_init__(self):
        setattr(self, 'statistics', [Statistics(), Statistics()])

    @property
    def stat_row(self):
        return self.statistics[0].stat_row
