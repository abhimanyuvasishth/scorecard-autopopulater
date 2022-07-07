from datetime import datetime

import pytz

from scorecard_autopopulater.factory.sport_factory import SportFactory
from scorecard_autopopulater.match.match import Match
from scorecard_autopopulater.reader.data_row_reader import DataRowReader


class MatchGenerator:
    def __init__(self, match_reader: DataRowReader, squad_reader: DataRowReader,
                 factory: SportFactory, hours_before=0, hours_after=5, limit=None):
        self.match_reader = match_reader
        self.squad_reader = squad_reader
        self.factory = factory
        self.hours_before = hours_before
        self.hours_after = hours_after
        self.limit = limit
        self.match_type = self.factory.get_match_type()
        self.scorecard_scraper_type = self.factory.get_scorecard_scraper_type()

    def generate_match_rows(self) -> list[Match]:
        cur_time = datetime.now(pytz.timezone('UTC')).replace(tzinfo=None)
        for i, row in enumerate(self.match_reader.generate_rows()):
            if i == self.limit:
                return

            num_hours = (cur_time - row.start_time).total_seconds() / 3600
            if num_hours < self.hours_before or num_hours > self.hours_after:
                continue

            team_games = {row.team_0: row.game_0, row.team_1: row.game_1}
            yield self.match_type(
                scraper=self.scorecard_scraper_type(row.url),
                team_games=team_games,
                squad_reader=self.squad_reader
            )
