from abc import ABC, abstractmethod
from dataclasses import dataclass


class DataRowReader(ABC):
    def __init__(self, row_type):
        self.row_type = row_type

    @abstractmethod
    def read_rows(self):
        ...

    @abstractmethod
    def generate_rows(self) -> list[dataclass]:
        ...
