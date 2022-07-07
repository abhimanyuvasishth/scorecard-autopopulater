from datetime import datetime

import pytest

from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.match import Match
from scorecard_autopopulater.reader.csv_data_row_reader import CSVDataRowReader
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.scraper.cricinfo_scorecard_scraper import CricinfoScorecardScraper
from scorecard_autopopulater.team import Team


@pytest.fixture
def match_generator():
    return MatchGenerator(
        match_reader=CSVDataRowReader('foo.csv', MatchRow),
        scraper_type=CricinfoScorecardScraper,
        hours_after=100000,
        limit=1
    )


@pytest.fixture
def teams():
    return [Team('Chennai Super Kings', 0, 3), Team('Kolkata Knight Riders', 1, 4)]


def test_match_generator(monkeypatch, match_generator, teams):
    def mock_generate_rows():
        yield MatchRow(**{
            'team_0': 'Chennai Super Kings',
            'team_1': 'Kolkata Knight Riders',
            'game_0': 3,
            'game_1': 4,
            'match_num': 4,
            'url': 'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423'
                   '/chennai-super-kings-vs-kolkata-knight-riders-1st-match-1304047/full-scorecard',
            'start_time': datetime(2022, 1, 20, 20, 0, 0),
        })

    monkeypatch.setattr(match_generator.match_reader, 'generate_rows', mock_generate_rows)
    matches = [match for match in match_generator.generate_match_rows()]
    assert len(matches) == 1
    assert isinstance(matches[0], Match)
    assert matches[0].teams == teams
