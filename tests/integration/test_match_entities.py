import pytest

from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.schema.match import Match
from scorecard_autopopulater.schema.player import Player


@pytest.fixture
def matches(monkeypatch):
    def mock_scrape_matches():
        yield 1304111

    match_generator = MatchGenerator()
    monkeypatch.setattr(match_generator, 'scrape_matches', mock_scrape_matches)
    return [match for match in match_generator.generate_matches()]


def test_match_generator(matches):
    assert len(matches) == 1
    assert isinstance(matches[0], Match)
    assert len(matches[0].teams) == 2
    assert matches[0].teams[0].match_number == 13
    assert matches[0].teams[1].match_number == 13


def test_statistics(matches):
    player = matches[0].teams[1].get_player(1079470)
    assert isinstance(player, Player)
    assert player.name == 'Ramandeep Singh'
    assert player.statistics.economy_rate == 6.66
    assert player.statistics.fielding_primary == 1
    assert matches[0].teams[0].get_player(446763).statistics.potm == 1
