import pytest

from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.utils import get_game_col, str_2_num
from scorecard_autopopulater.writer.cricket_sheet_writer import CricketSheetWriter


@pytest.fixture
def sheet():
    return GoogleSheet(doc_name='IPL 15 auction', sheet_name='Points Worksheet')


@pytest.fixture
def writer(sheet):
    return CricketSheetWriter(sheet)


def test_game_cols(sheet):
    for game in range(1, 18):
        col = get_game_col(game)
        assert sheet.cell(1, str_2_num(col)).value == f'Game {game}'


def test_players(writer):
    test_cases = [
        {'name': 'Shivam Dube', 'team': 'Chennai Super Kings', 'row': 10},
        {'name': 'Karn Sharma', 'team': 'Royal Challengers Bangalore', 'row': 205},
        {'name': 'Vijay Shankar', 'team': 'Gujarat Titans', 'row': 77},
    ]

    for test_case in test_cases:
        player = writer.players[test_case['name']]
        for key, value in player.items():
            assert player[key] == test_case[key]
