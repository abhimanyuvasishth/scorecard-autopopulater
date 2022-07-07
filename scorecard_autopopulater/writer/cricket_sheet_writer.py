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
        teams = self.google_sheet.col_values(SheetIntroCols.PLAYING_TEAM.value)

        for i, (name, team) in enumerate(zip(names, teams)):
            if name:
                players[name] = {'name': name, 'team': team, 'row': i + 1}

        return players

    def write_data_item(self, data_item: dict):
        row = self.players[data_item['player'].name]['row']
        col_start = get_game_col(data_item['game_number'])
        col_end = num_2_str(str_2_num(col_start) + len(data_item['player'].info) - 2)
        potm_offset = SheetOffsetCols.POTM.get_offset()
        potm_col = num_2_str(str_2_num(col_start) + potm_offset)
        stats = data_item['player'].info[:-1]

        potm = data_item['player'].info[-1]
        cur_potm = self.google_sheet.cell(row, str_2_num(potm_col)).value
        cur_info = self.google_sheet.get(f'{col_start}{row}:{col_end}{row}')

        if compare_info(stats, cur_info) and potm == cur_potm:
            return

        self.google_sheet.update(f'{col_start}{row}:{col_end}{row}', [stats])
        if potm:
            self.google_sheet.update_cell(row, str_2_num(potm_col), potm)
