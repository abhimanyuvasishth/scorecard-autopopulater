from dataclasses import dataclass, fields
from datetime import datetime


@dataclass(init=False)
class MatchRow:
    team_0: str
    team_1: str
    url: str
    start_time: datetime
    match_num: int = 0
    game_0: int = 0
    game_1: int = 0

    def __init__(self, **kwargs):
        names = set([field.name for field in fields(self)])
        for key, value in kwargs.items():
            if key in names:
                setattr(self, key, value)
