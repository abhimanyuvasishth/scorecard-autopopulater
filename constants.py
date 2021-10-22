from enum import Enum

game1_col = 'E'

in_date_fmt = '%d-%b-%Y, %I:%M %p'
out_date_fmt = '%Y-%m-%d %H:%M:%S'

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
    POTM = (12, 'potm')
    KAPTAAN = (13, 'kaptaan')
    POINTS = (14, 'points')

    def get_offset(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

class Teams(Enum):
    BANGALORE = (0, 'RCB', 'Bangalore', 'Royal Challengers Bangalore')
    CHENNAI = (1, 'CSK', 'Chennai', 'Chennai Super Kings')
    DELHI = (2, 'DC', 'Delhi', 'Delhi Capitals')
    HYDERABAD = (3, 'SRH', 'Hyderabad', 'Sunrisers Hyderabad')
    KOLKATA = (4, 'KKR', 'Kolkata', 'Kolkata Knight Riders')
    MUMBAI = (5, 'MI', 'Mumbai', 'Mumbai Indians')
    PUNJAB = (6, 'KXIP', 'Punjab', 'Punjab Kings')
    RAJASTHAN = (7, 'RR', 'Rajasthan', 'Rajasthan Royals')
    AFGHANISTAN = (8, 'AFG', 'Afghanistan', 'Afghanistan')
    AUSTRALIA = (9, 'AUS', 'Australia', 'Australia')
    BANGLADESH = (10, 'BAN', 'Bangladesh', 'Bangladesh')
    ENGLAND = (11, 'ENG', 'England', 'England')
    INDIA = (12, 'IND', 'India', 'India')
    IRELAND = (13, 'IRE', 'Ireland', 'Ireland')
    NAMIBIA = (14, 'NAM', 'Namibia', 'Namibia')
    NETHERLANDS = (15, 'NL', 'Netherlands', 'Netherlands')
    NEW_ZEALAND = (16, 'NZ', 'New Zealand', 'New Zealand')
    OMAN = (17, 'OMAN', 'Oman', 'Oman')
    PAPUA_NEW_GUINEA = (18, 'PNG', 'Papua New Guinea', 'Papua New Guinea')
    PAKISTAN = (19, 'PAK', 'Pakistan', 'Pakistan')
    SCOTLAND = (20, 'SCO', 'Scotland', 'Scotland')
    SOUTH_AFRICA = (21, 'SA', 'South Africa', 'South Africa')
    SRI_LANKA = (22, 'SL', 'Sri Lanka', 'Sri Lanka')
    WEST_INDIES = (23, 'WI', 'West Indies', 'West Indies')

    def get_id(self):
        return self.value[0]

    def get_abbrev(self):
        return self.value[1]

    def get_name(self):
        return self.value[2]

    def get_full_name(self):
        return self.value[3]

abbrev_lookup = {k.get_full_name(): k.get_abbrev() for k in Teams}
safe_modes = {'not out', 'retired hurt'}
