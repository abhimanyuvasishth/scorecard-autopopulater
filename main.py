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
    game = 1
    g = GoogleSheet()
    url_ids = [(1253264, 1253273)]
    start_time = time.time()
    for series_id, match_id in url_ids:
        match = Match(series_id, match_id)
        if match.players:
            pass
            # for player_name in match.players.keys():
            #     player_info = match.get_player_info(player_name)
            #     write_player_row(g, player_info, game)
