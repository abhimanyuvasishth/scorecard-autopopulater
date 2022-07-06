import csv
from datetime import datetime

from scorecard_autopopulater.constants import out_date_fmt
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.reader.match_reader import MatchReader


class CSVFileMatchReader(MatchReader):
    def __init__(self, file_name):
        self.file_name = file_name

    def read_rows(self):
        with open(self.file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

    def generate_match_rows(self) -> list[MatchRow]:
        for row in self.read_rows():
            row['start_time'] = datetime.strptime(row['start_time'], out_date_fmt)
            yield MatchRow(**row)
