import gspread
from oauth2client.service_account import ServiceAccountCredentials

from utils import letter_to_number, number_to_letter

class GoogleSheet:

    def __init__(self):
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        file = 'credentials.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.get_sheet()
        self.players = self.get_all_players()

    def get_sheet(self):
        return self.client.open('IPL 14 auction').worksheet('Test Points Worksheet')

    def get_all_players(self):
        return self.sheet.col_values(1)

    def get_cell_value(self, row, col_str):
        col_num = letter_to_number(col_str)
        return self.sheet.cell(row, col_num).value

    def write_cell_value(self, row, col_str, value):
        col_num = letter_to_number(col_str)
        self.sheet.update_cell(row, col_num, value)

    def update_row(self, row, start_str, end_str, values):
        self.sheet.update(f'{start_str}{row}:{end_str}{row}', values)
