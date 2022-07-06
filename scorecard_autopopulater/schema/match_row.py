from dataclasses import dataclass
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
        for key, value in kwargs.items():
            if key in MatchRow.__annotations__:
                if MatchRow.__annotations__[key] == datetime and type(value) == str:
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
