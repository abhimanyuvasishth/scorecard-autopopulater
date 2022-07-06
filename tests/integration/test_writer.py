from dataclasses import asdict
from datetime import datetime
from tempfile import NamedTemporaryFile

import pytest

from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.reader.csv_data_row_reader import CSVDataRowReader
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.writer.csv_writer import CsvWriter
from scorecard_autopopulater.writer.google_sheet_writer import GoogleSheetWriter


@pytest.fixture
def match_rows():
    return [
        MatchRow(**{
            'team_0': 'Chennai Super Kings',
            'team_1': 'Kolkata Knight Riders',
            'game_0': 2,
            'game_1': 1,
            'match_num': 4,
            'url': 'foo',
            'start_time': datetime(2022, 1, 20, 20, 0, 0),
        }),
        MatchRow(**{
            'team_0': 'Rajasthan Royals',
            'team_1': 'Royal Challengers Bangalore',
            'game_0': 2,
            'game_1': 1,
            'match_num': 4,
            'url': 'foo',
            'start_time': datetime(2022, 1, 20, 20, 0, 0),
        }),
    ]


@pytest.fixture
def data(match_rows):
    return [asdict(row) for row in match_rows]


def test_csv_writer(data):
    with NamedTemporaryFile() as fp:
        CsvWriter(fp.name).write_data(data)
        read_rows = [row for row in CSVDataRowReader(fp.name, MatchRow).generate_rows()]
        assert len(read_rows) == 2
        assert isinstance(read_rows[0], MatchRow)


def test_google_writer(data):
    sheet = GoogleSheet('Sandbox', 'Sandbox')
    GoogleSheetWriter(sheet).write_data(data)
    assert sheet.cell(1, 1).value == 'team_0'
    sheet.clear()
