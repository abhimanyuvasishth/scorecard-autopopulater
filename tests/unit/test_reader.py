from datetime import datetime

from scorecard_autopopulater.reader.csv_data_row_reader import CSVDataRowReader
from scorecard_autopopulater.schema.match_row import MatchRow


def test_reader(monkeypatch):
    reader = CSVDataRowReader('foo.csv', MatchRow)

    def mock_read_rows():
        yield {
            'team_0': 'Chennai Super Kings',
            'team_1': 'Kolkata Knight Riders',
            'game_0': 2,
            'game_1': 1,
            'match_num': 4,
            'url': 'foo',
            'start_time': datetime(2022, 1, 20, 20, 0, 0),
        }

    monkeypatch.setattr(reader, 'read_rows', mock_read_rows)
    rows = [row for row in reader.generate_rows()]
    assert len(rows) == 1
    assert isinstance(rows[0], MatchRow)
    assert rows[0].start_time.hour == 20
