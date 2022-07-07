from scorecard_autopopulater.schema.stat_row import StatRow
from scorecard_autopopulater.stat_items import StatItems, sheet_order


class CricketPlayer:
    def __init__(self, name, team, order):
        self.name = name
        self.team = team
        self.order = order
        self.statistics = self.generate_statistics()
        self.active = False

    @staticmethod
    def generate_statistics() -> dict[str, StatItems]:
        return {stat.name: StatRow(*stat.value) for stat in StatItems}

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
