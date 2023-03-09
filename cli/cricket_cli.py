import csv
import json
from time import perf_counter, sleep

import click

from cli import logger
from scorecard_autopopulater.cricket_match_generator import (generate_live_matches,
                                                             generate_matches_by_tournament)
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.match.cricket_match import CricketMatch
from scorecard_autopopulater.scraper.cricket_scraper import find_series_id
from scorecard_autopopulater.scraper.squad import Squad
from scorecard_autopopulater.scraper.stats import Stats

CONFIG = {
    'tournament_id': 1345038,
    'doc_name': 'IPL 16 Auction',
    'sheet_name': 'Points Worksheet',
    'start_row': 3,
    'team_gap': 5
}


@click.group(name='cricket_cli')
def cricket_cli():
    pass


@cricket_cli.command(name='get_matches')
def get_matches():
    match_configs = []
    for match in generate_matches_by_tournament(tournament_id=CONFIG['tournament_id']):
        match.populate()
        match_configs.append({
            'team_1': match.teams[0].name,
            'team_1_num': match.teams[0].match_number,
            'team_2': match.teams[1].name,
            'team_2_num': match.teams[1].match_number,
            'start_timestamp': match.start_time,
            'object_id': match.id
        })
    print(json.dumps(match_configs))


@cricket_cli.command(name='get_points')
def get_points():
    squad = Squad(CONFIG['tournament_id'])
    start_time = perf_counter()
    player_points = {}
    allowed_teams = [
        'India', 'Australia', 'Pakistan', 'Sri Lanka', 'South Africa',
        'Ireland', 'New Zealand', 'Afghanistan', 'Bangladesh', 'England', 'Zimbabwe', 'Netherlands'
    ]
    for team in squad.players:
        if team not in allowed_teams:
            continue
        print(team)
        for player in squad.players[team]:
            all_points = []
            base_url = 'https://stats.espncricinfo.com/ci/engine/player'
            params = 'class=3;template=results;type=allround;view=match'
            url = f"{base_url}/{player['id']}.html?{params}"
            match_ids = Stats(url).content
            for match_id in match_ids[::-1][:25]:
                series_id = find_series_id(match_id)
                match = CricketMatch(id=match_id, tournament_id=series_id)
                match.populate()
                try:
                    match_team = next(filter(lambda x: x.name == team, match.teams))
                    all_points.append(int(match_team.get_player(int(player['id'])).points))
                except Exception as e:
                    print(e)
                    continue

            avg = sum(all_points) / max(len(all_points), 1)
            player_points[player['name']] = {
                'all_points': all_points,
                'total_games': len(all_points),
                'average': avg,
                'url': url,
            }
            elapsed = perf_counter() - start_time
            print(elapsed, player)
            with open('results.csv', 'a') as csvfile:
                wr = csv.writer(csvfile)
                wr.writerow([
                    player['id'],
                    player['name'],
                    team,
                    avg,
                    len(all_points),
                    url,
                    all_points,
                    min(all_points or [0]),
                    max(all_points or [0])
                ])


@cricket_cli.command(name='initialize_squad')
def initialize_squad():
    squad = Squad(CONFIG['tournament_id'])
    sheet = GoogleSheet(CONFIG['doc_name'], CONFIG['sheet_name'])
    row_num = CONFIG['start_row']
    for team in squad.players:
        for player in squad.players[team]:
            sheet.sheet.update(f'A{row_num}:B{row_num}', [[player['name'], team]])
            row_num += 1
        row_num += CONFIG['team_gap']
        logger.info(team)
        sleep(60)


@cricket_cli.command(name='process_current_matches')
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    sheet = GoogleSheet(CONFIG['doc_name'], CONFIG['sheet_name'])
    tournament_id = CONFIG['tournament_id']
    for match in generate_live_matches():
        if tournament_id and match.tournament_id != tournament_id:
            continue
        # ignoring qualifiers
        if match.id < 1298147:
            continue
        logger.info(match)
        match.populate()
        for team in match.teams:
            logger.info(team)
            for player in team.players:
                logger.info(player)
                if not dry_run:
                    sheet.write_data_item(player, team)
        logger.info(f'Completed logging {match.id}')
        if not dry_run:
            sleep(60)  # to avoid rate limit issues on google sheets write
    logger.info('Completed processing current matches')


if __name__ == '__main__':
    cricket_cli()
