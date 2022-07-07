from datetime import datetime

from scorecard_autopopulater.constants import SheetIntroCols, SheetOffsetCols
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.utils import compare_info, get_game_col, num_2_str, str_2_num
from scorecard_autopopulater.writer.writer import Writer


class GoogleSheetWriter(Writer):
    def __init__(self, google_sheet: GoogleSheet):
        self.google_sheet = google_sheet
        self.players = self.get_players()

    def write_data(self, data: list[dict]):
        for row_num, row in enumerate(data):
            for col_num, item in enumerate(row.items()):
                key, value = item
                if isinstance(value, datetime):
                    value = datetime.isoformat(value)

                self.google_sheet.update_cell(row_num + 1, 2 * col_num + 1, key)
                self.google_sheet.update_cell(row_num + 1, 2 * col_num + 2, value)

    def get_players(self):
        players = {}
        names = self.google_sheet.col_values(SheetIntroCols.PLAYER.value)
        abbrevs = self.google_sheet.col_values(SheetIntroCols.PLAYING_TEAM.value)

        for i, (name, abbrev) in enumerate(zip(names, abbrevs)):
            if name:
                players[name] = {'name': name, 'abbrev': abbrev, 'row': i + 1}

        return players

    def write_player_row(self, player, game_num):
        row = self.players[player.name]['row']
        col_start = get_game_col(game_num)
        col_end = num_2_str(str_2_num(col_start) + len(player.info) - 2)
        potm_offset = SheetOffsetCols.POTM.get_offset()
        potm_col = num_2_str(str_2_num(col_start) + potm_offset)

        potm = player.info[-1]
        cur_potm = self.google_sheet.cell(row, str_2_num(potm_col)).value
        cur_info = self.google_sheet.get(f'{col_start}{row}:{col_end}{row}')

        if compare_info(player.info[:-1], cur_info) and potm == cur_potm:
            return

        self.google_sheet.update(f'{col_start}{row}:{col_end}{row}', [player.info[:-1]])
        if potm:
            self.google_sheet.update_cell(row, str_2_num(potm_col), potm)
