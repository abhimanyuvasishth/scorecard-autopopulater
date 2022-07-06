import logging

import click

from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.reader.csv_file_match_reader import CSVFileMatchReader
from scorecard_autopopulater.scraper.cricinfo_scorecard_scraper import CricinfoScorecardScraper

logging_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)


@click.group(name='event_cli')
def event_cli():
    pass


# TODO: replace with sheet
@event_cli.command(
    name='process_current_matches',
)
def process_current_matches():
    file_name = 'data/schedule.csv'
    match_generator = MatchGenerator(
        match_reader=CSVFileMatchReader(file_name),
        scraper_type=CricinfoScorecardScraper,
    )
    for match in match_generator.generate_match_rows():
        match.update_statistics()
        for team in match.teams:
            for player_name, player in team.active_players.items():
                try:
                    logging.info(player.info, team.game_number, player)
                except (ValueError, KeyError):
                    logging.error(f'Player not in sheet: {player_name}')
    logger.info('Completed updating sheet')


if __name__ == '__main__':
    event_cli()
