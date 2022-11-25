import click
import requests

from time import sleep
from cli import logger
from fake_useragent import UserAgent

from scorecard_autopopulater.google_sheet import GoogleSheet

CONFIG = {
    'tournament_id': 1298134,
    'doc_name': 'Fifa World Cup 2022',
    'sheet_name': 'Points Worksheet',
    'start_row': 3,
    'team_gap': 5
}


@click.group(name='football_cli')
def football_cli():
    pass


@football_cli.command(name='process_current_matches')
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    url = 'https://play.fifa.com/json/fantasy/players.json'
    headers = {
        'User-Agent': UserAgent()['google chrome']
    }
    response = requests.get(url, headers=headers)
    player_data = response.json()
    sheet = GoogleSheet(CONFIG['doc_name'], CONFIG['sheet_name'])
    count = 0

    for player in player_data:
        if count and count % 50 == 0:
            sleep(60)
        try:
            if player['stats']['roundScores'] is not None:
                if player['id'] in [336505]:
                    continue
                for match, points in player['stats']['roundScores'].items():
                    if int(match) <= 1:
                        continue
                    sheet.write_data_value(
                        row=sheet.get_player_row(player['name']),
                        col=3 + 3 * int(match),
                        value=int(points)
                    )
                    logger.info([count, player['name'], points])
                    count += 1
        except Exception as e:
            logger.error(f'{player["name"]} failed with {e}')


if __name__ == '__main__':
    football_cli()
