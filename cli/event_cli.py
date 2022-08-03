from time import sleep

import click

from cli import logger
from scorecard_autopopulater.cricket_match_generator import generate_matches
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.scraper.squad import Squad

CONFIG = {
    'tournament_id': 1299141,
    'doc_name': 'The Hundred 2022',
    'sheet_name': 'Points Worksheet',
    'start_row': 3,
    'team_gap': 6
}


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(name='initialize_squad')
def initialize_squad():
    squad = Squad(CONFIG['tournament_id'])
    sheet = GoogleSheet(CONFIG['doc_name'], CONFIG['sheet_name'])
    row_num = CONFIG['start_row']
    for team in squad.players:
        for player in squad.players[team]:
            sheet.sheet.update(f'A{row_num}:B{row_num}', [[player, team]])
            row_num += 1
        row_num += CONFIG['team_gap']
        logger.info(team)
        sleep(60)


@event_cli.command(name='process_current_matches')
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    sheet = GoogleSheet(CONFIG['doc_name'], CONFIG['sheet_name'])
    tournament_id = CONFIG['tournament_id']
    for match in generate_matches():
        if tournament_id and match.tournament_id != tournament_id:
            continue
        logger.info(match)
        match.populate()
        for team in match.teams:
            logger.info(team)
            for player in team.players:
                logger.info(player)
                if not dry_run:
                    sheet.write_data_item(player, team)
        logger.info(f'Completed logging {match.id}')
        if not dry_run:
            sleep(60)  # to avoid rate limit issues on google sheets write


if __name__ == '__main__':
    event_cli()
