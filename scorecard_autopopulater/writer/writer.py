from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def write_data_item(self, *args, **kwargs):
        ...
