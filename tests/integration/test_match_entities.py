import pytest

from scorecard_autopopulater.constants import Format, Stages
from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.schema.match import Match
from scorecard_autopopulater.schema.player import Player


@pytest.fixture
def match() -> Match:
    return Match(1304111, 1298423, '2022-05-17T14:00:00.000Z', Stages.FINISHED, Format.T2OI)


@pytest.fixture
def player(match) -> Player:
    return match.teams[1].get_player(1079470)


@pytest.fixture
def potm(match) -> Player:
    return match.teams[0].get_player(446763)


def test_generator():
    limit = 1
    live_matches = [live_match for live_match in MatchGenerator.generate_matches(limit=limit)]
    assert len(live_matches) == limit
    assert isinstance(live_matches[0], Match)


def test_match(match):
    assert isinstance(match, Match)
    assert len(match.teams) == 2
    assert match.teams[0].match_number == 13
    assert match.teams[1].match_number == 13
    assert len(match.teams[0].players) == 12
    assert len(match.teams[1].players) == 11


def test_player_statistics(player):
    assert isinstance(player, Player)
    assert player.long_name == 'Ramandeep Singh'
    assert player.statistics[0].economy_rate == 6.66
    assert player.statistics[0].fielding_primary == 1


def test_potm_statistics(potm):
    assert potm.long_name == 'Rahul Tripathi'
    assert potm.statistics[0].potm == 1
    assert potm.stat_row[1] == 1
    assert potm.stat_row[0][0] == 76
