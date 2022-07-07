from abc import ABC

from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.writer.writer import Writer


class GoogleSheetWriter(Writer, ABC):
    def __init__(self, google_sheet: GoogleSheet):
        self.google_sheet = google_sheet
