import pytest

from scorecard_autopopulater.player_row import PlayerRow
from scorecard_autopopulater.scraper.cricinfo_squad_scraper import CricinfoSquadScraper


@pytest.fixture
def scraper():
    url = 'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/squads'
    return CricinfoSquadScraper(url)


def test_scraper(scraper):
    for row in scraper.generate_player_rows():
        assert isinstance(row, PlayerRow)
        break
