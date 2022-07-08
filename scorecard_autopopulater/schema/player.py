from dataclasses import dataclass, field

from scorecard_autopopulater.schema.statistics import Statistics


@dataclass
class Player:
    id: int
    name: str
    long_name: str
    fielding_name: str
    statistics: Statistics = field(default_factory=Statistics)
