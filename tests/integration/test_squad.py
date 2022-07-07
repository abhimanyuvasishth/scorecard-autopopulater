import pytest

from scorecard_autopopulater.schema.player_row import PlayerRow
from scorecard_autopopulater.scraper.cricket_squad_scraper import CricketSquadScraper


@pytest.fixture
def scraper():
    url = 'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/squads'
    return CricketSquadScraper(url)


def test_scraper(scraper):
    for row in scraper.generate_player_rows():
        assert isinstance(row, PlayerRow)
        break
