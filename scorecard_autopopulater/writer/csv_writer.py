import csv

from scorecard_autopopulater.writer.writer import Writer


class CsvWriter(Writer):
    def __init__(self, file_name):
        self.file_name = file_name

    def write_data_item(self, data_item: dict):
        with open(self.file_name, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=data_item.keys())
            writer.writerow(data_item)

    def write_data_bulk(self, data: list[dict]):
        with open(self.file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)
