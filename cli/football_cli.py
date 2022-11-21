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
        if count == 50:
            count = 0
            sleep(60)
        try:
            if player['status'] != 'available':
                continue
            if player['matchDayPoints']['1'] is not None:
                sheet.write_data_value(
                    row=sheet.get_player_row(player['name']),
                    col=6,
                    value=int(player['matchDayPoints']['1'])
                )
                logger.info([player['name'], player['matchDayPoints']['1']])
                count += 1
        except Exception:
            print(player['name'])


if __name__ == '__main__':
    football_cli()
