from scorecard_autopopulater.player.player import Player
from scorecard_autopopulater.schema.stat_row import StatRow
from scorecard_autopopulater.stat_items import StatItems, sheet_order


class CricketPlayer(Player):
    @staticmethod
    def initialize_statistics() -> dict[str, StatItems]:
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
