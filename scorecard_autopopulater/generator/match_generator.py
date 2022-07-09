from abc import ABC, abstractmethod

from scorecard_autopopulater.match.match import Match


class MatchGenerator(ABC):
    def __init__(self, limit=10):
        self.limit = limit

    @abstractmethod
    def generate_matches(self) -> list[Match]:
        ...
