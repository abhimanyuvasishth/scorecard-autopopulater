from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def write_data(self, data):
        ...
