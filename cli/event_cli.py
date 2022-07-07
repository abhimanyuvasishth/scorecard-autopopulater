import logging

import click

from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.reader.csv_data_row_reader import CSVDataRowReader
from scorecard_autopopulater.schema.match_row import MatchRow
from scorecard_autopopulater.scraper.cricinfo_scorecard_scraper import CricinfoScorecardScraper
from scorecard_autopopulater.writer.google_sheet_writer import GoogleSheetWriter

logging_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(
    name='process_current_matches',
)
def process_current_matches():
    file_name = 'data/schedule/schedule.csv'
    match_generator = MatchGenerator(
        match_reader=CSVDataRowReader(file_name, MatchRow),
        scraper_type=CricinfoScorecardScraper,
    )
    sheet = GoogleSheet(doc_name='IPL 15 auction', sheet_name='Points Worksheet')
    writer = GoogleSheetWriter(sheet)
    for match in match_generator.generate_match_rows():
        match.update_statistics()
        for team in match.teams:
            for player_name, player in team.active_players.items():
                writer.write_player_row(player, team.game_number)
    logger.info('Completed updating sheet')


if __name__ == '__main__':
    event_cli()
