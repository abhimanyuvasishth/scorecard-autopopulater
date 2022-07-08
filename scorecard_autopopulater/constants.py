from enum import Enum, auto

game1_col = 'E'

in_date_fmt = '%d-%b-%Y, %I:%M %p'
out_date_fmt = '%Y-%m-%d %H:%M:%S'


class Format(Enum):
    T2OI = auto()
    ODI = auto()
    T20 = auto()
    TEST = auto()


class SheetIntroCols(Enum):
    PLAYER = 1
    PLAYING_TEAM = 2
    AUCTION_TEAM = 3


class SheetOffsetCols(Enum):
    RUNS_SCORED = (0, 'runs_scored')
    BALLS_FACED = (1, 'balls_faced')
    STRIKE_RATE = (2, 'strike_rate')
    NOT_OUT = (3, 'not_out')
    OVERS = (4, 'overs')
    ECONOMY_RATE = (5, 'economy_rate')
    WICKETS = (6, 'wickets')
    MAIDENS = (7, 'maidens')
    HATTRICKS = (8, 'hattricks')
    FIELDING = (9, 'fielding')
    BATTING_POINTS = (10, 'batting_points')
    BOWLING_POINTS = (11, 'bowling_points')
    POTM = (12, 'potm')
    KAPTAAN = (13, 'kaptaan')
    POINTS = (14, 'points')

    def get_offset(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]


class Stages(Enum):
    FINISHED = auto()
    RUNNING = auto()
    SCHEDULED = auto()


class Sports(Enum):
    CRICKET = auto()
    SOCCER = auto()
    TENNIS = auto()
