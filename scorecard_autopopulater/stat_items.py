from collections import namedtuple
from enum import Enum

Stat = namedtuple('Stat', ['role', 'name', 'data_type', 'default_value', 'sheet_order'])


class StatItems(Enum):

    DISMISSAL = Stat('batting', 'dismissal', str, 'not out', None)
    RUNS_SCORED = Stat('batting', 'runs_scored', int, 0, 0)
    BALLS_FACED = Stat('batting', 'balls_faced', int, 0, 1)
    MINUTES_PLAYED = Stat('batting', 'minutes_played', int, 0, None)
    FOURS_SCORED = Stat('batting', 'fours_scored', int, 0, None)
    SIXES_SCORED = Stat('batting', 'sixes_scored', int, 0, None)
    STRIKE_RATE = Stat('batting', 'strike_rate', float, 0.0, 2)
    NOT_OUT = Stat('batting', 'not_out', bool, True, 3)
    OVERS = Stat('bowling', 'overs', float, 0, 4)
    MAIDENS = Stat('bowling', 'maidens', int, 0, 7)
    RUNS_CONCEDED = Stat('bowling', 'runs_conceded', int, 0, None)
    WICKETS = Stat('bowling', 'wickets', int, 0, 6)
    ECONOMY_RATE = Stat('bowling', 'economy_rate', float, 0.0, 5)
    DOTS_BOWLED = Stat('bowling', 'dots_bowled', int, 0, None)
    FOURS_CONCEDED = Stat('bowling', 'fours_conceded', int, 0, None)
    SIXES_CONCEDED = Stat('bowling', 'sixes_conceded', int, 0, None)
    WIDES = Stat('bowling', 'wides', int, 0, None)
    NO_BALLS = Stat('bowling', 'no_balls', int, 0, None)
    HAT_TRICKS = Stat('bowling', 'hat_tricks', int, 0, 8)
    FIELDING = Stat('fielding', 'fielding', int, 0, 9)
    POTM = Stat('general', 'potm', bool, False, 10)

    @property
    def role(self):
        return self.value.role

    @property
    def name(self):
        return self.value.name

    @property
    def data_type(self):
        return self.value.data_type

    @property
    def sheet_order(self):
        return self.value.sheet_order

    @property
    def default_value(self):
        return self.value.default_value


batting_row = [stat.name for stat in StatItems if stat.role == 'batting']
bowling_row = [stat.name for stat in StatItems if stat.role == 'bowling']
sheet_columns = [
    (stat.name, stat.sheet_order) for stat in StatItems if stat.sheet_order is not None
]
sheet_order = sorted(sheet_columns, key=lambda x: x[1])
