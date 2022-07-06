from dataclasses import asdict

import click

from scorecard_autopopulater.scraper.cricinfo_schedule_scraper import CricinfoScheduleScraper
from scorecard_autopopulater.writer.csv_writer import CsvWriter


@click.group(name='schedule_cli')
def schedule_cli():
    pass


@schedule_cli.command(
    name='write_schedule_to_csv',
    help='writes the schedule for a tournament to csv',
)
@click.option('-u', '--url', type=str, required=True, help='url with schedule list')
@click.option('-f', '--file_name', type=click.Path(), required=False, help='file to write to',
              default='data/schedule.csv')
def write_schedule_to_csv(url, file_name):
    scraper = CricinfoScheduleScraper(url)
    CsvWriter(file_name).write_data([asdict(row) for row in scraper.generate_match_rows()])


if __name__ == '__main__':
    schedule_cli()
