import csv
import logging
import time
from datetime import datetime

import pytz

from scorecard_autopopulater.constants import SheetOffsetCols, out_date_fmt
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.match import Match
from scorecard_autopopulater.utils import compare_info, get_game_col, num_2_str, str_2_num

logging_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)


class Event:
    def __init__(self, test=True):
        self.sheet = GoogleSheet()
        self.test = test

    def write_player_row(self, info, game_num, player):
        row = self.sheet.players[player.name]['row']
        col_start = get_game_col(game_num)
        col_end = num_2_str(str_2_num(col_start) + len(info) - 2)
        potm_offset = SheetOffsetCols.POTM.get_offset()
        potm_col = num_2_str(str_2_num(col_start) + potm_offset)

        potm = info[-1]
        cur_potm = self.sheet.get_cell_value(row, potm_col)
        cur_info = self.sheet.get_cell_values(row, col_start, row, col_end)

        if compare_info(info, cur_info) and potm == cur_potm:
            return

        if self.test:
            return

        self.sheet.update_row(row, col_start, col_end, [info[:-1]])
        if potm:
            self.sheet.write_cell_value(row, potm_col, potm)

    def check_players_matching(self):
        players = set()
        with open('data/squads.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] not in self.sheet.players:
                    logger.info(row)
                if row['name'] in players:
                    logger.info(row)
                players.add(row['name'])

        for player in self.sheet.players:
            if player and player not in players:
                logger.info(player)

    def simulate_last_ipl(self):
        with open('data/schedule_2022.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                logger.info(row)
                time.sleep(30)
                match = Match(row['url'])
                match.update_statistics()
                for team in match.teams:
                    for player_name, player in team.players.items():
                        game = row['game_1'] if team == row['team_1'] else row['game_2']
                        assert team in [row['team_1'], row['team_2']]
                        try:
                            self.write_player_row(player.info, int(game), player)
                        except (ValueError, KeyError):
                            logging.error(f'Player not in sheet: {player_name}')

    def populate_scores(self):
        cur_time = datetime.now(pytz.timezone('UTC')).replace(tzinfo=None)
        matches_scraped = []
        with open('data/schedule.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                match_time = datetime.strptime(row['start'], out_date_fmt)
                num_hours = (cur_time - match_time).total_seconds() / 3600
                if num_hours < 0 or num_hours > 5:
                    continue
                logger.info(row)
                match = Match(row['url'])
                match.update_statistics()
                matches_scraped.append(match)
                for team in match.teams:
                    for player_name, player in team.active_players.items():
                        game = row['game_1'] if team == row['team_1'] else row['game_2']
                        try:
                            self.write_player_row(player.info, int(game), player)
                        except (ValueError, KeyError):
                            breakpoint()
                            logging.error(f'Player not in sheet: {player_name}')
                logger.info('Completed updating sheet')
                time.sleep(60)

        if not matches_scraped:
            logger.info('No matches to scrape')


if __name__ == '__main__':
    Event(test=False).populate_scores()
