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
    url_ids = [
        (1210595, 1237181),
        (1210595, 1237180),
        (1210595, 1237178),
        (1210595, 1237177),
        (1210595, 1216495),
        (1210595, 1216505),
        (1210595, 1216530),
        (1210595, 1216506),
        (1210595, 1216502),
        (1210595, 1216535),
        (1210595, 1216537),
        (1210595, 1216536),
        (1210595, 1216499),
        (1210595, 1216524),
        (1210595, 1216520),
        (1210595, 1216541),
        (1210595, 1216544),
        (1210595, 1216498),
        (1210595, 1216497),
        (1210595, 1216521),
        (1210595, 1216494),
    ]
    start_time = time.time()
    for series_id, match_id in url_ids:
        time.sleep(30)
        print(match_id)
        match = Match(series_id, match_id)
        match.convert_to_csv()
        for player_name in match.players.keys():
            player_info = match.get_player_info(player_name)
            write_player_row(g, player_info, game)
