from abc import ABC, abstractmethod

from scorecard_autopopulater.stat_items import StatItems


class Player(ABC):
    def __init__(self, name, team, order):
        self.name = name
        self.team = team
        self.order = order
        self.statistics = self.initialize_statistics()
        self.active = False

    @staticmethod
    @abstractmethod
    def initialize_statistics() -> dict[str, StatItems]:
        ...

    @abstractmethod
    def update_statistics(self, statistics):
        ...

    @property
    @abstractmethod
    def info(self):
        ...

    def __repr__(self):
        return f'{self.name} | {self.team} | {self.info}'

    def __eq__(self, other):
        return self.team == other.team and self.name == other.name

    def __hash__(self):
        return hash((self.name, self.team))
