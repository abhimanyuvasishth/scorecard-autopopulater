from google_sheet import GoogleSheet
from utils import convert_column_to_number, convert_number_to_column
from utils import get_game_col

def test_column_number_conversion():
    assert convert_number_to_column(convert_column_to_number('A')) == 'A'
    assert convert_number_to_column(convert_column_to_number('IG')) == 'IG'
    assert convert_number_to_column(convert_column_to_number('JF')) == 'JF'

def test_game_cols():
    google_sheet = GoogleSheet()
    for game in range(1, 18):
        col = get_game_col(game)
        cell_value = google_sheet.get_cell_value(1, col) == f'Game {game}'
