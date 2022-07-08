import click

from cli import logger
from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.writer.cricket_sheet_writer import CricketSheetWriter


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(
    name='process_current_matches',
)
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    writer = CricketSheetWriter(GoogleSheet('IPL 15 auction', 'Points Worksheet'))
    for match in MatchGenerator().generate_matches():
        logger.info(f'Started logging {match.id}')
        for team in match.teams:
            for player in team.players:
                if not dry_run:
                    writer.write_data_item(player, team)
                logger.info({'match_id': match.id, 'team_name': team.long_name, 'player': player})
        logger.info(f'Completed logging {match.id}')


if __name__ == '__main__':
    event_cli()
