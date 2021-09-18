import csv
from datetime import datetime
import logging
import pytz
from google_sheet import GoogleSheet
from match import Match
import time
from constants import in_date_fmt, out_date_fmt, SheetOffsetCols
from utils import get_game_col, str_2_num, num_2_str, compare_info

logging_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)


class Event:
    def __init__(self, test=True):
        self.sheet = GoogleSheet()
        self.test = test

    def write_player_row(self, info, game_num, player):
        row = self.sheet.players[player['name']]['row']
        col_start = get_game_col(game_num)
        col_end = num_2_str(str_2_num(col_start) + len(info) - 1)
        potm_offset = SheetOffsetCols.POTM.get_offset()
        potm_col = num_2_str(str_2_num(col_start) + (potm_offset))

        if self.test:
            return

        potm = player.get('potm')
        cur_potm = self.sheet.get_cell_value(row, potm_col)
        cur_info = self.sheet.get_cell_values(row, col_start, row, col_end)

        if compare_info(info, cur_info) and str(potm) == str(cur_potm):
            return

        self.sheet.update_row(row, col_start, col_end, [info])
        if potm:
            self.sheet.write_cell_value(row, potm_col, potm)

    def check_players_matching(self):
        players = set()
        with open(f'squads.csv') as csvfile:
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
        with open(f'schedule_2020.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                logger.info(row)
                time.sleep(30)
                match = Match(row['series_id'], row['match_id'])
                for name in match.players.keys():
                    info = match.get_info(name)
                    player = match.players[name]
                    team = player['team']
                    game = row['game_1'] if team == row['team_1'] else row['game_2']
                    assert team in [row['team_1'], row['team_2']]
                    try:
                        self.write_player_row(info, int(game), player)
                    except ValueError:
                        logging.error(f'Player not in sheet: {name}')

    def populate_scores(self):
        cur_time = datetime.now(pytz.timezone('UTC')).replace(tzinfo=None)
        matches_scraped = []
        with open(f'schedule_2021.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                match_time = datetime.strptime(row['start'], out_date_fmt)
                num_hours = (cur_time - match_time).total_seconds() / 3600
                if num_hours < 0 or num_hours > 5:
                    continue
                logger.info(row)
                match = Match(row['series_id'], row['match_id'])
                matches_scraped.append(match)
                for name in match.players.keys():
                    info = match.get_player_info(name)
                    player = match.players[name]
                    team = player['team']
                    abbrev = player['abbrev']
                    game = row['game_1'] if team == row['team_1'] else row['game_2']
                    try:
                        assert team in [row['team_1'], row['team_2']]
                        assert self.sheet.players[name]['abbrev'] == abbrev
                        self.write_player_row(info, int(game), player)
                    except (ValueError, KeyError):
                        logging.error(f'Player not in sheet: {name}')
                    except AssertionError:
                        logging.error(f'Player {name} team mismatch {abbrev}')

        if not matches_scraped:
            logger.info('No matches to scrape')


if __name__ == '__main__':
    Event(test=True).populate_scores()
