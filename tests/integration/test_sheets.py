import pytest

from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.utils import get_game_col, str_2_num


@pytest.fixture
def sheet():
    return GoogleSheet(doc_name='IPL 15 auction', sheet_name='Points Worksheet')


def test_game_cols(sheet):
    for game in range(1, 18):
        col = get_game_col(game)
        assert sheet.cell(1, str_2_num(col)).value == f'Game {game}'
