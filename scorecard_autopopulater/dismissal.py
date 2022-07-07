from enum import Enum

from scorecard_autopopulater.utils import extract_name


class DismissalType(Enum):
    CAUGHT = ('caught', 'c ')
    RUN_OUT = ('run_out', 'run out')
    OTHER = ('other', 'other')
    STUMPED = ('stumped', 'st ')

    def get_text(self):
        return self.value[1]


class Dismissal:
    def __init__(self, dismissal: str):
        self.dismissal = dismissal
        self.dismissal_type = self.extract_dismissal_type()
        self.fielder, self.bowler = self.extract_fielder_bowler()
        self.is_sub = 'sub (' in self.dismissal

    def extract_dismissal_type(self) -> DismissalType:
        try:
            raw_fielder, raw_bowler = self.dismissal.split(' b ')
            if raw_fielder.startswith('c '):
                return DismissalType.CAUGHT
            elif raw_fielder.startswith('st '):
                return DismissalType.STUMPED
        except ValueError:
            if self.dismissal.startswith('run out'):
                return DismissalType.RUN_OUT

        return DismissalType.OTHER

    def extract_fielder_bowler(self) -> (str, str):
        if self.dismissal_type in {DismissalType.CAUGHT, DismissalType.STUMPED}:
            fielder, bowler = self.dismissal.split(' b ')
            fielder = fielder.split(self.dismissal_type.get_text())[1]
            if fielder == '&':
                fielder = extract_name(bowler)
            else:
                fielder = extract_name(fielder)
            return fielder, extract_name(bowler)
        elif self.dismissal_type == DismissalType.RUN_OUT:
            fielders = extract_name(self.dismissal.split('run out')[1])
            return fielders.split('/')[0], None
        else:
            return None, None
