import csv

from scorecard_autopopulater.constants import SheetOffsetCols
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.utils import compare_info, get_game_col, num_2_str, str_2_num


class Event:
    def __init__(self, test=True):
        self.sheet = GoogleSheet()
        self.test = test

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
                    print(row)
                if row['name'] in players:
                    print(row)
                players.add(row['name'])

        for player in self.sheet.players:
            if player and player not in players:
                print(player)
