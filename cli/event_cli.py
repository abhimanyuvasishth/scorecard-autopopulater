import click

from cli import logger
from scorecard_autopopulater.factory.cricket_factory import CricketFactory
from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.reader.csv_data_row_reader import CSVDataRowReader
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.schema.player_row import PlayerRow
from scorecard_autopopulater.writer.cricket_sheet_writer import CricketSheetWriter
from scorecard_autopopulater.writer.csv_writer import CsvWriter
from scorecard_autopopulater.writer.stdout_writer import StdoutWriter


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(
    name='process_current_matches',
)
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    match_generator = MatchGenerator(
        match_reader=CSVDataRowReader('data/schedule/current_ipl_schedule.csv', MatchRow),
        squad_reader=CSVDataRowReader('data/squads/current_ipl_squad.csv', PlayerRow),
        factory=CricketFactory(),
        hours_after=48,
        limit=1
    )

    writers = [StdoutWriter(), CsvWriter('data/output/foo.csv')]
    if not dry_run:
        writers.append(CricketSheetWriter(
            GoogleSheet(doc_name='IPL 15 auction', sheet_name='Points Worksheet')
        ))

    for match in match_generator.generate_match_rows():
        match.update_statistics()
        for team in match.teams:
            for player_name, player in team.active_players.items():
                for writer in writers:
                    writer.write_data_item({
                        'player': player,
                        'game_number': team.game_number
                    })
    logger.info('Completed updating sheet')


if __name__ == '__main__':
    event_cli()
