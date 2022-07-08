import pytest

from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.schema.player import Statistics
from scorecard_autopopulater.utils import get_game_col, str_2_num


@pytest.fixture
def sheet():
    return GoogleSheet(doc_name='IPL 15 auction', sheet_name='Points Worksheet')


@pytest.fixture
def players():
    return [
        {'name': 'Shivam Dube', 'team': 'Chennai Super Kings', 'row': 10},
        {'name': 'Karn Sharma', 'team': 'Royal Challengers Bangalore', 'row': 205},
        {'name': 'Vijay Shankar', 'team': 'Gujarat Titans', 'row': 77},
    ]


def test_game_cols(sheet):
    for game in range(1, 18):
        col = get_game_col(game)
        assert sheet.sheet.cell(1, str_2_num(col)).value == f'Game {game}'


def test_players(sheet, players):
    for test_player in players:
        player = sheet.players[test_player['name']]
        for key, value in player.items():
            assert player[key] == test_player[key]


def test_write_row(sheet):
    data_row, _ = Statistics().stat_row
    assert sheet.get_row_cols('Shivam Dube', 13, data_row) == (10, 'GC', 'GL', 'GO')
