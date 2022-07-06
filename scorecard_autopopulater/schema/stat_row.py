from dataclasses import dataclass


@dataclass(init=False)
class StatRow:
    def __init__(self, role, name, data_type, default_value, sheet_order):
        self.role = role
        self.name = name
        self.data_type = data_type
        self.value = default_value
        self.sheet_order = sheet_order

    def __repr__(self):
        return str(self.value)
