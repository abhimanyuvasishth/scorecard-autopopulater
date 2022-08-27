import csv
from time import perf_counter, sleep

import click

from cli import logger
from scorecard_autopopulater.cricket_match_generator import generate_live_matches
from scorecard_autopopulater.google_sheet import GoogleSheet
from scorecard_autopopulater.match.cricket_match import CricketMatch
from scorecard_autopopulater.scraper.cricket_scraper import find_series_id
from scorecard_autopopulater.scraper.squad import Squad
from scorecard_autopopulater.scraper.stats import Stats

CONFIG = {
    'tournament_id': 1327237,
    'doc_name': 'Asia Cup 2022',
    'sheet_name': 'Points Worksheet',
    'start_row': 3,
    'team_gap': 5
}


@click.group(name='event_cli')
def event_cli():
    pass


@event_cli.command(name='get_points')
def get_points():
    squad = Squad(CONFIG['tournament_id'])
    start_time = perf_counter()
    player_points = {}
    for team in squad.players:
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
                match_team = next(filter(lambda x: x.name == team, match.teams))
                all_points.append(int(match_team.get_player(int(player['id'])).points))

            avg = sum(all_points) / max(len(all_points), 1)
            player_points[player['name']] = {
                'all_points': all_points,
                'total_games': len(all_points),
                'average': avg,
                'url': url,
            }
            elapsed = perf_counter() - start_time
            print(f'{elapsed:0.02f}', player['name'], all_points, f'{avg:0.02f}')

    with open('data.csv', 'w') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerow(['name', 'average', 'total', 'max'])
        for player, data in player_points.items():
            wr.writerow([
                player,
                data['average'],
                data['total_games'],
                data['url'],
                max(data['all_points'] or [0])
            ])


@event_cli.command(name='initialize_squad')
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


@event_cli.command(name='process_current_matches')
@click.option('--dry-run', type=bool, is_flag=True, help='dry run updates')
def process_current_matches(dry_run):
    sheet = GoogleSheet(CONFIG['doc_name'], CONFIG['sheet_name'])
    tournament_id = CONFIG['tournament_id']
    for match in generate_live_matches():
        if tournament_id and match.tournament_id != tournament_id:
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
    event_cli()
