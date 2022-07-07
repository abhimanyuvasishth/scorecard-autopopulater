import pytest

from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.scraper.cricket_schedule_scraper import CricketScheduleScraper


@pytest.fixture
def scraper():
    url = 'https://www.espncricinfo.com/series/new-zealand-in-ireland-2022-1307472/match-schedule' \
          '-fixtures'
    return CricketScheduleScraper(url)


def test_scraper(scraper):
    for row in scraper.generate_match_rows():
        assert isinstance(row, MatchRow)
        break
