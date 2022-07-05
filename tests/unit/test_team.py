import pytest

from scorecard_autopopulater.player import Player
from scorecard_autopopulater.team import Team


@pytest.fixture
def team():
    return Team('Fake Team', 0)


@pytest.fixture
def player(team):
    return Player('Fake Player', team.name, team.innings)


# TODO: add players to teams better
def test_team_initialization(team, player):
    team.players = {player.name: Player(player.name, team.name, team.innings)}
    assert player.name in team.players
    assert team.players[player.name] == player


def test_get_player(team, player):
    team.players = {player.name: Player(player.name, team.name, team.innings)}
    assert player.name in team.subs
    assert team.find_player('Fake', sub=True) == player
    assert team.find_player('Player', sub=True) == player
