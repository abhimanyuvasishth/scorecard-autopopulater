from time import sleep

import click

from cli import logger
from scorecard_autopopulater.cricket_match_generator import generate_matches
from scorecard_autopopulater.google_sheet import GoogleSheet


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(name='process_current_matches')
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
@click.option('--tournament_id', type=int, help='tournament id to scrape')
def process_current_matches(dry_run, tournament_id):
    sheet = GoogleSheet('Sandbox', 'Sandbox')
    for match in generate_matches():
        if tournament_id and match.tournament_id != tournament_id:
            continue
        match.populate()
        logger.info(match)
        for team in match.teams:
            logger.info(team)
            for player in team.players:
                logger.info(player)
                if not dry_run:
                    sheet.write_data_item(player, team)
        logger.info(f'Completed logging {match.id}')
        sleep(60)  # to avoid rate limit issues on google sheets write


if __name__ == '__main__':
    event_cli()
