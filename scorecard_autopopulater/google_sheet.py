import gspread
from gspread.exceptions import APIError
from oauth2client.service_account import ServiceAccountCredentials

from scorecard_autopopulater.constants import SheetOffsetCols
from scorecard_autopopulater.player.player import Player
from scorecard_autopopulater.team.team import Team
from scorecard_autopopulater.utils import get_game_col, num_2_str, str_2_num, tracing


class SheetIntegrityError(Exception):
    pass


class GoogleSheet:
    def __init__(self, doc_name, sheet_name):
        self.doc_name = doc_name
        self.sheet_name = sheet_name
        self.client = self.get_client()
        self.sheet = self.get_sheet()

    @tracing(errors=FileNotFoundError, message='credentials file does not exist', raises=True)
    def get_client(self):
        file_name = 'credentials.json'
        scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scopes)
        return gspread.authorize(creds)

    @tracing(errors=APIError, message='read API requests exhausted', raises=True)
    def get_sheet(self):
        return self.client.open(self.doc_name).worksheet(self.sheet_name)

    def get_player_row(self, name):
        cells = self.sheet.findall(name)
        if len(cells) > 1:
            raise SheetIntegrityError(f'Duplicate Player {name}')
        elif len(cells) == 0:
            raise SheetIntegrityError(f'Player Not Found {name}')
        else:
            return cells[0].row

    def get_row_cols(self, name, match_number, data_row):
        row = self.get_player_row(name)
        start = get_game_col(match_number)
        end = num_2_str(str_2_num(start) + len(data_row) - 1)
        potm_col = num_2_str(str_2_num(start) + SheetOffsetCols.POTM.get_offset())
        return row, start, end, potm_col

    @tracing(errors=APIError, message='write API requests exhausted', raises=True)
    def write_data_item(self, player: Player, team: Team):
        data_row, potm = player.stat_row
        row, start, end, potm_col = self.get_row_cols(player.long_name, team.match_number, data_row)
        write_range = f'{start}{row}:{end}{row}'
        self.sheet.update(write_range, [data_row])
        self.sheet.update_cell(row, str_2_num(potm_col), potm)

    def write_data_value(self, row, col, value):
        self.sheet.update_cell(row, col, value)
