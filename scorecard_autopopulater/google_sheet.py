import gspread
from oauth2client.service_account import ServiceAccountCredentials

from scorecard_autopopulater.constants import SheetIntroCols, SheetOffsetCols
from scorecard_autopopulater.player.player import Player
from scorecard_autopopulater.team.team import Team
from scorecard_autopopulater.utils import get_game_col, num_2_str, str_2_num


class GoogleSheet:
    def __init__(self, doc_name, sheet_name):
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        file = 'credentials.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(doc_name).worksheet(sheet_name)
        self.players = self.get_players()

    def get_players(self):
        players = {}
        names = self.sheet.col_values(SheetIntroCols.PLAYER.value)
        teams = self.sheet.col_values(SheetIntroCols.PLAYING_TEAM.value)

        for i, (name, team) in enumerate(zip(names, teams)):
            if name:
                players[name] = {'name': name, 'team': team, 'row': i + 1}

        return players

    def get_row_cols(self, name, match_number, data_row):
        row = self.players[name]['row']
        start = get_game_col(match_number)
        end = num_2_str(str_2_num(start) + len(data_row) - 1)
        potm_col = num_2_str(str_2_num(start) + SheetOffsetCols.POTM.get_offset())
        return row, start, end, potm_col

    def write_data_item(self, player: Player, team: Team):
        data_row, potm = player.stat_row
        row, start, end, potm_col = self.get_row_cols(player.long_name, team.match_number, data_row)
        write_range = f'{start}{row}:{end}{row}'
        self.sheet.update(write_range, [data_row])
        self.sheet.update_cell(row, str_2_num(potm_col), potm)
