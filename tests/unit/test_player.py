import pytest

from scorecard_autopopulater.player import Player
from scorecard_autopopulater.stat_items import StatItems, sheet_order


@pytest.fixture
def player():
    return Player('Rohit Sharma', 'Mumbai Indians', 1)


def test_player_initialization(player):
    for stat_item in StatItems:
        assert player.statistics[stat_item.name].value == stat_item.default_value


def test_update_statistics(player):
    player.update_statistics({StatItems.RUNS_SCORED.name: 40})
    assert player.statistics[StatItems.RUNS_SCORED.name].value == 40
    assert player.active


def test_info(player):
    assert len(player.info) == len(sheet_order)
