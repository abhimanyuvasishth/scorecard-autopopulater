import logging

import click

from scorecard_autopopulater.factory.cricket_factory import CricketFactory
from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.reader.csv_data_row_reader import CSVDataRowReader
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.schema.player_row import PlayerRow
from scorecard_autopopulater.writer.cricket_sheet_writer import CricketSheetWriter

logging_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(
    name='process_current_ipl_matches',
)
def process_current_ipl_matches():
    match_generator = MatchGenerator(
        match_reader=CSVDataRowReader('data/schedule/schedule.csv', MatchRow),
        squad_reader=CSVDataRowReader('data/squads/current_ipl_squad.csv', PlayerRow),
        factory=CricketFactory(),
        hours_after=48,
        limit=1
    )
    sheet = GoogleSheet(doc_name='IPL 15 auction', sheet_name='Points Worksheet')
    writer = CricketSheetWriter(sheet)
    for match in match_generator.generate_match_rows():
        match.update_statistics()
        for team in match.teams:
            for player_name, player in team.active_players.items():
                writer.write_data({
                    'player': player,
                    'game_number': team.game_number
                })
    logger.info('Completed updating sheet')


if __name__ == '__main__':
    event_cli()
