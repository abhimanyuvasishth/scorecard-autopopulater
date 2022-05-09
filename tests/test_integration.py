import pytest

from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.utils import get_game_col


@pytest.mark.integration
def test_game_cols():
    google_sheet = GoogleSheet()
    for game in range(1, 18):
        col = get_game_col(game)
        _ = google_sheet.get_cell_value(1, col) == f'Game {game}'
