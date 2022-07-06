import csv

from scorecard_autopopulater.writer.writer import Writer


class CsvWriter(Writer):
    def __init__(self, file_name):
        self.file_name = file_name

    def write_data(self, data: list[dict]):
        with open(self.file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)
