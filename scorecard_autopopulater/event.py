import csv
import logging
import time

from scorecard_autopopulater.constants import SheetOffsetCols
from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.reader.csv_file_match_reader import CSVFileMatchReader
from scorecard_autopopulater.scraper.cricinfo_scorecard_scraper import CricinfoScorecardScraper
from scorecard_autopopulater.utils import compare_info, get_game_col, num_2_str, str_2_num

logging_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)


class Event:
    def __init__(self, test=True):
        self.sheet = GoogleSheet()
        self.test = test

    @staticmethod
    def write_player_row(info, game_num, player):
        print(info, game_num, player)

    def write_player_row_to_sheet(self, info, game_num, player):
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

    def populate_scores(self):
        file_name = 'data/schedule.csv'
        match_generator = MatchGenerator(
            match_reader=CSVFileMatchReader(file_name),
            scraper_type=CricinfoScorecardScraper,
            hours_after=100000,
            limit=1
        )
        for match in match_generator.generate_match_rows():
            match.update_statistics()
            for team in match.teams:
                for player_name, player in team.active_players.items():
                    try:
                        self.write_player_row(player.info, team.game_number, player)
                    except (ValueError, KeyError):
                        logging.error(f'Player not in sheet: {player_name}')

            time.sleep(1)
        logger.info('Completed updating sheet')


# TODO: add cli
if __name__ == '__main__':
    Event(test=False).populate_scores()
