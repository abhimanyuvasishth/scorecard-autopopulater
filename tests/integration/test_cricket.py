import pytest

from scorecard_autopopulater.generator.cricket_match_generator import (CricketMatchFormat,
                                                                       CricketMatchGenerator,
                                                                       CricketMatchStages)
from scorecard_autopopulater.match.cricket_match import CricketMatch
from scorecard_autopopulater.player.player import Player


@pytest.fixture
def match() -> CricketMatch:
    return CricketMatch(
        id=1304111,
        tournament_id=1298423,
        stage=CricketMatchStages.FINISHED,
        format=CricketMatchFormat.T2OI
    )


@pytest.fixture
def player(match) -> Player:
    return match.teams[1].get_player(1079470)


@pytest.fixture
def potm(match) -> Player:
    return match.teams[0].get_player(446763)


def test_generator():
    limit = 1
    live_matches = [match for match in CricketMatchGenerator(limit=limit).generate_matches()]
    assert len(live_matches) == limit
    assert isinstance(live_matches[0], CricketMatch)


def test_match(match):
    assert isinstance(match, CricketMatch)
    assert len(match.teams) == 2
    assert match.teams[0].match_number == 13
    assert match.teams[1].match_number == 13
    assert len(match.teams[0].players) == 12
    assert len(match.teams[1].players) == 11


def test_player_statistics(player):
    assert isinstance(player, Player)
    assert player.long_name == 'Ramandeep Singh'
    assert player.player_stats[0].economy_rate == 6.66
    assert player.player_stats[0].fielding_primary == 1


def test_potm_statistics(potm):
    assert potm.long_name == 'Rahul Tripathi'
    assert potm.player_stats[0].potm == 1
    assert potm.stat_row[1] == 1
    assert potm.stat_row[0][0] == 76
