from google_sheet import GoogleSheet
from match import Match
import time
import utils

def write_player_row(match, g, player_name):
    player_row = g.players.index(player_name) + 1
    player = match.players[player_name]
    col_start = utils.get_game_col(1)

    info = [
        player.get('runs_scored', 0),
        player.get('balls_faced', 0),
        player.get('strike_rate', 0.0),
        player.get('not_out', 0),
        player.get('overs', 0),
        player.get('economy_rate', 0),
        player.get('wickets', 0),
        player.get('maidens', 0),
        0,
        0,
    ]
    col_end = utils.number_to_letter(utils.letter_to_number(col_start) + len(info) - 1)
    g.update_row(player_row, col_start, col_end, [info])

if __name__ == '__main__':
    game = 1
    g = GoogleSheet()
    match_ids = [
        1237177,
        1216495,
        1216505,
        1216530,
        1216506,
        1216502,
        1216535,
    ]
    start_time = time.time()
    for match_id in match_ids:
        time.sleep(30)
        match = Match(match_id)
        match.scrape_page()
        match.convert_to_csv()
        print(match_id)
        for player_name in match.players.keys():
            try:
                write_player_row(match, g, player_name)
                print(player_name, f'{time.time() - start_time:0.2f}')
            except ValueError:
                print(player_name, 'AAAAA')
