import csv
from google_sheet import GoogleSheet
from match import Match
import time
from utils import get_game_col, letter_to_number, number_to_letter

def write_player_row(g, info, game_num):
    player_row = g.players.index(player_name) + 1
    col_start = get_game_col(game_num)
    col_end = number_to_letter(letter_to_number(col_start) + len(info) - 1)
    g.update_row(player_row, col_start, col_end, [info])

if __name__ == '__main__':
    g = GoogleSheet()
    with open(f'schedule_2020.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            time.sleep(30)
            match = Match(row['series_id'], row['match_id'])
            for player_name in match.players.keys():
                player_info = match.get_player_info(player_name)
                team = match.players[player_name]['team']
                game = row['game_1'] if team == row['team_1'] else row['game_2']
                assert team in [row['team_1'], row['team_2']]
                write_player_row(g, player_info, int(game))
