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
        # Batting Points
        batting_points = self.runs_scored
        if self.strike_rate >= 200 and self.balls_faced >= 7:
            batting_points = max(1.75 * batting_points, 50 + batting_points)
        elif (200 > self.strike_rate >= 175) and self.balls_faced >= 7:
            batting_points = max(1.5 * batting_points, 50 + batting_points)
        elif (175 > self.strike_rate >= 150) and self.balls_faced >= 7:
            batting_points = 1.2 * batting_points
        elif (150 > self.strike_rate >= 120) and self.balls_faced >= 7:
            batting_points = 1.1 * batting_points
        elif (75 > self.strike_rate >= 50) and self.balls_faced >= 7:
            batting_points -= self.balls_faced
        elif (50 > self.strike_rate >= 0) and self.balls_faced >= 7:
            batting_points -= 3 * self.balls_faced

        if self.runs_scored < 5 and not self.not_out:
            batting_points -= 25
        elif 100 > self.runs_scored >= 50:
            batting_points += 25
        elif 150 > self.runs_scored >= 100:
            batting_points += 60
        elif self.runs_scored >= 150:
            batting_points += 100

        # Bowling Points
        wicket_points = [0, 30, 60, 100, 150, 200, 225, 250]
        bowling_points = wicket_points[self.wickets] + self.maidens * 25

        if self.economy_rate <= 3 and self.overs >= 4:
            bowling_points += 50
        elif (3 < self.economy_rate <= 5) and self.overs >= 3:
            bowling_points += 35
        elif (5 < self.economy_rate <= 6.5) and self.overs >= 3:
            bowling_points += 25
        elif (10 > self.economy_rate >= 9) and self.overs >= 1:
            bowling_points -= 10
        elif (12 > self.economy_rate >= 10) and self.overs >= 1:
            bowling_points -= 25
        elif (self.economy_rate >= 12) and self.overs >= 1:
            bowling_points -= 40

        # Fielding & Bonus Points
        fielding_points = self.fielding_primary * 7
        potm_points = 0 * self.potm
        return batting_points + bowling_points + fielding_points + potm_points
