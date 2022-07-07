from datetime import datetime

import pytest

from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.match import Match
from scorecard_autopopulater.player import Player
from scorecard_autopopulater.reader.csv_data_row_reader import CSVDataRowReader
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.schema.player_row import PlayerRow
from scorecard_autopopulater.scraper.cricinfo_scorecard_scraper import CricinfoScorecardScraper
from scorecard_autopopulater.stat_items import StatItems
from scorecard_autopopulater.team import Team


@pytest.fixture(scope='session')
def squad_reader():
    return CSVDataRowReader('data/squads/current_ipl_squad.csv', PlayerRow)


@pytest.fixture
def match_generator(squad_reader):
    return MatchGenerator(
        match_reader=CSVDataRowReader('foo.csv', MatchRow),
        squad_reader=squad_reader,
        scraper_type=CricinfoScorecardScraper,
        hours_after=100000,
        limit=1
    )


@pytest.fixture
def match_row():
    return MatchRow(**{
        'team_0': 'Chennai Super Kings',
        'team_1': 'Kolkata Knight Riders',
        'game_0': 3,
        'game_1': 4,
        'match_num': 4,
        'url': 'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423'
               '/chennai-super-kings-vs-kolkata-knight-riders-1st-match-1304047/full-scorecard',
        'start_time': datetime(2022, 1, 20, 20, 0, 0),
    })


@pytest.fixture
def matches(monkeypatch, match_generator, match_row):
    def mock_generate_rows():
        yield match_row

    monkeypatch.setattr(match_generator.match_reader, 'generate_rows', mock_generate_rows)
    return [match for match in match_generator.generate_match_rows()]


@pytest.fixture
def teams(squad_reader):
    return [
        Team(name='Chennai Super Kings', innings=0, game_number=3, squad_reader=squad_reader),
        Team(name='Kolkata Knight Riders', innings=1, game_number=4, squad_reader=squad_reader),
    ]


@pytest.fixture
def player(teams):
    return Player('Ravindra Jadeja', teams[0].name, teams[0].innings)


def test_match_generator(matches, teams):
    assert len(matches) == 1
    assert isinstance(matches[0], Match)
    assert matches[0].teams == teams


def test_team_initialization(teams, player):
    assert player.name in teams[0].players
    assert teams[0].players[player.name] == player


def test_get_player(teams, player):
    assert player.name in teams[0].subs
    assert teams[0].find_player('Ravindra', sub=True) == player
    assert teams[0].find_player('Jadeja', sub=True) == player


def test_statistics(matches, teams, player):
    match = matches[0]
    match.update_statistics()
    match_player = match.teams[0].players[player.name]
    assert match_player.statistics[StatItems.WICKETS.name].value == 0
    assert match_player.statistics[StatItems.RUNS_SCORED.name].value == 26
    assert match_player.statistics[StatItems.FIELDING.name].value == 1
    assert not match_player.statistics[StatItems.POTM.name].value
    assert player.name in matches[0].teams[0].active_players
