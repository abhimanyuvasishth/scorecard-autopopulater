from scorecard_autopopulater.constants import SheetIntroCols, SheetOffsetCols
from scorecard_autopopulater.schema.player import Player
from scorecard_autopopulater.schema.statistics import Statistics
from scorecard_autopopulater.schema.team import Team
from scorecard_autopopulater.utils import get_game_col, num_2_str, str_2_num
from scorecard_autopopulater.writer.google_sheet_writer import GoogleSheetWriter


class CricketSheetWriter(GoogleSheetWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.players = self.get_players()

    def get_players(self):
        players = {}
        names = self.google_sheet.col_values(SheetIntroCols.PLAYER.value)
        teams = self.google_sheet.col_values(SheetIntroCols.PLAYING_TEAM.value)

        for i, (name, team) in enumerate(zip(names, teams)):
            if name:
                players[name] = {'name': name, 'team': team, 'row': i + 1}

        return players

    @staticmethod
    def create_info(statistics: Statistics):
        return (
            [
                statistics.runs_scored,
                statistics.balls_faced,
                statistics.strike_rate,
                int(statistics.not_out),
                statistics.overs,
                statistics.economy_rate,
                statistics.wickets,
                statistics.maidens,
                statistics.hat_tricks,
                statistics.fielding_primary,
            ],
            int(statistics.potm)
        )

    def write_data_item(self, player: Player, team: Team):
        data_row, potm = self.create_info(player.statistics)

        # finding row and column
        row_number = self.players[player.long_name]['row']
        col_start = get_game_col(team.match_number)
        col_end = num_2_str(str_2_num(col_start) + len(data_row) - 1)
        potm_col = num_2_str(str_2_num(col_start) + SheetOffsetCols.POTM.get_offset())

        # writing information
        write_range = f'{col_start}{row_number}:{col_end}{row_number}'
        self.google_sheet.update(write_range, [data_row])
        self.google_sheet.update_cell(row_number, str_2_num(potm_col), potm)
