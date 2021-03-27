import csv
from google_sheet import GoogleSheet
from match import Match
import time
from utils import get_game_col, letter_to_number, number_to_letter


class Event:
    def __init__(self, test=True):
        self.sheet = GoogleSheet(test)

    def write_player_row(self, info, game_num, player_name):
        player_row = self.sheet.players.index(player_name) + 1
        col_start = get_game_col(game_num)
        col_end = number_to_letter(letter_to_number(col_start) + len(info) - 1)
        self.sheet.update_row(player_row, col_start, col_end, [info])

    def check_players_matching(self):
        players = set()
        with open(f'squads.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] not in self.sheet.players:
                    print(row)
                if row['name'] in players:
                    print(row)
                players.add(row['name'])

        for player in self.sheet.players:
            if player and player not in players:
                print(player)

    def simulate_last_ipl(self):
        with open(f'schedule_2020.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                time.sleep(30)
                match = Match(row['series_id'], row['match_id'])
                for name in match.players.keys():
                    player_info = match.get_player_info(name)
                    team = match.players[name]['team']
                    game = row['game_1'] if team == row['team_1'] else row['game_2']
                    assert team in [row['team_1'], row['team_2']]
                    try:
                        self.write_player_row(player_info, int(game), name)
                    except ValueError:
                        print(name)


if __name__ == '__main__':
    Event().simulate_last_ipl()
