import gspread
from oauth2client.service_account import ServiceAccountCredentials

from scorecard_autopopulater.constants import SheetIntroCols
from scorecard_autopopulater.utils import str_2_num


class GoogleSheet:

    def __init__(self):
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        file = 'credentials.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
        self.client = gspread.authorize(creds)
        self.doc_name = 'IPL 15 auction'
        self.sheet_name = 'Points Worksheet'
        self.sheet = self.get_sheet()
        self.players = self.get_all_players()

    def get_sheet(self):
        return self.client.open(self.doc_name).worksheet(self.sheet_name)

    def get_all_players(self):
        players = {}
        names = self.sheet.col_values(SheetIntroCols.PLAYER.value)
        abbrevs = self.sheet.col_values(SheetIntroCols.PLAYING_TEAM.value)
        for i in range(len(names)):
            name, abbrev, row = names[i], abbrevs[i], i + 1
            if name:
                players[name] = {'name': name, 'abbrev': abbrev, 'row': row}
        return players

    def get_cell_value(self, row, col_str):
        col_num = str_2_num(col_str)
        return self.sheet.cell(row, col_num).value

    def get_cell_values(self, start_row, start_str, end_row, end_str):
        return self.sheet.get(f'{start_str}{start_row}:{end_str}{end_row}')

    def write_cell_value(self, row, col_str, value):
        col_num = str_2_num(col_str)
        self.sheet.update_cell(row, col_num, value)

    def update_row(self, row, start_str, end_str, values):
        self.sheet.update(f'{start_str}{row}:{end_str}{row}', values)
