import pytest

from scorecard_autopopulater.constants import Format, Stages
from scorecard_autopopulater.schema.match import Match
from scorecard_autopopulater.schema.player import Player


@pytest.fixture
def matches():
    return [
        Match(1304111, 1298423, '2022-05-17T14:00:00.000Z', Stages.FINISHED, Format.T2OI)
    ]


def test_match_generator(matches):
    assert len(matches) == 1
    assert isinstance(matches[0], Match)
    assert len(matches[0].teams) == 2
    assert matches[0].teams[0].match_number == 13
    assert matches[0].teams[1].match_number == 13
    assert len(matches[0].teams[0].players) == 12
    assert len(matches[0].teams[1].players) == 11


def test_statistics(matches):
    player = matches[0].teams[1].get_player(1079470)
    assert isinstance(player, Player)
    assert player.name == 'Ramandeep Singh'
    assert player.statistics[0].economy_rate == 6.66
    assert player.statistics[0].fielding_primary == 1
    assert matches[0].teams[0].get_player(446763).statistics[0].potm == 1
