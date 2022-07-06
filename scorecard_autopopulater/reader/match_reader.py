from abc import ABC, abstractmethod

from scorecard_autopopulater.match_row import MatchRow


class MatchReader(ABC):
    @abstractmethod
    def read_rows(self):
        ...

    @abstractmethod
    def generate_match_rows(self) -> list[MatchRow]:
        ...
