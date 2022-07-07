import csv

from scorecard_autopopulater.player import Player


class Team:
    def __init__(self, name, innings, game_number=1):
        self.name = name
        self.innings = innings
        self.game_number = int(game_number or 1)
        self.players = self._generate_players()

    @property
    def active_players(self):
        return {name: player for name, player in self.players.items() if player.active}

    @property
    def subs(self):
        return {name: player for name, player in self.players.items() if not player.active}

    def _generate_players(self):
        player_names = []
        with open('data/squads/current_ipl_squad.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['team'] == self.name:
                    player_names.append(row['name'])

        players = {name: Player(name, self.name, self.innings) for name in player_names}
        return players

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
