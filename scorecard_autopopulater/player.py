from scorecard_autopopulater.schema.stat_row import StatRow
from scorecard_autopopulater.stat_items import StatItems, sheet_order


class Player:
    def __init__(self, name, team, innings):
        self.name = name
        self.team = team
        self.innings = innings
        self.statistics = {stat.name: StatRow(*stat.value) for stat in StatItems}
        self.active = False

    def update_statistics(self, statistics):
        for name, value in statistics.items():
            try:
                self.statistics[name].value = self.statistics[name].data_type(value)
                self.active = True
            except ValueError:
                pass

    @property
    def info(self):
        info = []
        for col, order in sheet_order:
            if self.statistics[col].data_type == bool:
                info.append(int(self.statistics[col].value))
            else:
                info.append(self.statistics[col].value)

        return info

    def __repr__(self):
        return f'{self.name} | {self.team}'

    def __eq__(self, other):
        return self.team == other.team and self.name == other.name

    def __hash__(self):
        return hash((self.name, self.team))
