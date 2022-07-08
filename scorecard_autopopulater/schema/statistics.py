from dataclasses import dataclass


@dataclass
class Statistics:
    dismissal: str = 'not out'
    runs_scored: int = 0
    balls_faced: int = 0
    minutes: int = 0
    fours_scored: int = 0
    sixes_scored: int = 0
    strike_rate: float = 0.0
    not_out: bool = True
    overs: int = 0
    maidens: int = 0
    runs_conceded: int = 0
    wickets: int = 0
    economy_rate: float = 0.0
    dots_bowled: int = 0
    fours_conceded: int = 0
    sixes_conceded: int = 0
    wides: int = 0
    no_balls: int = 0
    hat_tricks: int = 0
    fielding_primary: int = 0
    fielding_secondary: int = 0
    potm: int = 0