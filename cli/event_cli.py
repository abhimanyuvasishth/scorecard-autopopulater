from time import sleep

import click

from cli import logger
from scorecard_autopopulater.generator.cricket_match_generator import CricketMatchGenerator
from scorecard_autopopulater.google_sheet import GoogleSheet


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(name='process_current_matches',)
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    sheet = GoogleSheet('Sandbox', 'Sandbox')
    for match in CricketMatchGenerator().generate_matches(limit=5):
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
