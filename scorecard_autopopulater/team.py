from scorecard_autopopulater.player import Player
from scorecard_autopopulater.reader.data_row_reader import DataRowReader


class Team:
    def __init__(self, name, innings, squad_reader: DataRowReader, game_number=1):
        self.name = name
        self.innings = innings
        self.squad_reader = squad_reader
        self.game_number = int(game_number or 1)
        self.players = self.generate_players()

    @property
    def active_players(self):
        return {name: player for name, player in self.players.items() if player.active}

    @property
    def subs(self):
        return {name: player for name, player in self.players.items() if not player.active}

    def generate_players(self) -> dict[str, Player]:
        player_rows = [row for row in self.squad_reader.generate_rows() if row.team == self.name]
        return {row.name: Player(row.name, self.name, self.innings) for row in player_rows}

    def find_player(self, player_name, sub=False):
        relevant_players = self.subs if sub else self.active_players
        for name, player in relevant_players.items():
            if player_name == name:
                return player
            else:
                parts = player_name.split(' ')
                name_parts = name.split(' ')
                num_parts = len(parts)
                if num_parts == 1:
                    if player_name in name_parts:
                        return player
                elif num_parts == 2:
                    if parts[1] in name_parts:
                        if name[0] == player_name[0] or player_name[0] == player_name[0].lower():
                            return player
                        if parts[0] in name_parts:
                            return player
                elif num_parts == 3:
                    if parts[2] in name_parts:
                        if name[0] == player_name[0] or player_name[0] == player_name[0].lower():
                            return player
        return None

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.innings == other.innings
