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
    for match in CricketMatchGenerator(limit=10).generate_matches():
        logger.info(match)
        for team in match.teams:
            logger.info(team)
            for player in team.players:
                logger.info(player)
                if not dry_run:
                    sheet.write_data_item(player, team)
        logger.info(f'Completed logging {match.id}')


if __name__ == '__main__':
    event_cli()
