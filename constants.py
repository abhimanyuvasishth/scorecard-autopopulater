from enum import Enum

game1_col = 'E'

class BatCols(Enum):
    DISMISSAL = (0, 'dismissal')
    RUNS_SCORED = (1, 'runs_scored')
    BALLS_FACED = (2, 'balls_faced')
    FOURS_SCORED = (3, 'fours_scored')
    SIXES_SCORED = (4, 'sixed_scored')
    STRIKE_RATE = (5, 'strike_rate')
    NOT_OUT = (6, 'not_out')

    def get_id(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

class BowlCols(Enum):
    OVERS = (0, 'overs')
    MAIDENS = (1, 'maidens')
    RUNS_CONCEDED = (2, 'runs_conceded')
    WICKETS = (3, 'wickets')
    ECONOMY_RATE = (4, 'economy_rate')
    DOTS_BOWLED = (5, 'dots_bowled')
    FOURS_CONCEDED = (6, 'fours_conceded')
    SIXES_CONCEDED = (7, 'sixes_conceded')
    WIDES = (8, 'wides')
    NO_BALLS = (9, 'no_balls')
    HATTRICKS = (10, 'hattricks')

    def get_id(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

class FieldCols(Enum):
    FIELDING = (0, 'fielding')

    def get_id(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

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
    FIELDING_POINTS = (12, 'fielding_points')
    MOTM = (13, 'motm')
    KAPTAAN = (14, 'kaptaan')
    POINTS = (15, 'points')

    def get_offset(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]
