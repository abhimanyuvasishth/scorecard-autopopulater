import csv
import logging
from dataclasses import asdict

import click

from scorecard_autopopulater.constants import SheetIntroCols
from scorecard_autopopulater.google_sheet import GoogleSheet
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
              default='data/squads/squads.csv')
def write_squads_to_csv(url, file_name):
    scraper = CricinfoSquadScraper(url)
    CsvWriter(file_name).write_data([asdict(row) for row in scraper.generate_player_rows()])


@squad_cli.command(
    name='get_non_overlapping_players',
    help='gets players that do not overlap between squads and the google sheet',
)
def get_non_overlapping_players():
    sheet = GoogleSheet(doc_name='IPL 15 auction', sheet_name='Points Worksheet')
    sheet_players = {}

    names = sheet.col_values(SheetIntroCols.PLAYER.value)
    abbrevs = sheet.col_values(SheetIntroCols.PLAYING_TEAM.value)

    for i in range(len(names)):
        name, abbrev, row = names[i], abbrevs[i], i + 1
        if name:
            sheet_players[name] = {'name': name, 'abbrev': abbrev, 'row': row}

    players = set()
    with open('data/squads/current_ipl_squad.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['name'] not in sheet_players:
                if row['withdrawn']:
                    logging.warning(f"withdrawn player {row['name']} not in sheet")
                else:
                    logging.error(f"{row['name']} not in sheet")
            if row['name'] in players:
                logging.error(f"{row['name']} duplicated in squad")
            players.add(row['name'])

    for player in sheet_players:
        if player and player not in players:
            logging.error(f"{player.name} not in squad")


if __name__ == '__main__':
    squad_cli()
