from scorecard_autopopulater.constants import SheetIntroCols, SheetOffsetCols
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.utils import compare_info, get_game_col, num_2_str, str_2_num
from scorecard_autopopulater.writer.google_sheet_writer import GoogleSheetWriter


class CricketSheetWriter(GoogleSheetWriter):
    def __init__(self, google_sheet: GoogleSheet):
        super().__init__(google_sheet)
        self.players = self.get_players()

    def get_players(self):
        players = {}
        names = self.google_sheet.col_values(SheetIntroCols.PLAYER.value)
        abbrevs = self.google_sheet.col_values(SheetIntroCols.PLAYING_TEAM.value)

        for i, (name, abbrev) in enumerate(zip(names, abbrevs)):
            if name:
                players[name] = {'name': name, 'abbrev': abbrev, 'row': i + 1}

        return players

    def write_data(self, data: dict):
        row = self.players[data['player'].name]['row']
        col_start = get_game_col(data['game_number'])
        col_end = num_2_str(str_2_num(col_start) + len(data['player'].info) - 2)
        potm_offset = SheetOffsetCols.POTM.get_offset()
        potm_col = num_2_str(str_2_num(col_start) + potm_offset)

        potm = data['player'].info[-1]
        cur_potm = self.google_sheet.cell(row, str_2_num(potm_col)).value
        cur_info = self.google_sheet.get(f'{col_start}{row}:{col_end}{row}')

        if compare_info(data['player'].info[:-1], cur_info) and potm == cur_potm:
            return

        self.google_sheet.update(f'{col_start}{row}:{col_end}{row}', [data['player'].info[:-1]])
        if potm:
            self.google_sheet.update_cell(row, str_2_num(potm_col), potm)
