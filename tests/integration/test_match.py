import pytest

from scorecard_autopopulater.match import Match
from scorecard_autopopulater.player import Player
from scorecard_autopopulater.scraper.cricinfo_scorecard_scraper import \
    CricinfoScorecardScraper
from scorecard_autopopulater.stat_items import StatItems
from scorecard_autopopulater.team import Team


@pytest.fixture
def scraper():
    url = 'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/punjab-kings-vs' \
          '-delhi-capitals-64th-match-1304110/full-scorecard'
    return CricinfoScorecardScraper(url)


@pytest.fixture
def match(scraper):
    return Match(scraper)


@pytest.fixture
def teams():
    return [Team('Delhi Capitals', 0), Team('Punjab Kings', 1)]


@pytest.fixture
def player(teams):
    return Player('Shardul Thakur', teams[0].name, teams[0].innings)


def test_initialization(match, teams):
    assert match.teams == teams


def test_statistics(match, teams, player):
    match.update_statistics()
    # assert match == player
    assert match.teams[0].players[player.name].statistics[StatItems.WICKETS.name].value == 4
#     assert match.teams[0].players[player.name].statistics[StatItems.RUNS_SCORED.name].value == 3
#     assert match.teams[0].players[player.name].statistics[StatItems.FIELDING.name].value == 0
#     assert match.teams[0].players[player.name].statistics[StatItems.POTM.name].value
