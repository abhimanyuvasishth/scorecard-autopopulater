from abc import ABC, abstractmethod

from scorecard_autopopulater.match.match import Match


class MatchGenerator(ABC):
    @abstractmethod
    def generate_matches(self, **kwargs) -> list[Match]:
        ...
