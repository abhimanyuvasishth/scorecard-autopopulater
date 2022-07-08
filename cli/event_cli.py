import click

from cli import logger
from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.google_sheet import GoogleSheet


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(name='process_current_matches',)
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    sheet = GoogleSheet('Sandbox', 'Sandbox')
    for match in MatchGenerator().generate_matches(limit=10):
        logger.info({'match': [match.id, match.series_id, match.stage, match.format]})
        for team in match.teams:
            logger.info({'team': [team.id, team.long_name]})
            for player in team.players:
                if not dry_run:
                    sheet.write_data_item(player, team)
                logger.info({'player': player})
        logger.info(f'Completed logging {match.id}')


if __name__ == '__main__':
    event_cli()
