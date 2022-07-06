import csv
from dataclasses import dataclass

from scorecard_autopopulater.reader.data_row_reader import DataRowReader


class CSVDataRowReader(DataRowReader):
    def __init__(self, file_name: str, row_type: dataclass):
        self.file_name = file_name
        super().__init__(row_type)

    def read_rows(self):
        with open(self.file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

    def generate_rows(self) -> list[dataclass]:
        for row in self.read_rows():
            yield self.row_type(**row)
