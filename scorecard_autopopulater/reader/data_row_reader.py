from abc import ABC, abstractmethod


class DataRowReader(ABC):
    @abstractmethod
    def read_rows(self):
        ...

    @abstractmethod
    def generate_rows(self) -> list:
        ...
