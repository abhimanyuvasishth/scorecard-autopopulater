from datetime import datetime

from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.writer.writer import Writer


class GoogleSheetWriter(Writer):
    def __init__(self, google_sheet: GoogleSheet):
        self.google_sheet = google_sheet

    def write_data(self, data: list[dict]):
        for row_num, row in enumerate(data):
            for col_num, item in enumerate(row.items()):
                key, value = item
                if isinstance(value, datetime):
                    value = datetime.isoformat(value)

                self.google_sheet.update_cell(row_num + 1, 2 * col_num + 1, key)
                self.google_sheet.update_cell(row_num + 1, 2 * col_num + 2, value)
