from dataclasses import dataclass, fields


@dataclass(init=False)
class PlayerRow:
    name: str
    team: str
    abbrev: str
    withdrawn: bool = False

    def __init__(self, **kwargs):
        names = set([field.name for field in fields(self)])
        for key, value in kwargs.items():
            if key in names:
                setattr(self, key, value)
