from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.reader.csv_file_match_reader import CSVFileMatchReader


def test_reader(monkeypatch):
    reader = CSVFileMatchReader('foo.csv')

    def mock_read_rows():
        yield {
            'team_0': 'Chennai Super Kings',
            'team_1': 'Kolkata Knight Riders',
            'game_0': 2,
            'game_1': 1,
            'match_num': 4,
            'url': 'foo',
            'start_time': '2022-03-26 14:00:00',
        }

    monkeypatch.setattr(reader, 'read_rows', mock_read_rows)
    rows = [row for row in reader.generate_match_rows()]
    assert len(rows) == 1
    assert isinstance(rows[0], MatchRow)
    assert rows[0].start_time.hour == 14
