from dataclasses import dataclass


@dataclass(kw_only=True)
class PlayerStats:
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

    @property
    def stat_row(self):
        return (
            [
                self.runs_scored,
                self.balls_faced,
                self.strike_rate,
                int(self.not_out),
                self.overs,
                self.economy_rate,
                self.wickets,
                self.maidens,
                self.hat_tricks,
                self.fielding_primary,
            ],
            int(self.potm)
        )

    @property
    def points(self):
        batting_points = self.runs_scored
        if (200 > self.strike_rate >= 150) and self.balls_faced >= 7:
            batting_points = 1.2 * batting_points
        elif (200 > self.strike_rate >= 175) and self.balls_faced >= 7:
            batting_points = 1.5 * batting_points
        elif (self.strike_rate >= 200) and self.balls_faced >= 7:
            batting_points = 1.75 * batting_points
        bowling_points = self.wickets * 25 + self.maidens * 25
        fielding_points = self.fielding_primary * 10
        potm_points = 25 * self.potm
        if (self.runs_scored < 5 or self.strike_rate < 90) and not self.not_out:
            batting_points -= 25
        if self.economy_rate > 10:
            bowling_points -= 25
        elif self.economy_rate < 6.5 and self.overs > 3:
            bowling_points += 25
        return batting_points + bowling_points + fielding_points + potm_points
