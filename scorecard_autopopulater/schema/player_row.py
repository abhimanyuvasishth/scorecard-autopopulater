from dataclasses import dataclass


@dataclass(init=False)
class PlayerRow:
    name: str
    team: str
    abbrev: str
    withdrawn: bool = False

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__annotations__:
                setattr(self, key, value)
