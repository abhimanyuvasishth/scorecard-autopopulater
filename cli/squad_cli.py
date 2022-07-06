from dataclasses import asdict

import click

from scorecard_autopopulater.scraper.cricinfo_squad_scraper import CricinfoSquadScraper
from scorecard_autopopulater.writer.csv_writer import CsvWriter


@click.group(name='squad_cli')
def squad_cli():
    pass


@squad_cli.command(
    name='write_squads_to_csv',
    help='writes the squads for a tournament to csv',
)
@click.option('-u', '--url', type=str, required=True, help='url with squads list')
@click.option('-f', '--file_name', type=click.Path(), required=False, help='file to write to',
              default='data/squads.csv')
def write_squads_to_csv(url, file_name):
    scraper = CricinfoSquadScraper(url)
    CsvWriter(file_name).write_data([asdict(row) for row in scraper.generate_player_rows()])


if __name__ == '__main__':
    squad_cli()
